from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from enum import auto, Enum
from inspect import signature
from instructions import Instruction, InstructionType, Operation

class ValueType(Enum):
    INT      = auto() # int
    FLOAT    = auto() # float
    FUNCTION = auto() # tuple[int, list[Instruction]]
    BUILTIN  = auto() # Callable[[Value, ...], Value]

    def is_callable(self) -> bool:
        return self.value >= ValueType.FUNCTION.value

@dataclass(frozen=True, slots=True)
class Value:
    type: ValueType
    inner: int | float | tuple[int, list[Instruction]] | Callable[[Value, ...], Value]

    def __str__(self) -> str:
        match self.type:
            case ValueType.INT | ValueType.FLOAT:
                return str(self.inner)
            case ValueType.FUNCTION:
                return "<function object>"
            case ValueType.BUILTIN:
                return f"<builtin function>"

@dataclass(frozen=True, slots=True)
class InterpreterError(Exception):
    explaination: str

    def __str__(self) -> str:
        return self.explaination

def _max(x: Value, y: Value, /) -> Value:
    if x.type.is_callable() or y.type.is_callable():
        raise InterpreterError("arguments to `max()` can't be functions")
    inner = x.inner if y.inner < x.inner else y.inner
    type = ValueType.INT if isinstance(inner, int) else ValueType.FLOAT
    return Value(type, inner)

def _min(x: Value, y: Value, /) -> Value:
    if x.type.is_callable() or y.type.is_callable():
        raise InterpreterError("arguments to `min()` can't be functions")
    inner = x.inner if x.inner < y.inner else y.inner
    type = ValueType.INT if isinstance(inner, int) else ValueType.FLOAT
    return Value(type, inner)

def _check_parameter_count(actual: int, expected: int):
    if actual != expected:
        raise InterpreterError("call with {actual} parameters instead of {expected}")

class Interpreter:
    __slots__ = "_value_stack", "_call_stack", "_namespace"

    def __init__(self, builtins: Iterable[tuple[str, Callable[[Value, ...], Value]]] = None):
        self._value_stack = []
        self._call_stack = []
        self.reset_namespace(builtins)

    def interpret(self, instruction: Instruction):
        arg = instruction.argument
        match instruction.type:
            case InstructionType.LOAD:
                if (val := self._namespace.get(arg)) is None:
                    raise InterpreterError(f"unknown name `{arg}`")
                self._value_stack.append(val)
            case InstructionType.STORE:
                if not self._value_stack:
                    raise InterpreterError("store with empty stack")
                val = self._value_stack.pop()
                self._namespace[arg] = val
            case InstructionType.PARAM:
                if not self._call_stack or len(self._call_stack[-1]) <= arg:
                    raise InterpreterError("invalid parameter access")
                val = self._call_stack[-1][arg]
                self._value_stack.append(val)
            case InstructionType.CALL:
                if not self._value_stack or len(self._value_stack) <= arg:
                    raise InterpreterError("call with insufficient stack")
                *params, func = self._value_stack[-arg-1:]
                match func.type:
                    case ValueType.FUNCTION:
                        arg_count, instructions = func.inner
                        _check_parameter_count(arg, arg_count)
                        stack = self._value_stack
                        self._value_stack = []
                        self._call_stack.append(params)
                        try:
                            for i in instructions:
                                self.interpret(i)
                            if len(self._value_stack) != 1:
                                raise InterpreterError("function did not return correctly")
                            val = self._value_stack[0]
                        finally:
                            self._call_stack.pop()
                            self._value_stack = stack
                    case ValueType.BUILTIN:
                        arg_count = len(signature(func.inner).parameters)
                        _check_parameter_count(arg, arg_count)
                        try:
                            if (val := func.inner(*params)) is None:
                                return
                        except Exception as e:
                            raise InterpreterError(f"builtin raised {e!r}")
                    case _:
                        raise InterpreterError("called non-callable")
                del self._value_stack[-arg:]
                self._value_stack[-1] = val
            case InstructionType.OPERATION:
                stack_err = InterpreterError(f"insufficient stack for {arg}")
                func_err  = InterpreterError("{arg} cannot be applied to callable")
                if arg is Operation.NEG:
                    if not self._value_stack:
                        raise stack_err
                    if self._value_stack[-1].type.is_callable():
                        raise func_err 
                    val = self._value_stack.pop()
                    val = Value(val.type, -val.inner)
                    self._value_stack.append(val)
                elif len(self._value_stack) < 2:
                    raise stack_err
                elif self._value_stack[-1].type.is_callable() or self._value_stack[-2].type.is_callable():
                    raise func_err
                else:
                    rhs = self._value_stack.pop().inner
                    lhs = self._value_stack.pop().inner
                    match arg:
                        case Operation.ADD:
                            op = lambda x, y: x + y
                        case Operation.SUB:
                            op = lambda x, y: x - y
                        case Operation.MULT:
                            op = lambda x, y: x * y
                        case Operation.DIV:
                            op = lambda x, y: x / y
                        case Operation.IDIV:
                            op = lambda x, y: x // y
                        case Operation.POW:
                            op = lambda x, y: x ** y
                    val = op(lhs, rhs)
                    type = ValueType.INT if isinstance(val, int) else ValueType.FLOAT
                    self._value_stack.append(Value(type, val))
            case InstructionType.INT:
                self._value_stack.append(Value(ValueType.INT, arg))
            case InstructionType.FLOAT:
                self._value_stack.append(Value(ValueType.FLOAT, arg))
            case InstructionType.FUNCTION:
                self._value_stack.append(Value(ValueType.FUNCTION, arg))

    def print_stack(self):
        for val in self._value_stack:
            print(val)

    def print_namespace(self):
        for name, val in self._namespace.items():
            print(f"{name}={val}")

    def reset_stack(self):
        self._value_stack = []

    def reset_namespace(self, builtins: Iterable[tuple[str, Callable[[Value, ...], Value]]] = None):
        if builtins is None:
            builtins = (
                ("max", _max),
                ("min", _min),
            )
        self._namespace = {name: Value(ValueType.BUILTIN, f) for name, f in builtins}

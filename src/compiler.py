from instructions import Instruction, InstructionType, Operation
from nodes import Node, NodeType

def compile(node: Node) -> list[Instruction]:
    match node.type:
        case NodeType.ASSIGNMENT:
            name, node = node.data
            store = Instruction(InstructionType.STORE, name)
            instructions = compile(node)
            instructions.append(store)
            return instructions
        case NodeType.DEFINITION:
            name, args, node = node.data
            store = Instruction(InstructionType.STORE, name)
            instructions = compile(node)
            for i, instr in enumerate(instructions):
                if instr.type is not InstructionType.LOAD:
                    continue
                try:
                    j = args.index(instr.argument)
                    new = Instruction(InstructionType.PARAM, j)
                    instructions[i] = new
                except ValueError:
                    pass
            func = (len(args), instructions)
            func = Instruction(InstructionType.FUNCTION, func)
            return [func, store]
        case NodeType.ADDITION:
            operation = Operation.ADD
        case NodeType.SUBTRACTION:
            operation = Operation.SUB
        case NodeType.MULTIPLICATION:
            operation = Operation.MULT
        case NodeType.DIVISION:
            operation = Operation.DIV
        case NodeType.IDIVISION:
            operation = Operation.IDIV
        case NodeType.NEGATION:
            instructions = compile(node.data)
            neg = Instruction(InstructionType.OPERATION, Operation.NEG)
            instructions.append(neg)
            return instructions
        case NodeType.POWER:
            operation = Operation.POW
        case NodeType.IDENTIFIER:
            name = node.data
            return [Instruction(InstructionType.LOAD, name)]
        case NodeType.CALL:
            id, params = node.data
            load = Instruction(InstructionType.LOAD, id)
            call = Instruction(InstructionType.CALL, len(params))
            return [load, call]
        case NodeType.INT:
            int = node.data
            int = Instruction(InstructionType.INT, int)
            return [int]
        case NodeType.FLOAT:
            float = node.data
            float = Instruction(InstructionType.FLOAT, float)
            return [float]
    lhs, rhs = map(compile, node.data)
    lhs += rhs
    lhs.append(Instruction(InstructionType.OPERATION, operation))
    return lhs

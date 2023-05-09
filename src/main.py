from compiler import compile
from interpreter import Interpreter
from parser import Parser
from tokenizer import Tokenizer

def main():
    text = "f(t,v,s)=-1/2*g*t**2+v*t+s h(t)=f(t,0,0) g=9.81 max(h(1), 0) f(1, 5, 5) f max"
    tokenizer = Tokenizer(text)
    parser = Parser(tokenizer)
    interpreter = Interpreter()
    for statement in parser:
        instructions = compile(statement)
        for i in instructions:
            interpreter.interpret(i)
    interpreter.output_stack()

if __name__ == "__main__":
    main()

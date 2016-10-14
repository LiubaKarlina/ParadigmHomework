import yat.model
from yat.model import *

class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, number):
        return number

    def visitFunction(self, function):
        body = list()
        if function.body:
            for i in function.body:
                body.append(i.visit(self))
        return Function(function.args, body)

    def visitFunctionCall(self, function_call):
        args = list()
        if function_call.args:
            for arg in function_call.args:
                args.append(arg.visit(self))
        return FunctionCall(function_call.fun_expr.visit(self), args)

    def visitFunctionDefinition(self, function_def):
        return FunctionDefinition(function_def.name, function_def.function.visit(self))

    def visitBinaryOperation(self, binary):
        left = binary.lhs.visit(self)
        right = binary.rhs.visit(self)
        if type(left) is Number:
            if type(right) is Number:
                return binary.evaluate(Scope())
            elif binary.op == '*':
                if left.value == 0 and type(right) is Reference:
                    return Number(0)
        elif type(right) is Number and binary.op == '*':
            if right.value == 0 and type(left) is Reference:
                return Number(0)
        elif binary.op == '-' and type(left) is Reference and type(right) is Reference:
            if left.name == right.name:
                return Number(0)
        return binary


    def visitUnaryOperation(self, unary):
        if type(unary.expr) is Number:
            return unary.evaluate(Scope())

    def visitConditional(self, cond):
        cond.condtion = cond.condtion.visit(self)
        if (cond.if_true):
            for i in cond.if_true:
                i = i.visit(self)
            if (cond.if_false):
                for i in cond.if_false:
                    i = i.visit(self)
        return cond

    def visitReference(self, reference):
        return reference

    def visitPrint(self, prin):
        return prin.expr.visit(self)

    def visitRead(self, read):
        return read


def main():
    un = UnaryOperation('-', Print(Number(0)))
    f = ConstantFolder()

    b = BinaryOperation(Number(34), '-', Number(3))
    #r = f.visit(b)
    con = Conditional(Number(1), [Number(1), Number(1)], [Number(3)])
    con1 = Conditional(Number(1), [], [])
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '-',
                                                    Reference('hello'))),
                              Read('hello'),
                              b
                              ])
    fd = FunctionDefinition('foo', parent['foo'])
    function = Function(['hello'], [UnaryOperation('-', Reference('hello')), con, con1])
    definition = FunctionDefinition('foo', function)
    p = Read('xox')
    un = UnaryOperation('!', Number(0))
    funcall = FunctionCall(definition,
                           [Number(5)])
    reference = model.Reference('foo')
    call = FunctionCall(BinaryOperation(Number(1), '*', Number(3)), [Number(1), Number(2), Number(3)])
    rer = f.visit(call)

if __name__ == "__main__":
    main()
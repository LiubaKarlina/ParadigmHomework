import yat.model
from yat.model import *

class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, number):
        return Number(number.value)

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
                return BinaryOperation(left, binary.op, right).evaluate(Scope())
            elif binary.op == '*':
                if left.value == 0 and type(right) is Reference:
                    return Number(0)
        elif type(right) is Number and binary.op == '*':
            if right.value == 0 and type(left) is Reference:
                return Number(0)
        elif binary.op == '-' and type(left) is Reference and type(right) is Reference:
            if left.name == right.name:
                return Number(0)
        return BinaryOperation(left, binary.op, right)


    def visitUnaryOperation(self, unary):
        expr = unary.expr.visit(self)
        if type(expr) is Number:
            return UnaryOperation(unary.op, expr).evaluate(Scope())
        return UnaryOperation(unary.op, expr)

    def visitConditional(self, cond):
        condtion = cond.condtion.visit(self)
        true = list()
        false = list()
        if (cond.if_true):
            for i in cond.if_true:
                true.append(i.visit(self))
            if (cond.if_false):
                for i in cond.if_false:
                    false.append(i.visit(self))
        return Conditional(condtion, true, false)

    def visitReference(self, reference):
        return Reference(reference.name)

    def visitPrint(self, prin):
        expr = prin.expr.visit(self)
        return Print(expr)

    def visitRead(self, read):
        return Read(read.name)


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
    definition = FunctionDefinition('foo', parent["foo"])
    p = Read('xox')
    un = UnaryOperation('!', Number(0))
    funcall = FunctionCall(definition,
                           [Number(5)])
    reference = model.Reference('foo')
    call = FunctionCall(BinaryOperation(Number(1), '*', Number(3)), [Number(1), Number(2), Number(3)])
    un = UnaryOperation('-', Reference('hello'))
    rer = f.visit(fd)
    #pg = PrettyPrinter()
    #pg.visit(fd)
    un = UnaryOperation('+', Reference('hello'))
    #pg.visit(rer)

if __name__ == "__main__":
    main()
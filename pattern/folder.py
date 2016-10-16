import model
from printer import *
from model import *


class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, number):
        return Number(number.value)

    def make(self, old_l):
        new_l = list()
        if old_l:
            for elem in old_l:
                new_l.append(elem.visit(self))
        return new_l

    def visitFunctionCall(self, function_call):
        args = self.make(function_call.args)
        return FunctionCall(function_call.fun_expr.visit(self), args)

    def visitFunctionDefinition(self, function_def):
        body = self.make(function_def.function.body)
        return FunctionDefinition(
            function_def.name, Function(function_def.function.args, body))

    def visitBinaryOperation(self, binary):
        left = binary.lhs.visit(self)
        right = binary.rhs.visit(self)
        if type(left) is Number:
            if type(right) is Number:
                return BinaryOperation(left, binary.op,
                                       right).evaluate(Scope())
            elif binary.op == '*':
                if left.value == 0 and type(right) is Reference:
                    return Number(0)
        elif type(right) is Number and binary.op == '*':
            if right.value == 0 and type(left) is Reference:
                return Number(0)
        elif binary.op == '-':
            if type(left) is Reference and type(right) is Reference:
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
        true = self.make(cond.if_true)
        false = self.make(cond.if_false)
        return Conditional(condtion, true, false)

    def visitReference(self, reference):
        return Reference(reference.name)

    def visitPrint(self, prin):
        return Print(prin.expr.visit(self))

    def visitRead(self, read):
        return Read(read.name)


def main():
    print("None")

if __name__ == "__main__":
    main()

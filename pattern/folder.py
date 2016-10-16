import yat.model as model


class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, number):
        return model.Number(number.value)

    def make(self, old_l):
        new_l = list()
        if old_l:
            for elem in old_l:
                new_l.append(elem.visit(self))
        return new_l

    def visitFunctionCall(self, function_call):
        args = self.make(function_call.args)
        return model.FunctionCall(function_call.fun_expr.visit(self), args)

    def visitFunctionDefinition(self, function_def):
        body = self.make(function_def.function.body)
        return model.FunctionDefinition(function_def.name,
                                        model.Function(function_def.function.args, body))

    def visitBinaryOperation(self, binary):
        left = binary.lhs.visit(self)
        right = binary.rhs.visit(self)
        if type(left) is model.Number:
            if type(right) is model.Number:
                return model.BinaryOperation(left, binary.op,
                                             right).evaluate(Scope())
            elif binary.op == '*':
                if left.value == 0 and type(right) is model.Reference:
                    return model.Number(0)
        elif type(right) is model.Number and binary.op == '*':
            if right.value == 0 and type(left) is model.Reference:
                return model.Number(0)
        elif binary.op == '-':
            if type(left) is model.Reference and type(right) is model.Reference:
                if left.name == right.name:
                    return model.Number(0)
        return model.BinaryOperation(left, binary.op, right)

    def visitUnaryOperation(self, unary):
        expr = unary.expr.visit(self)
        if type(expr) is model.Number:
            return model.UnaryOperation(unary.op, expr).evaluate(model.Scope())
        return model.UnaryOperation(unary.op, expr)

    def visitConditional(self, cond):
        true = self.make(cond.if_true)
        false = self.make(cond.if_false)
        return model.Conditional(cond.condtion.visit(self), true, false)

    def visitReference(self, reference):
        return model.Reference(reference.name)

    def visitPrint(self, prin):
        return model.Print(prin.expr.visit(self))

    def visitRead(self, read):
        return model.Read(read.name)


def main():
    f = ConstantFolder()
    n = f.visit(model.UnaryOperation("-", model.Number(6)))
    print(n.value)

if __name__ == "__main__":
    main()

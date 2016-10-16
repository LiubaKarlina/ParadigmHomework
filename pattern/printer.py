import yat.model


class PrettyPrinter:

    def __init__(self):
        self.tab = 0

    def print_tab(self):
        print(self.tab * 4 * ' ', end='')

    def visit(self, tree):
        tree.visit(self)
        print(';')

    def visitNumber(self, number):
        print(number.value, end='')

    def forn(self, for_iter):
        if for_iter:
            self.tab += 1
            for comand in for_iter:
                self.print_tab()
                comand.visit(self)
                print(';')
            self.tab -= 1

    def visitFunctionCall(self, function_call):
        function_call.fun_expr.visit(self)
        print('(', end='')
        args = function_call.args
        if args:
            args[0].visit(self)
            for arg in args[1:]:
                print(', ', end='')
                arg.visit(self)
        print(')', end='')

    def visitFunctionDefinition(self, function_def):
        print('def ' + function_def.name + '(', end='')
        fun = function_def.function
        if fun.args:
            print(','.join(fun.args), end='')
        print(') {')
        self.forn(fun.body)
        self.print_tab()
        print('}', end='')

    def visitBinaryOperation(self, binary):
        print('(', end='')
        binary.lhs.visit(self)
        print(' ' + binary.op + ' ', end='')
        binary.rhs.visit(self)
        print(')', end='')

    def visitUnaryOperation(self, unary):
        print(unary.op + '(', end='')
        unary.expr.visit(self)
        print(')', end='')

    def visitConditional(self, cond):
        print('if (', end='')
        cond.condtion.visit(self)
        print(') {')
        self.forn(cond.if_true)
        self.print_tab()
        print("} else {")
        self.forn(cond.if_false)
        self.print_tab()
        print('}', end='')

    def visitReference(self, reference):
        print(reference.name, end='')

    def visitPrint(self, prin):
        print('print', end=' ')
        prin.expr.visit(self)

    def visitRead(self, read):
        print('read ' + read.name, end='')


def main():
    p = PrettyPrinter()
    p.visit(model.UnaryOperation("!", model.Number(6)))
    bo2 = model.BinaryOperation(model.FunctionCall(model.Reference('foo'), [model.BinaryOperation(model.Reference('o'), '*', model.Number(0)), model.Number(10), model.Number(100)]), '*', model.Reference('i'))
    func = model.FunctionDefinition('hard', model.Function(['a', 'b', 'c', 'd'], [model.UnaryOperation('-', model.Number(0)), model.BinaryOperation(model.Reference('a'), '*', model.Number(1)), model.Number(0), model.Conditional(model.Number(0), [], [bo2])]))
    p.visit(bo2)

if __name__ == "__main__":
    main()

class Scope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.dict = dict()

    def __getitem__(self, key):
        if key not in self.dict:
            if self.parent:
                return self.parent[key]
        else:
            return self.dict[key]

    def __setitem__(self, key, value):
            self.dict[key] = value


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def visit(self, visitor):
        return visitor.visitNumber(self)


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = None
        for i in self.body:
            res = i.evaluate(scope)
        return res


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def visit(self, visitor):
        return visitor.visitFunctionDefinition(self)


class Conditional:
    def __init__(self, condtion, if_true, if_false=None):
        self.condtion = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        res = None
        if self.condtion.evaluate(scope).value:
            to_do = self.if_true
        else:
            to_do = self.if_false
        if to_do:
            for com in to_do:
                res = com.evaluate(scope)
        return res

    def visit(self, visitor):
        return visitor.visitConditional(self)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        number = self.expr.evaluate(scope)
        print(number.value)
        return number

    def visit(self, visitor):
        return visitor.visitPrint(self)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        n = int(input())
        scope[self.name] = Number(n)
        return scope[self.name]

    def visit(self, visitor):
        return visitor.visitRead(self)


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        self.function = self.fun_expr.evaluate(scope)
        self.call_scope = Scope(scope)
        for name_arg, arg in zip(self.function.args, self.args):
            self.call_scope[name_arg] = arg.evaluate(scope)
        return self.function.evaluate(self.call_scope)

    def visit(self, visitor):
        return visitor.visitFunctionCall(self)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def visit(self, visitor):
        return visitor.visitReference(self)


class BinaryOperation:
    comand = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x // y,
        '%': lambda x, y: x % y,
        '&&': lambda x, y: x and y,
        '||': lambda x, y: x or y,
        '==': lambda x, y: 1 if x == y else 0,
        '<': lambda x, y: 1 if x < y else 0,
        '>': lambda x, y: 1 if x > y else 0,
        '<=': lambda x, y: 1 if x <= y else 0,
        '>=': lambda x, y: 1 if x >= y else 0,
        '!=': lambda x, y: 1 if x != y else 0,
    }

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        return Number(self.comand[self.op](self.lhs.evaluate(scope).value,
                                           self.rhs.evaluate(scope).value))

    def visit(self, visitor):
        return visitor.visitBinaryOperation(self)


class UnaryOperation:

    comand = {
        '-': lambda x: -x,
        '!': lambda x: 0 if x else 1
    }

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        return Number(self.comand[self.op](self.expr.evaluate(scope).value))

    def visit(self, visitor):
        return visitor.visitUnaryOperation(self)


def main():
    print("Hey")

if __name__ == "__main__":
    main()

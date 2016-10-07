class Scope(object):
    def __init__(self, parent = None):
        self.parent = parent
        self.dict = dict()
    def __getitem__(self, key):
        if key not in self.dict:
            if self.parent:
                return self.parent.dict[key]
        return self.dict[key]
    def __setitem__(self, key, value):
            self.dict[key] = value
    def __delitem__(self, key):
        del self.dict[key]

class Number:
    def __init__(self, value):
        self.value = value
    def evaluate(self, scope):
        return self

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

class Conditional:
    def __init__(self, condtion, if_true, if_false = None):
        self.condtion = condition
        self.if_true = if_true
        self.if_false = if_false
    def evaluate(self, scope):
        res = None
        if self.condition.evaluate(scope).value:
            for i in if_true:
                res = i.evaluate(scope)
            return res
        else:
            for i in if_false:
                res = i.evaluate(scope)
            return res

class Print:
    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, scope):
        value = self.expr.evaluate(scope).value
        print(value)
        return value

class Read:
    def __init__(self, name):
        self.name = name
    def evaluate(self, scope):
        n = int(input())
        scope[self.name] = n
        return scope[self.name]


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args
    def evaluate(self, scope):
        self.function = self.fun_expr.evaluate(scope)
        self.call_scope = Scope(scope)
        i = 0
        for arg in self.args:
            self.call_scope[self.function.args[i]] = arg.evaluate(scope)
            i += 1
        return self.function.evaluate(self.call_scope)

class Reference:
    def __init__(self, name):
        self.name = name
    def evaluate(self, scope):
        return scope[self.name]

class BinaryOperation:
    comand ={
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '%': lambda x, y: x % y,
        '&&': lambda x, y: x and y,
        '||': lambda x, y: x or y,
        '==': lambda x, y: 1 if x == y else 0,
        '<' : lambda x, y: 1 if x < y else 0,
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
        return Number(self.comand[self.op](self.lhs.evaluate(scope).value, self.rhs.evaluate(scope).value))

class UnaryOperation:

    comand = {
        '-': lambda x: -x,
        '!': lambda x: not x
    }
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    def evaluate(self, scope):
        return Number(self.comand[self.op](self.expr.evaluate(scope).value))


def main():
    print("Hey")
    #parent = Scope()

    #parent["bar"] = Number(10)
    #scope = Scope(parent)
    #assert 10 == scope["bar"].value

    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                   Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    #pr = Print(UnaryOperation('-', Number(3)))
    #pr.evaluate(scope)
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

if __name__ == "__main__":
    main()
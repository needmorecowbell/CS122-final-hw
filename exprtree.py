from abc import ABCMeta,abstractmethod
from vartree import VarTree
from machine import *

def compile_tree( exp, variables, functions, prog ):
    exp.compile(variables, functions, prog)

def next_num():
    num = 1
    while True: 
        yield num
        num +=1
    
center = next_num()        
def next_reg():
    return next(center)

class ExprTree(metaclass=ABCMeta):
    """Abstract class for expression"""
    def __str__(self):
        return ' '.join( str(x) for x in iter(self) )

    #   All of the derived class mus implement these functions
    @abstractmethod
    def __iter__(self):
        """an inorder iterator for this tree node, for display"""
        pass
    @abstractmethod
    def postfix(self):
        """a post-order iterator to create a postfix expression"""
        pass
    @abstractmethod
    def evaluate(self, variables,functions):
        """evaluate using the existing variables"""
        pass

class Var(ExprTree):
    """A variable leaf"""
    def __init__(self, n):
        self._name = n
    def __iter__(self):
        yield self._name
    def postfix(self):
        yield self._name
    def evaluate(self, variables,functions):
        return variables.lookup(self._name)
    def compile(self, variables, functions, code):
        code.append(Load(next_reg(), variables.lookup_pos(self._name)))

class Value(ExprTree):
    """A value leaf"""
    def __init__(self, v):
        self._value = v
    def __iter__(self):
        yield self._value
    def postfix(self):
        yield self._value
    def evaluate(self, variables,functions):
        return self._value
    def compile(self, variables, functions, code):
        code.append(Initialize(next_reg(), self._value))

class Oper(ExprTree):
    """A binary operation"""
    def __init__(self, l, o, r):
        self._left = l
        self._oper = o
        self._right = r
    def __iter__(self):
        yield '('
        yield from self._left
        yield self._oper
        yield from self._right
        yield ')'
    def postfix(self):
        yield from self._left.postfix()
        yield from self._right.postfix()
        yield self._oper
    def evaluate(self, variables, functions):
        if self._oper == '=':
            value = self._right.evaluate(variables, functions)
            variables.assign( self._left._name, value)
            return value
        else:
            op1 = self._left.evaluate(variables, functions)
            op2 = self._right.evaluate(variables, functions)
            return eval( str(op1)+self._oper+str(op2) )
        
    def compile(self, variables, functions, code):
        if self._oper != '=':
            
            self._left.compile(variables, functions, code)
            ans_left = code[-1].get_temp()
            
            
            self._right.compile(variables, functions, code)
            ans_right = code[-1].get_temp()
            
            code.append(Compute(next_reg(), ans_left, self._oper, ans_right))
            
        else:
            self._right.compile(variables, functions, code)
            ans_right = code[-1].get_temp()
            ans_left = variables.lookup_pos(self._left._name)
            
            code.append(Store(ans_right, ans_left))

class Cond(ExprTree):
    """A conditional expression"""
    def __init__(self, b, t, f):
        self._test = b
        self._true = t
        self._false = f
    def __iter__(self):
        yield '('
        yield from self._test
        yield '?'
        yield from self._true
        yield ':'
        yield from self._false
        yield ')'
    def postfix(self):
        pass     # postfix conditional not required
    def evaluate(self, variables, functions):
        if self._test.evaluate(variables, functions):
            return self._true.evaluate(variables, functions)
        else:
            return self._false.evaluate(variables, functions)

class Call(ExprTree):
    """A function call"""
    def __init__(self, n, a):
        self._name = n
        self._args = a
    def __iter__(self):
        yield self._name
        yield '('
        yield self._args[0]
        for i in range(1,len(self._args)):
            yield ','
            yield self._args[i]
        yield ')'
    def postfix(self):
        pass
    def evaluate(self, variables, functions):
        parms, body = functions.lookup(self._name)
        new_vars = VarTree()
        for i in range(len(parms)):
            new_vars.assign(parms[i], self._args[i].evaluate(variables,functions))
        return body.evaluate( new_vars, functions)



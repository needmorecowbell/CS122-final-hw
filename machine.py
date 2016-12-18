
class Instruction:
    """Simple instructions representative of a RISC machine

    These instructions are mostly immutable -- once constructed,
    they will not be changed -- only displayed and executed
    """
    def __init__(self, t):      # default constructor
        self._temp = t          # every instruction has a register

    def get_temp(self):         #     which holds its answer
        return self._temp

class Print(Instruction):
    """A simple non-RISC output function to display a value"""
    def __str__(self):
        return "print T" + str(self._temp)
    
    def execute(self,temps,stack,pc,sp):
        print(temps[self._temp])
        
class Initialize(Instruction):

    def __init__(self, temp, val):
        self._temp = temp
        self._value = val

    def __str__(self):
        return "T" + str(self._temp) + "=" + self._value
    
    def execute(self, temps, stack, pc, sp):
         temps[self._temp] = self._value
          
class Load(Instruction):
    
    def __init__(self, temp, loc):
        self._temp = temp
        self._loc = loc
        
    def __str__(self):
        return "T" + str(self._temp) + "= stack [" + str(self._loc) + "]"
        
    def execute(self, temps, stack, pc, sp): 
         temps[self._temp] = stack[self._loc]
    
class Store(Instruction):
    
    def __init__(self, temp, location):
        self._temp = temp
        self._loc = location
        
    def __str__(self):
        return "stack[" + str(self._loc) + "] = T" + str(self._temp) 
    
    def execute(self, temps, stack, pc, sp):
        stack[self._loc]= temps[self._temp]
        
class Compute(Instruction):
    
    def __init__(self, temp, left, op, right):
        self._temp = temp
        self._left = left
        self._oper = op
        self._right = right
        
    def __str__(self):
        return "T" + str(self._temp) + "= (T" + str(self._left) +  self._oper + "T" + str(self._right) + ")"
    
    def execute(self, temps, stack, pc, sp):
         temps[self._temp] = eval(str(temps[self._left]) +  self._oper + str(temps[self._right]))
          

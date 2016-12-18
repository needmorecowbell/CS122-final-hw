class List:                             #A simple singly linked list"""
    class Node:                         #An element of the linked list
        __slots__ = "_value","_next"
        def __init__(self, v, n):
            self._value = v
            self._next = n
        def __str__(self):
            return str(self._value)    
        
    def __init__(self):                #Creates new list
        self._head = self.Node(None,None)

    def push(self,value):               #Adds value in constant time
        self._head = self.Node(value,self._head)
        
    def pop(self):                      #Retrives last insertion     
        if(len(self) > 0):
            current = self._head
            self._head = self._head._next
            return current._value
        return None

    def top(self):                      #returns last insertion, without removal
        return self._head

    def isEmpty(self):
        if(len(self) == 0):
            return True
        else:
            return False
    
    def __iter__(self):                 #An iterator generator to visit the values in sequence"""
        current = self._head
        while current._value is not None:
            yield str(current._value)
            current = current._next
            
    def __len__(self):                  #Return the length of the list
        counter = 0
        current = self._head
        while (current._next is not None):
            counter+=1
            current=current._next
        return counter
    
    def __str__(self):                  #Names the endpoint values and lists all of them"""
        return str(list(iter(self)))








    

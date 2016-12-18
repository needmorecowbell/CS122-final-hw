class VarTree:
    """A simple binary tree to associate variables with values"""
    
    class Node:
        """A simple tree node, with no parent link"""
        __slots__ = "_name", "_value","_left","_right", "_pos"
        def __init__(self,var,val,l, r, pos):
            self._name = var
            self._value = val
            
            self._left = l
            self._right = r
            
            self._pos = pos
            
    def __init__(self):
        self._root = None
        self._size = 0
        
    def _search( self, here, var):
        """search for a variable, returning Node (None if not found)"""
        if here is None:
            return None
        elif here._name == var:
            return here
        elif here._name > var:
            return self._search( here._left, var )
        else:
            return self._search( here._right, var )
    
    def _insert( self, here, var, value):
        
        if here is None:
            self._size += 1
            
            count = self._size
            
            return self.Node( var, value, None, None, count)
        elif here._name == var:
            return self.Node( var, value, here._left, here._right, here._pos )
        elif here._name > var:
            return self.Node( here._name, here._value,
                              self._insert( here._left, var, value),
                              here._right, here._pos  )
        else:
            return self.Node( here._name, here._value, here._left,
                              self._insert( here._right, var, value ), here._pos)
    def assign( self, var, val):
        """Assign value to named variable, by creating a new tree
        root is assigned to refer to the new tree
        """
        self._root = self._insert( self._root, var, val)
        
        
    def lookup( self, var ):
        
        node = self._search( self._root, var )
        
        if node is None:
            self.assign(var, 0 )
            
            return None
            
        else:
            
            return node._value




    def __len__( self ):
        return self._size
        
    def is_empty(self):
        return self._root is None
        
                
    def _rec_iter(self,here):
        if here is not None:
            yield from self._rec_iter(here._left)
            yield here._name, here._value
            yield from self._rec_iter(here._right)
            
    def __iter__( self ):
        if self._root is not None:
            yield from self._rec_iter(self._root)
            
    def __str__( self ):
        return ', '.join( name + '=' + str(val) for name,val in iter(self))
        
    def lookup_pos(self, var):
        """"Memory Addressing"""
        node = self._search( self._root, var )
        if node is None:
            self.assign( var, 0)
            node = self._search( self._root, var )
            return node._pos
        else:
            return node._pos
        

if __name__ == '__main__':
    V = VarTree()
    
   
    

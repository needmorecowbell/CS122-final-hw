class Peekable():
    """An iterator with the ability to examine a value without advancement"""

    def __init__(self, iterator):
        """Take an existing iterator and add peek functionality
        iterator    -- the previous 'ordinary iterator
    """
        self._iterator = iterator;
        self._peeked = None

    #   the following two methods meet the protocol for iterators

    def __iter__(self):
        return self

    def __next__(self):
        """return the next element of the data (as would be expected)
    no advancement occurs if that element has already been peeked at
    """
        if self._peeked is None:
            self._peeked = next(self._iterator)
        ans = self._peeked
        self._peeked = None     # we don't yet see what comes next
        return ans

    def peek(self):
        """peek at the next element of the data
    only advancing if that next item has not yet been peeked at
    """
        if self._peeked is None:
            self._peeked = next(self._iterator)
        return self._peeked


# this function is defined just to allow similarity to next()
def peek(x):
    return x.peek()


"""if __name__ == "__main__":
    i = Peekable(iter([1,2,3,4,5]))
    print( peek(i) )        # peek at the 1
    print( peek(i) )        # and again
    print( next(i) )        # should also be the 1 we were looking at
    print( next(i) )        # move on and return 2
    print( next(i) )        # move on and return 3
    print( peek(i) )        # peek at the 4
    print( next(i) )        # which is still there before this advances
    print( list(Peekable(iter([1,2,3,4,5]))) )   # still iterates normallly"""

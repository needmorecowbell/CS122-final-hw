def new_split_iter(expr):   
   """divide a character string into individual tokens, which need not be separated by spaces (but can be!)
   also, the results are returned in a manner similar to iterator instead of a new data structure
   """
   expr = expr + ";"             # append new symbol to mark end of data, for simplicity
   pos = 0;                      #begin at first character position in the list
   while expr[pos] != ";": 	 #repeat until the end of the input is found.
    
      if expr[pos].isdigit():
         expr1 = ""
         while expr[pos].isdigit():
                expr1 += expr[pos]
                pos += 1
         yield expr1

      elif expr[pos].isalpha():
         expr1 = ""
         while expr[pos].isalnum():
                expr1 += expr[pos]
                pos += 1
         yield expr1
         
      elif expr[pos]==' ':
            pos += 1   

      elif expr[pos] == '=' or '>' or '<' or '!':
         if expr[pos+1] == '=':
            expr1 = expr[pos] + expr[pos+1]
            yield expr1
            pos +=2 
         else: 
            yield expr[pos]
            pos +=1
         
      else:
         if expr[pos] != ' ':
            yield expr[pos]
            pos +=1
   
   yield ";"   

if __name__ == "__main__":
   print( list( new_split_iter("deffn sqr(x,y) = x*x")))
         


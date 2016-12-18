from peekable import Peekable, peek
from newsplit import new_split_iter
from exprtree import Var,Value,Oper,Cond,Call

def tree_assign( iter ):
    left = tree_cond( iter )
    if peek(iter) == '=':
        next(iter)
        right = tree_assign( iter )
        return Oper( left, '=', right )
    else:
        return left

def tree_cond( iter ):
    left = tree_rel( iter )
    if peek(iter) == '?':
        next(iter)
        true_case = tree_cond( iter )
        next(iter)  # : expected
        false_case = tree_cond( iter )
        return Cond( left, true_case, false_case )
    else:
        return left

def tree_rel( iter ):
    left = tree_sum( iter )
    oper = peek(iter)
    while oper in ['<','<=','>','>=','!=','==']:
        next(iter)
        right = tree_sum( iter )
        left = Oper( left, oper, right )
        oper = peek(iter)
    return left

def tree_sum( iter ):
    left = tree_product( iter )
    oper = peek(iter)
    while oper == '+' or oper == '-':
        next(iter)
        right = tree_product( iter )
        left = Oper( left, oper, right )
        oper = peek(iter)
    return left

def tree_product( iter ):
    left = tree_factor( iter )
    oper = peek(iter)
    while oper == '*' or oper == '/' or oper == '%':
        next(iter)
        right = tree_factor( iter )
        left = Oper( left, oper, right )
        oper = peek(iter)
    return left

def tree_factor( iter ):
    item = next(iter)
    if item == '(':
        res = tree_assign( iter )
        next(iter)
        return res
    elif item.isdigit():
        return Value(item)
    elif peek( iter ) == '(':
        next(iter)
        args = [ tree_assign( iter ) ]
        while next(iter) == ',':
            args.append( tree_assign( iter ) )
        return Call(item, args)
    else:
        return Var(item)
        
    
def to_expr_tree( expr ):
    return tree_assign(Peekable((new_split_iter(expr))))

def iter_to_tree(iterator):
    return tree_assign(iterator)

def define_func(iterator):
    next(iterator)              # "deffn"
    name = next(iterator)       # function name
    next(iterator)              # (
    parms = [next(iterator)]    # first argument
    while next(iterator)==',':
        parms.append(next(iterator))
    next(iterator)              # =
    return name, parms, tree_assign(iterator)

if __name__ == "__main__":
    print (to_expr_tree("B= 8"))
    

"""
This file contains the back propagation feature using interface designed in 
forward.py
"""
import autodiff.forward as fwd

def forward_pass(y,val_dict):
    """ 
    The function evaluating each variable/constant and storing their values
    in .val attributes, using atomic variable values from val_dict, in a 
    recursive fashion, starting from root node in the computational graph
        
    INPUTS:
    =======
    val_dict: a dictionary containing variable name and values.
    y: the highest node(root) encompassing all variable in the computational 
    graph
    """
    # forward pass, store values
    if type(y) == fwd.Expression:
        y.val = y.evaluation_at(val_dict)
        if y._sub_expr1 != None:
            forward_pass(y._sub_expr1,val_dict)
        if y._sub_expr2!=None:
            forward_pass(y._sub_expr2,val_dict)
    elif isinstance(y,fwd.Variable):
        y.val = val_dict[y]
    return 

def initialize(top,y):
    """ 
    The function initializing derivative values of each variable/constant
    in the computational graph with respect to the root.
        
    INPUTS:
    =======
    y: the highest node(root) encompassing all variable in the computational 
    graph
    """
    #print(y.val)
    if y == top:
        y.bder = 1 
    else:
        y.bder = 0
    if not isinstance(y,fwd.Variable) and isinstance(y._sub_expr1,fwd.Expression) and not isinstance(y._sub_expr1, fwd.Constant):
        initialize(top,y._sub_expr1)
    if not isinstance(y,fwd.Variable) and isinstance(y._sub_expr2,fwd.Expression) and not isinstance(y._sub_expr2, fwd.Constant):
        initialize(top,y._sub_expr2)   
    return

def backward(y,val_dict,depth = 0):
    """ 
    The function calculating derivative values of each variable/constant
    in the computational graph with respect to the root in a recursive fashion,
    starting from the root node.
        
    INPUTS:
    =======
    y: the highest node(root) encompassing all variable in the computational 
    graph
    val_dict: a dictionary containing variable name and values.
    """
    # val_dict stores the basic variables
    # (atomic,cannot be further decomposed)
    if type(y) == fwd.Expression:
        if y._sub_expr1 != None and isinstance(y._sub_expr1,fwd.Expression):
            y._sub_expr1.bder += y.bder*y.back_derivative(y._sub_expr1,val_dict)
            backward(y._sub_expr1,val_dict,depth+1)
        if y._sub_expr2 != None and isinstance(y._sub_expr2,fwd.Expression) and not isinstance(y._sub_expr2, fwd.Constant):
            y._sub_expr2.bder += y.bder*y.back_derivative(y._sub_expr2,val_dict)
            backward(y._sub_expr2,val_dict,depth+1)
    return 

def back_propagation(y,val_dict):
    """ 
    The wrapper function for three steps of back propogation.
    After calling this function, the .bder attributes of each variables/constant
    in the computational graph stores its first derivative with respect to
    the root node.
        
    INPUTS:
    =======
    y: the highest node(root) encompassing all variable in the computational 
    graph
    val_dict: a dictionary containing variable name and values.
    """
    # get backprop derivative with respect to y at every node lower than y
    forward_pass(y,val_dict)
    initialize(y,y)
    backward(y,val_dict)

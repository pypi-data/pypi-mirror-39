"""
This file contains some root finding algorithms built on top of autodiff.
"""



from autodiff.backprop import back_propagation

def newton_scalar(f, init_val_dict, max_itr, method = 'forward',tol=1e-8):
    """
    Newton's Method finding 0 root for a single expression 
    
    INPUTS
    =======
    f: expression 
    init_val_dict: dictionary containing initial value of variables
    max_itr: maximum iteration before the algorithm stops
    method: string, default set to 'forward mode', in all other cases 
    use 'backward'
    tol: tolerance, the minimum threshold for absolute 
    difference of value of f from 0 for the algorithm to stop
    
    RETURNS
    ========
    variable values corresponding to the 0 point of f
    """
    itr = 1
    val_dict = init_val_dict.copy()
    
    while True:
        evalf = f.evaluation_at(val_dict)
        if method == 'forward':    
            derif = {v: f.derivative_at(v, val_dict) for v in val_dict.keys()}
        else:
            back_propagation(f,val_dict)
            derif = {v:v.bder for v in val_dict.keys()}
        
        for v in val_dict.keys():
            val_dict[v] = val_dict[v] - evalf/derif[v]

        if abs(f.evaluation_at(val_dict)) <= tol: break

        if itr > max_itr:
            print("Exceeded allowable max iterations without finding a root.")

            break
        
        itr += 1
        
    return val_dict
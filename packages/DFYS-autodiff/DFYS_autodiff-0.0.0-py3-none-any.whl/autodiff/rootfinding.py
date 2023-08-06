"""
This file contains some root finding algorithms built on top of autodiff.
"""

import warnings
# import autodiff.forward as fwd

def newton_scalar(f, init_val_dict, max_itr, tol=1e-8):
    
    itr = 1
    val_dict = init_val_dict.copy()
    
    while True:
        evalf = f.evaluation_at(val_dict)
        derif = {v: f.derivative_at(v, val_dict) for v in val_dict.keys()}
        for v in val_dict.keys():
            val_dict[v] = val_dict[v] - evalf/derif[v]

        if abs(f.evaluation_at(val_dict)) <= tol: break

        if itr > max_itr:
            warnings.warn("Exceeded allowable max iterations without finding a root.")
            break
        
        itr += 1
        
    return val_dict
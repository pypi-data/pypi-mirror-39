import numpy as np
from numpy.linalg import multi_dot
from numpy.linalg import norm
from scipy.linalg import solve

def bfgs(f, init_val_dict, max_iter=2000, stop_stepsize=1e-8):
    
    variables  = [var for var in init_val_dict.keys()]
    curr_point = np.array([v for k, v in init_val_dict.items()])
    B          = np.eye(len(curr_point))
    
    for i in range(max_iter):
        
        # solve Bs = - (gradient of f at x)
        curr_val_dict = {var: val for var, val in zip(variables, curr_point)}
        f_grad = f.gradient_at(curr_val_dict)
        s = solve(B, -f_grad)
        if norm(s, ord=2) < stop_stepsize: break
            
        # x_next := x + s
        next_point = curr_point + s

        # y := (gradient of f at x_next) - (gradient of f at x)
        # x := x_next
        next_val_dict = {var: val for var, val in zip(variables, next_point)}
        y = f.gradient_at(next_val_dict) - f.gradient_at(curr_val_dict)
        curr_point = next_point
        
        # B := B + deltaB
        s, y = s.reshape(-1, 1), y.reshape(-1, 1)
        deltaB = multi_dot([y, y.T])/multi_dot([y.T, s]) \
                 - multi_dot([B, s, s.T, B])/multi_dot([s.T, B, s]) 
        B = B + deltaB
    
    return {var: val for var, val in zip(variables, curr_point)}


def newton(f,  init_val_dict, max_iter=1000, stop_stepsize=1e-8,return_history=False):
    
    variables  = [var for var in init_val_dict.keys()]
    curr_point = np.array([v for k, v in init_val_dict.items()])
    f_grad = f.gradient_at(init_val_dict)
    f_hess = f.hessian_at(init_val_dict)
    history = [curr_point.tolist()]
    
    for i in range(max_iter):
        
        curr_val_dict = {var: val for var, val in zip(variables, curr_point)}
        # solve (Hessian of f at x)s = - (gradient of f at x)
        f_grad =f.gradient_at(curr_val_dict)
        f_hess = f.hessian_at(curr_val_dict)

        step = np.linalg.solve(f_hess, -f_grad)
        if np.linalg.norm(step, ord=2) < stop_stepsize: break
        
        # x := x + s
        curr_point = curr_point + step
        history.append(curr_point.tolist())
    
    if return_history:
        return history

    return {var: val for var, val in zip(variables, curr_point)}



def gradient_descent(f,init_val_dict, learning_rate=0.001, max_iter=1000, stop_stepsize=1e-6,return_history=False):
    f_grad = f.gradient_at(init_val_dict)
    variables  = [var for var in init_val_dict.keys()]
    curr_point = np.array([v for k, v in init_val_dict.items()])
    history = [curr_point.tolist()]
    
    for i in range(max_iter):
        
        prev_point =curr_point
        prev_val_dict = {var: val for var, val in zip(variables, prev_point)}
        f_grad =f.gradient_at(prev_val_dict)

        curr_point =curr_point - learning_rate*f_grad
        history.append(curr_point.tolist())
        if np.linalg.norm(curr_point-prev_point, ord=2) < stop_stepsize: break
        
    if return_history:
        return history

    return {var: val for var, val in zip(variables, curr_point)}
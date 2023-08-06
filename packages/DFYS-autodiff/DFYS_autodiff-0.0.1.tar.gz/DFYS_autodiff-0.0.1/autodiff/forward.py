"""
This file contains the central data structure and functions related to the
forward mode auto differentiation. We may want to separate the code into 
multiple files later.
"""

import numpy as np

class Expression:
    def __init__(self, ele_func, sub_expr1, sub_expr2=None):
        self._ele_func  = ele_func
        self._sub_expr1 = sub_expr1
        self._sub_expr2 = sub_expr2
        self.val = None
        self.bder=0
    
    def evaluation_at(self, val_dict):
        
        # self._sub_expr2 is None implies that self._ele_func is an unary operator
        if self._sub_expr2 is None: 
            return self._ele_func.evaluation_at(
                self._sub_expr1, val_dict)
        
        # self._sub_expr2 not None implies that self._ele_func is a binary operator
        else:
            return self._ele_func.evaluation_at(
                self._sub_expr1, self._sub_expr2, val_dict)
    
    def derivative_at(self, var, val_dict, order=1):
        
        # var being a tuple implies multivariate higher derivatives
#        if type(var) is tuple:
#            if len(var) != 2:
#                raise NotImplementedError('only 2nd order derivatives implemented for multivariate derivatives')
#            var1, var2 = var
#            # sub_expr2 being None implies that _ele_func is an unary operator
#            if self._sub_expr2 is None:
#                return self._ele_func.derivative_at(
#                    self._sub_expr1, var, val_dict, order) 
#            # sub_expr2 not None implies that _ele_func is a binary operator
#            else:
#                return self._ele_func.derivative_at(
#                    self._sub_expr1, self._sub_expr2, var, val_dict, order)

        if var is self: 
            if   order == 1: return 1.0
            else: return 0.0
        
        # sub_expr2 being None implies that _ele_func is an unary operator
        if self._sub_expr2 is None:
            return self._ele_func.derivative_at(
                self._sub_expr1, var, val_dict, order)
        
        # sub_expr2 not None implies that _ele_func is a binary operator
        else:
            return self._ele_func.derivative_at(
                self._sub_expr1, self._sub_expr2, var, val_dict, order)
    
    def back_derivative(self,var,val_dict):
        if var is self: return 1.0
        if self._sub_expr2 is None:
            return self._ele_func.backderivative_at(self._sub_expr1,var)
        else:
            return self._ele_func.backderivative_at(self._sub_expr1,
                                                    self._sub_expr2,var)    



    def gradient_at(self, val_dict, returns_dict=False):
        if returns_dict:
            return {v: self.derivative_at(v, val_dict) for v in val_dict.keys()}
        return np.array([self.derivative_at(var, val_dict, order=1) 
                         for var in val_dict.keys()])
    
    def hessian_at(self, val_dict):
        return np.array( [ \
                          [self.derivative_at((var1, var2), val_dict, order=2)
                           for var1 in val_dict.keys()]
                          for var2 in val_dict.keys() \
                          ] )
    
    def __neg__(self):
        return Expression(Neg, self)

                
    def __add__(self, another):
        if isinstance(another, Expression):
            return Expression(Add, self, another)
        # if the other operand is not an Expression, then it must be a number
        # the number then should be converted to a Constant
        else:
            return Expression(Add, self, Constant(another))
    
    
    def __radd__(self, another):
        if isinstance(another, Expression):
            return Expression(Add, another, self)
        else:
            return Expression(Add, Constant(another), self)
    
    def __sub__(self, another):
        if isinstance(another, Expression):
            return Expression(Sub, self, another)
        else:
            return Expression(Sub, self, Constant(another))
    
    def __rsub__(self, another):
        if isinstance(another, Expression):
            return Expression(Sub, another, self)
        else:
            return Expression(Sub, Constant(another), self)
        

    def __mul__(self, another):
        if isinstance(another, Expression):
            return Expression(Mul,self,another)
        else:
            return Expression(Mul, self, Constant(another))

    def __rmul__(self, another):
        if isinstance(another, Expression):
            return Expression(Mul,another,self)
        else:
            return Expression(Mul, Constant(another),self)
    
    def __truediv__(self, another):
        if isinstance(another, Expression):
            return Expression(Div,self,another)
        else:
            return Expression(Div, self, Constant(another))

    def __rtruediv__(self, another):
        if isinstance(another, Expression):
            return Expression(Div,another,self)
        else:
            return Expression(Div, Constant(another),self)
    
    def __pow__(self,another):
        if isinstance(another, Expression):
            return Expression(Pow,self,another)
        else:
            return Expression(Pow, self, Constant(another))
    
    def __rpow__(self,another):
        if isinstance(another, Expression):
            return Expression(Pow,another,self)
        else:
            return Expression(Pow, Constant(another),self)
    
    def __eq__(self, another):
        if not isinstance(another, Expression):
            return False
        return self._ele_func == another._ele_func \
               and self._sub_expr1 == another._sub_expr1 \
               and self._sub_expr2 == another._sub_expr2
               
    def __ne__(self, another):
        return ~self.__eq__(another)
    
    def __hash__(self):
        return object.__hash__(self)   

class Variable(Expression):
    def __init__(self):
        self.val = None
        self.bder = 0
        return
    
    def evaluation_at(self, val_dict):
        return val_dict[self]
    
    def derivative_at(self, var, val_dict, order=1):
        if order == 1:
            return 1.0 if var is self else 0.0
        else:
            return 0.0
    
    def __eq__(self, another):
        return another is self
    
    def __ne__(self, another):
        return ~self.__eq__(another)
    
    def __hash__(self):
        return Expression.__hash__(self) 

class Constant(Expression):
    def __init__(self, val):
        self.val = val
 
    def evaluation_at(self, val_dict):
        return self.val
    
    def derivative_at(self, var, val_dict, order=1):
        return 0.0
    
    def __eq__(self, another):
        if isinstance(another, Constant): return True
        else:                             return False
    
    def __ne__(self, another):
        return ~self.__eq__(another)
    
    def __hash__(self):
        return Expression.__hash__(self) 


class VectorFunction:
    
    def __init__(self, exprlist):
        self._exprlist = exprlist.copy()
    
    def evaluation_at(self, val_dict):
        return np.array([expr.evaluation_at(val_dict) 
                        for expr in self._exprlist])
    
    def gradient_at(self, var, val_dict):
        return np.array([f.derivative_at(var, val_dict) for f in self._exprlist])
    
    def jacobian_at(self, val_dict):
        return np.array([self.gradient_at(var, val_dict)
                         for var in val_dict.keys()]).transpose()


class Add:
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        return sub_expr1.evaluation_at(val_dict) + \
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict, order=1):
        return sub_expr1.derivative_at(var, val_dict, order) + \
               sub_expr2.derivative_at(var, val_dict, order)
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        return 1

class Sub:
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        return sub_expr1.evaluation_at(val_dict) - \
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict, order=1):
        return sub_expr1.derivative_at(var, val_dict, order) - \
               sub_expr2.derivative_at(var, val_dict, order)
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        if var == sub_expr1:
            return 1
        if var == sub_expr2:
            return -1 

class Mul:
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        return sub_expr1.evaluation_at(val_dict) *\
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict,order=1):
        if   order == 1:
            return sub_expr1.derivative_at(var, val_dict) * \
                   sub_expr2.evaluation_at(val_dict)+ \
                   sub_expr1.evaluation_at(val_dict) *\
                   sub_expr2.derivative_at(var, val_dict)
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                term1 = sub_expr1.derivative_at(var, val_dict, order=2) \
                        * sub_expr2.evaluation_at(val_dict)
                term2 = sub_expr2.derivative_at(var, val_dict, order=2) \
                        * sub_expr1.evaluation_at(val_dict)
                term3 = sub_expr1.derivative_at(var1, val_dict, order=1) \
                        * sub_expr2.derivative_at(var2, val_dict, order=1)
                term4 = sub_expr2.derivative_at(var1, val_dict, order=1) \
                        * sub_expr1.derivative_at(var2, val_dict, order=1)
                return term1 + term2 + term3 + term4
            else:
                return Mul.derivative_at(sub_expr1, sub_expr2, (var, var), val_dict, order=2)
#            return sub_expr1.derivative_at(var, val_dict,2)*sub_expr2.evaluation_at(val_dict)+\
#                   sub_expr1.derivative_at(var, val_dict,1)*sub_expr2.derivative_at(var, val_dict,1)+\
#                   sub_expr1.derivative_at(var, val_dict,1)*sub_expr2.derivative_at(var, val_dict,1)+\
#                   sub_expr1.evaluation_at(val_dict)*sub_expr2.derivative_at(var, val_dict,2)
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        if var == sub_expr1:
            return sub_expr2.val
        else:
            return sub_expr1.val
               
class Div:
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        return sub_expr1.evaluation_at(val_dict) /\
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict,order=1):
        if   order == 1:
            return  sub_expr1.derivative_at(var, val_dict) / \
                    sub_expr2.evaluation_at(val_dict)- \
                    sub_expr1.evaluation_at(val_dict) *\
                    sub_expr2.derivative_at(var, val_dict)/\
                    sub_expr2.evaluation_at(val_dict)**2
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                f = sub_expr1.evaluation_at(val_dict)
                g = sub_expr2.evaluation_at(val_dict)
                term1 =  1/g    * sub_expr2.derivative_at(var, val_dict, order=2)
                term2 = -f/g**2 * sub_expr1.derivative_at(var, val_dict, order=2)
                term3 = -1/g**2 * sub_expr1.derivative_at(var1, val_dict, order=1) \
                                * sub_expr2.derivative_at(var2, val_dict, order=1)
                term4 = -1/g**2 * sub_expr1.derivative_at(var2, val_dict, order=1) \
                                * sub_expr2.derivative_at(var1, val_dict, order=1)
                term5 = 2*f/g**3 * sub_expr2.derivative_at(var1, val_dict, order=1) \
                                 * sub_expr2.derivative_at(var2, val_dict, order=1)
                return term1 + term2 + term3 + term4 + term5  
            else:
                return Div.derivative_at(sub_expr1, sub_expr2, (var, var), val_dict, order=2)
#            return ((sub_expr1.derivative_at(var, val_dict,2)*\
#                    sub_expr2.evaluation_at(val_dict)-\
#                    sub_expr1.evaluation_at(val_dict)*\
#                    sub_expr2.derivative_at(var, val_dict,2))*sub_expr2.evaluation_at(val_dict)**2 -\
#                    2*(sub_expr1.derivative_at(var, val_dict,1)*\
#                    sub_expr2.evaluation_at(val_dict) -\
#                    sub_expr1.evaluation_at(val_dict)*\
#                    sub_expr2.derivative_at(var, val_dict,1))*\
#                    sub_expr2.evaluation_at(val_dict)*\
#                    sub_expr2.derivative_at(var, val_dict,1))/\
#                    sub_expr2.evaluation_at(val_dict)**4
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        if var == sub_expr1:
            return 1/sub_expr2.val
        elif var == sub_expr2:
            return -sub_expr1.val/sub_expr2/sub_expr2
#class Pow:
#    
#    @staticmethod
#    def evaluation_at(sub_expr1, sub_expr2, val_dict):
#        return sub_expr1.evaluation_at(val_dict) **\
#               sub_expr2.evaluation_at(val_dict)
#    @staticmethod
#    #f(x)^g(x) * g‘(x)  * ln( f(x) )+ f(x)^( g(x)-1 ) * g(x) * f’(x) 
#    def derivative_at(sub_expr1, sub_expr2, var, val_dict):
#        return  sub_expr1.evaluation_at(val_dict)** \
#                sub_expr2.evaluation_at(val_dict)* \
#                sub_expr2.derivative_at(var, val_dict)*\
#                np.log(sub_expr1.evaluation_at(val_dict))+ \
#                sub_expr1.evaluation_at(val_dict) **\
#                (sub_expr2.evaluation_at(val_dict)-1)*\
#                sub_expr2.evaluation_at(val_dict)*\
#                sub_expr1.derivative_at(var, val_dict)

# a simplified version: assuming sub_expr2 is a constant
class Pow:

    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        return np.power(sub_expr1.evaluation_at(val_dict), 
                        sub_expr2.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict,order=1):
        p = sub_expr2.evaluation_at(val_dict)
        if   order == 1:
            return p*np.power(sub_expr1.evaluation_at(val_dict), p-1.0) \
                   * sub_expr1.derivative_at(var, val_dict)
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                term1 = p*np.power(sub_expr1.evaluation_at(val_dict), p-1.0) \
                        * sub_expr1.derivative_at((var1, var2), val_dict, order=2)
                term2 = p*(p-1.0)*np.power(sub_expr1.evaluation_at(val_dict), p-2.0) \
                        * sub_expr1.derivative_at(var1, val_dict, order=1) \
                        * sub_expr1.derivative_at(var2, val_dict, order=1)
                return term1 + term2
            else:
                return Pow.derivative_at(sub_expr1, sub_expr2, (var, var), val_dict, order=2)
#            return p*(p-1)*np.power(sub_expr1.evaluation_at(val_dict),p-2.0)*sub_expr1.derivative_at(var, val_dict)**2\
#                    + p*np.power(sub_expr1.evaluation_at(val_dict), p-1.0)*sub_expr1.derivative_at(var, val_dict,2)
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        p = sub_expr2.val
        return p*np.power(sub_expr1.val, p-1.0)
#def pow(expr1, expr2):
#    return Expression(Pow, expr1, expr2)

class Exp:
    @staticmethod
    def evaluation_at(sub_expr1, val_dict):
        return np.exp(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1, var, val_dict, order=1):
        if   order == 1:
            return sub_expr1.derivative_at(var, val_dict) * \
                   np.exp(sub_expr1.evaluation_at(val_dict))
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                f = sub_expr1.evaluation_at(val_dict)
                term1 = np.exp(f) * sub_expr1.derivative_at(var,  val_dict, order=2)
                term2 = np.exp(f) * sub_expr1.derivative_at(var1, val_dict, order=1) \
                                  * sub_expr1.derivative_at(var2, val_dict, order=1)
                return term1 + term2
            else:
                return Exp.derivative_at(sub_expr1, (var,var), val_dict, order=2)
#            return np.exp(sub_expr1.evaluation_at(val_dict)) * (sub_expr1.derivative_at(var, val_dict, order=1))**2 \
#                 + np.exp(sub_expr1.evaluation_at(val_dict)) *  sub_expr1.derivative_at(var, val_dict, order=2)
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        return sub_expr1.val
        
class Neg:
    @staticmethod
    def evaluation_at(sub_expr1, val_dict):
        return -sub_expr1.evaluation_at(val_dict)
    
    @staticmethod
    def derivative_at(sub_expr1, var, val_dict, order=1):
        return -sub_expr1.derivative_at(var, val_dict, order)
    @staticmethod
    def back_derivative(sub_expr1,var):
        return -1
def exp(expr):
    return Expression(Exp, expr)


class Sin:
    @staticmethod
    def evaluation_at(sub_expr1, val_dict):
        return np.sin(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1, var, val_dict, order=1):
        if   order == 1:
            return sub_expr1.derivative_at(var, val_dict) * \
        np.cos(sub_expr1.evaluation_at(val_dict))
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                f = sub_expr1.evaluation_at(val_dict)
                term1 =  np.cos(f) * sub_expr1.derivative_at(var,  val_dict, order=2)
                term2 = -np.sin(f) * sub_expr1.derivative_at(var1, val_dict, order=1) \
                                   * sub_expr1.derivative_at(var2, val_dict, order=1)
                return term1 + term2
            else:
                return Sin.derivative_at(sub_expr1, (var,var), val_dict, order=2)
#            return -np.sin(sub_expr1.evaluation_at(val_dict)) * \
#                   sub_expr1.derivative_at(var, val_dict, order=1)**2 + \
#                   np.cos(sub_expr1.evaluation_at(val_dict)) * \
#                   sub_expr1.derivative_at(var, val_dict, order=2)
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        return np.cos(sub_expr1.val)
        
def sin(expr):
    return Expression(Sin, expr)

class Cos:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        return np.cos(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        if   order == 1:
            return -sub_expr1.derivative_at(var, val_dict, order) * \
                   np.sin(sub_expr1.evaluation_at(val_dict)) 
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                f = sub_expr1.evaluation_at(val_dict)
                term1 = -np.sin(f) * sub_expr1.derivative_at(var,  val_dict, order=2)
                term2 = -np.cos(f) * sub_expr1.derivative_at(var1, val_dict, order=1) \
                                   * sub_expr1.derivative_at(var2, val_dict, order=1)
                return term1 + term2
            else:
                return Cos.derivative_at(sub_expr1, (var,var), val_dict, order=2)
#            return -np.cos(sub_expr1.evaluation_at(val_dict)) * \
#                   sub_expr1.derivative_at(var, val_dict, order=1)**2 + \
#                   -np.sin(sub_expr1.evaluation_at(val_dict)) * \
#                   sub_expr1.derivative_at(var, val_dict, order=2)
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        return -np.sin(sub_expr1.val)
        
def cos(expr):
    return Expression(Cos, expr)
    
class Tan:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        return np.tan(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        if   order == 1:
            return sub_expr1.derivative_at(var, val_dict) /(np.cos(sub_expr1.evaluation_at(val_dict))**2)
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                f = sub_expr1.evaluation_at(val_dict)
                term1 = 1/(np.cos(f)**2) * sub_expr1.derivative_at(var,  val_dict, order=2)
                term2 = 2*np.tan(f)/(np.cos(f)**2) \
                        * sub_expr1.derivative_at(var1, val_dict, order=1) \
                        * sub_expr1.derivative_at(var2, val_dict, order=1)
                return term1 + term2
            else:
                return Tan.derivative_at(sub_expr1, (var,var), val_dict, order=2)
#            u = sub_expr1.evaluation_at(val_dict)
#            return 2*np.tan(u)/(np.cos(u)**2) * (sub_expr1.derivative_at(var, val_dict))**2 \
#                           + 1/(np.cos(u)**2) *  sub_expr1.derivative_at(var, val_dict, order=2)
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        return 1/(np.cos(sub_expr1.val)**2)

def tan(expr):
    return Expression(Tan, expr)
    
class Cotan:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        return 1/np.tan(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1): 
        if order == 1:
            return -sub_expr1.derivative_at(var, val_dict)/(np.sin(sub_expr1.evaluation_at(val_dict))**2)
        else: raise NotImplementedError('higher order derivatives not implemented for cotan.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        return -1/(np.sin(sub_expr1.val)**2)          

def cotan(expr):
    return Expression(Cotan, expr)
    
class Sec:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        return 1/np.cos(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * \
               np.tan(x) * (1/np.cos(x))
        else: raise NotImplementedError('higher order derivatives not implemented for sec.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x =sub_expr1.val
        return np.tan(x)/np.cos(x)
        
def sec(expr):
    return Expression(Sec, expr) 

class Csc:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        return 1/np.sin(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return -sub_expr1.derivative_at(var, val_dict) * \
               (1/np.tan(x)) * (1/np.sin(x))
        else: raise NotImplementedError('higher order derivatives not implemented for csc.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        return -(1/np.tan(x)) * (1/np.sin(x))

def csc(expr):
    return Expression(Csc, expr) 

class Sinh:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        return np.sinh(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * np.cosh(x)
        else: raise NotImplementedError('higher order derivatives not implemented for sinh.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        return np.cosh(x)

def sinh(expr):
    return Expression(Sinh, expr) 

class Cosh:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        return np.cosh(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * np.sinh(x)
        else: raise NotImplementedError('higher order derivatives not implemented for cosh.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        return np.sinh(sub_expr1.val)

def cosh(expr):
    return Expression(Cosh, expr) 
    
class Tanh:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        x = sub_expr1.evaluation_at(val_dict)
        return np.sinh(x)/np.cosh(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        tanh = np.sinh(x)/np.cosh(x)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * (1-tanh*tanh)
        else: raise NotImplementedError('higher order derivatives not implemented for tanh.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        tanh = np.sinh(x)/np.cosh(x)
        return 1-tanh*tanh

def tanh(expr):
    return Expression(Tanh,expr) 

class Csch:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        x = sub_expr1.evaluation_at(val_dict)
        return 1/np.sinh(x)
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        # d = -csch(x)*cot(x)
        d = -(1/np.sinh(x)) * (np.cosh(x)/np.sinh(x))
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for csch.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        return -(np.cosh(x)/np.sinh(x))*(1/np.sinh(x))

def csch(expr):
    return Expression(Csch, expr) 

class Sech:
    def evaluation_at(sub_expr1,val_dict):
        x = sub_expr1.evaluation_at(val_dict)
        return 1/np.cosh(x)
    
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        # d = -sech(x)tanh(x)
        d = -(1/np.cosh(x)) * (np.sinh(x)/np.cosh(x))
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict)*d
        else: raise NotImplementedError('higher order derivatives not implemented for sech.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        return -(1/np.cosh(x)) * (np.sinh(x)/np.cosh(x))

def sech(expr):
    return Expression(Sech, expr) 

class Coth:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        x = sub_expr1.evaluation_at(val_dict)
        return np.cosh(x)/np.sinh(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        coth = np.cosh(x)/np.sinh(x)

        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * (1-coth**2)
        else: raise NotImplementedError('higher order derivatives not implemented for cotan.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        coth = np.cosh(x)/np.sinh(x)            
        return 1-coth**2

def coth(expr):
    return Expression(Coth, expr)    

class Arcsin:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        x = sub_expr1.evaluation_at(val_dict)
        return np.arcsin(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        d = 1/np.sqrt(1-x**2)
        #1/sqrt(1-x^2)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for arcsin.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        return 1/np.sqrt(1-x**2)

def arcsin(expr):
    return Expression(Arcsin, expr)
    
class Arccos:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        x = sub_expr1.evaluation_at(val_dict)
        return np.arccos(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        d = 1/np.sqrt(1-x**2)
        #-1/sqrt(1-x^2)
        if order == 1:
            return -sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for arccos.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        return -1/np.sqrt(1-x**2)

def arccos(expr):
    return Expression(Arccos, expr)
    
class Arctan:
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        x = sub_expr1.evaluation_at(val_dict)
        return np.arctan(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        x = sub_expr1.evaluation_at(val_dict)
        d = 1/(1+x**2)
        # d = 1/(1+x**2)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for arctan.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        x = sub_expr1.val
        return 1/(1+x**2)

def arctan(expr):
    return Expression(Arctan, expr)

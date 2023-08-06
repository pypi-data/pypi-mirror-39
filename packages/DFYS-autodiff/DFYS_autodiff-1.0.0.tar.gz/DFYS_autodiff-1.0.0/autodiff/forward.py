"""
This file contains the central data structure and functions related to the
forward mode auto differentiation. 
"""

import numpy as np

class Expression:
    """ 
    This is a class for representing expression.
    It is the super class for variable and constant.
    """
    def __init__(self, ele_func, sub_expr1, sub_expr2=None):
        """ 
        The constructor for VectorFunction class. 
        
        PARAMETERS:
        =======
        ele_func: the function creating this expression
        sub_expr1: variable/constant composing this expression
        sub_expr2: variable/constant composing this expression, set to non
        for unary operations
        """
        self._ele_func  = ele_func
        self._sub_expr1 = sub_expr1
        self._sub_expr2 = sub_expr2
        self.val = None
        self.bder=0
    
    def evaluation_at(self, val_dict):
        """ 
        The wrapper function for individual evaluation_at function of 
        self_ele_func
        
        PARAMETERS:
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        a scalar value 
        """
        # self._sub_expr2 is None implies that self._ele_func is an unary operator
        if self._sub_expr2 is None: 
            return self._ele_func.evaluation_at(
                self._sub_expr1, val_dict)
        
        # self._sub_expr2 not None implies that self._ele_func is a binary operator
        else:
            return self._ele_func.evaluation_at(
                self._sub_expr1, self._sub_expr2, val_dict)
    
    def derivative_at(self, var, val_dict, order=1):
        """ 
        The wrapper function for individual derivative_at function of 
        self_ele_func
        
        PARAMETERS:
        =======
        val_dict: a dictionary containing variable name and values.
        var: variable of interests for derivative calculation
        
        RETURNS
        ======== 
        a scalar value 
        """
        
        if type(var) is tuple: order=len(var)
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
        """
        The wrapper function for individual backderivative_at 
        function of self_ele_func
        
        PARAMETERS:
        =======
        val_dict: a dictionary containing variable name and values. Variables
        in val_dict are of atomic feature and cannot be further decomposed.
        var: variable with respect to which the function calculates derivative   
        
        RETURNS
        ========
        derivative of var with respect to the immediate parent that contain var
        """
        if var is self: return 1.0
        if self._sub_expr2 is None:
            return self._ele_func.backderivative_at(self._sub_expr1,var)
        else:
            return self._ele_func.backderivative_at(self._sub_expr1,
                                                    self._sub_expr2,var)    



    def gradient_at(self, val_dict, returns_dict=False):
        """
        calculate 1st derivative of variables in val_dict using forward mode
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        returns_dict: the format of output
         
        RETURNS
        ========
        derivative of variables in val_dict with respect to the current 
        expression, stored in a dictionary or a 2-D numpy array
        """
        if returns_dict:
            return {v: self.derivative_at(v, val_dict) for v in val_dict.keys()}
        return np.array([self.derivative_at(var, val_dict, order=1) 
                         for var in val_dict.keys()])
    
    def hessian_at(self, val_dict):
        """
        calculate 2nd derivative of variables in val_dict using forward mode
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
         
        RETURNS
        ========
        2nd derivative of variables in val_dict with respect to the current 
        expression, stored in a 2-D list
        """
        return np.array( [ \
                          [self.derivative_at((var1, var2), val_dict, order=2)
                           for var1 in val_dict.keys()]
                          for var2 in val_dict.keys() \
                          ] )
    
    def __neg__(self):
        """ Implement dunder method for neg """
        return Expression(Neg, self)

                
    def __add__(self, another):
        """ Implement dunder method for add """
        if isinstance(another, Expression):
            return Expression(Add, self, another)
        # if the other operand is not an Expression, then it must be a number
        # the number then should be converted to a Constant
        else:
            return Expression(Add, self, Constant(another))
    
    
    def __radd__(self, another):
        """ Implement dunder method for right add """
        if isinstance(another, Expression):
            return Expression(Add, another, self)
        else:
            return Expression(Add, Constant(another), self)
    
    def __sub__(self, another):
        """ Implement dunder method for subtraction """
        if isinstance(another, Expression):
            return Expression(Sub, self, another)
        else:
            return Expression(Sub, self, Constant(another))
    
    def __rsub__(self, another):
        """ Implement dunder method for right subtraction """
        if isinstance(another, Expression):
            return Expression(Sub, another, self)
        else:
            return Expression(Sub, Constant(another), self)
        

    def __mul__(self, another):
        """ Implement dunder method for multiplication """
        if isinstance(another, Expression):
            return Expression(Mul,self,another)
        else:
            return Expression(Mul, self, Constant(another))

    def __rmul__(self, another):
        """ Implement dunder method for right multiplication """
        if isinstance(another, Expression):
            return Expression(Mul,another,self)
        else:
            return Expression(Mul, Constant(another),self)
    
    def __truediv__(self, another):
        """ Implement dunder method for division """
        if isinstance(another, Expression):
            return Expression(Div,self,another)
        else:
            return Expression(Div, self, Constant(another))

    def __rtruediv__(self, another):
        """ Implement dunder method for right division """
        if isinstance(another, Expression):
            return Expression(Div,another,self)
        else:
            return Expression(Div, Constant(another),self)
    
    def __pow__(self,another):
        """ Implement dunder method for power """
        if isinstance(another, Expression):
            return Expression(Pow,self,another)
        else:
            return Expression(Pow, self, Constant(another))
    
    def __rpow__(self,another):
        """ Implement dunder method for right power """
        if isinstance(another, Expression):
            return Expression(Pow,another,self)
        else:
            return Expression(Pow, Constant(another),self)
    
    def __eq__(self, another):
        """ Implement dunder method for equal """
        if not isinstance(another, Expression):
            return False
        return self._ele_func == another._ele_func \
               and self._sub_expr1 == another._sub_expr1 \
               and self._sub_expr2 == another._sub_expr2
               
    def __ne__(self, another):
        """ Implement dunder method not equal """
        return ~self.__eq__(another)
    
    def __hash__(self):
        """ Implement dunder method hash """
        return object.__hash__(self)   

class Variable(Expression):
    """ 
    This is a class for representing variable. 
    """
    def __init__(self):
        """ 
        The constructor for VectorFunction class. 
        It has no parameters: 
        """
        self.val = None
        self.bder = 0
        return
    
    def evaluation_at(self, val_dict):
        """ 
        The function to evaluation the value of variable class
        
        PARAMETERS:
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ======== 
        a scalar value 
        """
        return val_dict[self]
    
    def derivative_at(self, var, val_dict, order=1):
        """ 
        The function calculates derivative of variable class. 
  
        PARAMETERS:
        =======
        val_dict: a dictionary containing variable name and values.
        var: variable whose derivative is the result of this function
        order: default set to 1 for 1st derivative, change to 2 for 
        higher order
        
        RETURNS
        ========
        scalar value  
        """
        if order == 1:
            return 1.0 if var is self else 0.0
        else:
            return 0.0
    
    def __eq__(self, another):
        """ Implement dunder method for equal """
        return another is self
    
    def __ne__(self, another):
        """ Implement dunder method for not equal """
        return ~self.__eq__(another)
    
    def __hash__(self):
        """ Implement dunder method for hash """
        return Expression.__hash__(self) 

class Constant(Expression):
    """ 
    This is a class for representing constant. 
      
    Attributes: 
       val: value of the constant
    """
    def __init__(self, val):
        """ 
        The constructor for VectorFunction class. 
        
        PARAMETERS:
        =======
        val: the value of the constant object
        """
        self.val = val
 
    def evaluation_at(self, val_dict):
        """ 
        The function to evaluation the value of constant class
        
        PARAMETERS:
        ======= 
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        a scalar value 
        """
        return self.val
    
    def derivative_at(self, var, val_dict, order=1):
        """ 
        The function calculates derivative of constant class. 
  
        PARAMETERS:
        ======= 
        val_dict: a dictionary containing variable name and values.
        var: variable whose derivative is the result of this function
        order: default set to 1 for 1st derivative, change to 2 for 
        higher order
        
        RETURNS
        ========
        scalar value  
        """
        return 0.0
    
    def __eq__(self, another):
         """ Implement dunder method for equal """
         if isinstance(another, Constant): return True
         else:                             return False
    
    def __ne__(self, another):
         """ Implement dunder method for not equal """
         return ~self.__eq__(another)
    
    def __hash__(self):
         """ Implement dunder method for hash"""
         return Expression.__hash__(self) 


class VectorFunction:
    """ 
    This is a class for applying operations to a vector of variables. 
      
    Attributes: 
        _exprlist: a list of expressions with respect to which the operations
    are applied 
    """
    def __init__(self, exprlist):
        """ 
        The constructor for VectorFunction class. 
        
        PARAMETERS:
        ======= 
        exprlist: a list of expressions with respect to which the class 
        functions are applied to  
        """
        self._exprlist = exprlist.copy()
    
    def evaluation_at(self, val_dict):
        """ 
        The function to apply evaluation_at to a vector of expressions. 
  
        PARAMETERS:
        ======= 
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        a numpy array containing value of expressions in the self._exprlist. 
        """
        return np.array([expr.evaluation_at(val_dict) 
                        for expr in self._exprlist])
    
    def gradient_at(self, var, val_dict):
        """ 
        The function to apply derivative_at to a vector of expressions. 
  
        PARAMETERS:
        =======
        val_dict: a dictionary containing variable name and values.
        var: variable whose derivative is the result of this function
       
        RETURNS
        ========
        a numpy array containing first derivative of expressions in 
        self._exprlist with respect to var. 
        """
        return np.array([f.derivative_at(var, val_dict) for f in self._exprlist])
    
    def jacobian_at(self, val_dict):
        """ 
        The function to calculate jacobian with respect to atomic variables in 
        val_dict. 
  
        PARAMETERS:
        ======= 
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        a 2-D numpy array containing derivatives of variables in val_dict 
        with resepct to expressions in self._exprlist. 
        """
        return np.array([self.gradient_at(var, val_dict)
                         for var in val_dict.keys()]).transpose()


class Add:
    """ 
    This is a class to wrap up static method related to add operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        """
        Compute addition of sub_expr1 with sub_expr2 using inputs of variable
        values from val_dict.
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sub_expr1 + sub_expr2
        """
        return sub_expr1.evaluation_at(val_dict) + \
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict, order=1):
        return sub_expr1.derivative_at(var, val_dict, order) + \
               sub_expr2.derivative_at(var, val_dict, order)
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression or constant 
        sub_expr2: expression or constant 
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return 1

class Sub:
    """ 
    This is a class to wrap up static method related to sub operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        """
        Compute subtraction of sub_expr2 from sub_expr1 using inputs of variable
        values from val_dict.
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sub_expr1 - sub_expr2
        """
        return sub_expr1.evaluation_at(val_dict) - \
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default set to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return sub_expr1.derivative_at(var, val_dict, order) - \
               sub_expr2.derivative_at(var, val_dict, order)
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression or constant 
        sub_expr2: expression or constant 
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        if var == sub_expr1:
            return 1
        if var == sub_expr2:
            return -1 

class Mul:
    """ 
    This is a class to wrap up static method related to mul operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        """
        Compute multiplication of sub_expr1 with sub_expr2 using inputs 
        of variable values from val_dict.
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sub_expr1 * sub_expr2
        """
        return sub_expr1.evaluation_at(val_dict) *\
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict,order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default set to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
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
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression or constant 
        sub_expr2: expression or constant 
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        if var == sub_expr1:
            return sub_expr2.val
        else:
            return sub_expr1.val
               
class Div:
    """ 
    This is a class to wrap up static method related to div operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        """
        Compute division of sub_expr1 by sub_expr2 using inputs of variable
        values from val_dict.
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sub_expr1 / sub_expr2
        """
        return sub_expr1.evaluation_at(val_dict) /\
               sub_expr2.evaluation_at(val_dict)
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict,order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default set to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
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
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression or constant 
        sub_expr2: expression or constant 
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        if var == sub_expr1:
            return 1/sub_expr2.val
        elif var == sub_expr2:
            return -sub_expr1.val/sub_expr2.val**2
            
class Pow:
    """ 
    This is a class to wrap up static method related to pow operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, sub_expr2, val_dict):
        """
        Compute sub_expr1 to the sub_expr2 power using inputs of variable
        values from val_dict.
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: constant
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sub_expr1 ** sub_expr2
        """
        return np.power(sub_expr1.evaluation_at(val_dict), 
                        sub_expr2.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1, sub_expr2, var, val_dict,order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default set to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
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
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,sub_expr2,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression or constant
        sub_expr2: expression or constant
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        p = sub_expr2.val
        return p*np.power(sub_expr1.val, p-1.0)

def power(expr, p):
    return Expression(Pow, expr, Constant(p))
def sqrt(expr):
    return Expression(Pow, expr, Constant(0.5))


class Exp:
    """ 
    This is a class to wrap up static method related to exp operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, val_dict):
        """
        Compute exponent of sub_expr1 using inputs of variable
        values from val_dict.
    
        INPUTS
        =======
        sub_expr1: expression or constant
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        exponent(sub_expr1)
        """
        return np.exp(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1, var, val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default set to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
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
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression or constant
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return np.exp(sub_expr1.val)
    
def exp(expr):
    return Expression(Exp, expr)

class Log:
    
    @staticmethod
    def evaluation_at(sub_expr1, val_dict):
        return np.log(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1, var, val_dict, order=1):
        if   order == 1:
            return 1 / sub_expr1.evaluation_at(val_dict) * sub_expr1.derivative_at(var, val_dict)
        elif order == 2:
            if type(var) is tuple:
                var1, var2 = var
                f = sub_expr1.evaluation_at(val_dict)
                term1 = 1/f * sub_expr1.derivative_at(var,  val_dict, order=2)
                term2 = -1/f**2 * sub_expr1.derivative_at(var1, val_dict, order=1) \
                            * sub_expr1.derivative_at(var2, val_dict, order=1)
                return term1 + term2
            else:
                return Log.derivative_at(sub_expr1, (var,var), val_dict, order=2)
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    def backderivative_at(sub_expr1,var):
        if sub_expr1 == var:
            return 1/sub_expr1.val

def log(expr):
    return Expression(Log, expr)
        
class Neg:
    """ 
    This is a class to wrap up static method related to neg operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, val_dict):
        """
        Compute negation of sub_expr1 using inputs of variable
        values from val_dict.
    
        INPUTS
        =======
        sub_expr1: expression or constant
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        negate sub_expr1
        """
        return -sub_expr1.evaluation_at(val_dict)
    
    @staticmethod
    def derivative_at(sub_expr1, var, val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default set to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return -sub_expr1.derivative_at(var, val_dict, order)
    
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression or constant 
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return -1


class Sin:
    """ 
    This is a class to wrap up static method related to sin operation
    """
    @staticmethod
    def evaluation_at(sub_expr1, val_dict):
        """
        Compute sin of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sin of sub_expr1 
        """
        return np.sin(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1, var, val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression or constant 
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default set to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
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
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return np.cos(sub_expr1.val)
        
def sin(expr):
    return Expression(Sin, expr)

class Cos:
    """ 
    This is a class to wrap up static method related to cos operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute cos of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        cos sub_expr1
        """
        return np.cos(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression or constant
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
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
        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return -np.sin(sub_expr1.val)
        
def cos(expr):
    return Expression(Cos, expr)
    
class Tan:
    """ 
    This is a class to wrap up static method related to tan operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute tan of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        tan sub_expr1
        """
        return np.tan(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression or constant
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
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

        else: raise NotImplementedError('3rd order or higher derivatives are not implemented.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return 1/(np.cos(sub_expr1.val)**2)

def tan(expr):
    return Expression(Tan, expr)
    
class Cotan:
    """ 
    This is a class to wrap up static method related to cotan operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute cotan of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        cotan sub_expr1
        """
        return 1/np.tan(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1): 
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        if order == 1:
            return -sub_expr1.derivative_at(var, val_dict)/(np.sin(sub_expr1.evaluation_at(val_dict))**2)
        else: raise NotImplementedError('higher order derivatives not implemented for cotan.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return -1/(np.sin(sub_expr1.val)**2)          

def cotan(expr):
    return Expression(Cotan, expr)
    
class Sec:
    """ 
    This is a class to wrap up static method related to sec operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute sec of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sec sub_expr1
        """
        return 1/np.cos(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * \
               np.tan(x) * (1/np.cos(x))
        else: raise NotImplementedError('higher order derivatives not implemented for sec.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x =sub_expr1.val
        return np.tan(x)/np.cos(x)
        
def sec(expr):
    return Expression(Sec, expr) 

class Csc:
    """ 
    This is a class to wrap up static method related to csc operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute csc of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        csc sub_expr1
        """
        return 1/np.sin(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return -sub_expr1.derivative_at(var, val_dict) * \
               (1/np.tan(x)) * (1/np.sin(x))
        else: raise NotImplementedError('higher order derivatives not implemented for csc.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        return -(1/np.tan(x)) * (1/np.sin(x))

def csc(expr):
    return Expression(Csc, expr) 

class Sinh:
    """ 
    This is a class to wrap up static method related to sinh operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute sinh of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sinh sub_expr1
        """
        return np.sinh(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * np.cosh(x)
        else: raise NotImplementedError('higher order derivatives not implemented for sinh.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        return np.cosh(x)

def sinh(expr):
    return Expression(Sinh, expr) 

class Cosh:
    """ 
    This is a class to wrap up static method related to cosh operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute cosh of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        cosh sub_expr1
        """
        return np.cosh(sub_expr1.evaluation_at(val_dict))
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * np.sinh(x)
        else: raise NotImplementedError('higher order derivatives not implemented for cosh.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        return np.sinh(sub_expr1.val)

def cosh(expr):
    return Expression(Cosh, expr) 
    
class Tanh:
    """ 
    This is a class to wrap up static method related to tanh operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute tanh of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        tanh sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        return np.sinh(x)/np.cosh(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        tanh = np.sinh(x)/np.cosh(x)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * (1-tanh*tanh)
        else: raise NotImplementedError('higher order derivatives not implemented for tanh.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        tanh = np.sinh(x)/np.cosh(x)
        return 1-tanh*tanh

def tanh(expr):
    return Expression(Tanh,expr) 

class Csch:
    """ 
    This is a class to wrap up static method related to csch operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute csch of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        csch sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        return 1/np.sinh(x)
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        # d = -csch(x)*cot(x)
        d = -(1/np.sinh(x)) * (np.cosh(x)/np.sinh(x))
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for csch.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        return -(np.cosh(x)/np.sinh(x))*(1/np.sinh(x))

def csch(expr):
    return Expression(Csch, expr) 

class Sech:
    """ 
    This is a class to wrap up static method related to sech operation
    """
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute sech of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        sech sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        return 1/np.cosh(x)
    
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        # d = -sech(x)tanh(x)
        d = -(1/np.cosh(x)) * (np.sinh(x)/np.cosh(x))
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict)*d
        else: raise NotImplementedError('higher order derivatives not implemented for sech.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        return -(1/np.cosh(x)) * (np.sinh(x)/np.cosh(x))

def sech(expr):
    return Expression(Sech, expr) 

class Coth:
    """ 
    This is a class to wrap up static method related to coth operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute coth of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        coth sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        return np.cosh(x)/np.sinh(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        coth = np.cosh(x)/np.sinh(x)

        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * (1-coth**2)
        else: raise NotImplementedError('higher order derivatives not implemented for cotan.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        coth = np.cosh(x)/np.sinh(x)            
        return 1-coth**2

def coth(expr):
    return Expression(Coth, expr)    

class Arcsin:
    """ 
    This is a class to wrap up static method related to arcsin operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute arcsin of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        arcsin sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        return np.arcsin(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        d = 1/np.sqrt(1-x**2)
        #1/sqrt(1-x^2)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for arcsin.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        return 1/np.sqrt(1-x**2)

def arcsin(expr):
    return Expression(Arcsin, expr)
    
class Arccos:
    """ 
    This is a class to wrap up static method related to arccos operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute arccos of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        arccos sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        return np.arccos(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        d = 1/np.sqrt(1-x**2)
        #-1/sqrt(1-x^2)
        if order == 1:
            return -sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for arccos.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        return -1/np.sqrt(1-x**2)

def arccos(expr):
    return Expression(Arccos, expr)
    
class Arctan:
    """ 
    This is a class to wrap up static method related to arctan operation
    """
    @staticmethod
    def evaluation_at(sub_expr1,val_dict):
        """
        Compute arctan of sub_expr1 with inputs of variable values from val_dict.
    
        INPUTS
        =======
        val_dict: a dictionary containing variable name and values.
        
        RETURNS
        ========
        arctan sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        return np.arctan(x)
    
    @staticmethod
    def derivative_at(sub_expr1,var,val_dict, order=1):
        """
        calculate 1st derivative of var using forward mode
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        val_dict: a dictionary containing variable name and values.
        var: variable of interest
        order: default to 1, set to 2 if 2nd derivative is desired
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.evaluation_at(val_dict)
        d = 1/(1+x**2)
        # d = 1/(1+x**2)
        if order == 1:
            return sub_expr1.derivative_at(var, val_dict) * d
        else: raise NotImplementedError('higher order derivatives not implemented for arctan.')
    @staticmethod
    def backderivative_at(sub_expr1,var):
        """
        calculate 1st derivative of var using back propagation
    
        INPUTS
        =======
        sub_expr1: expression whose components include var(or itself be to var)
        var: variable of interest
        
        RETURNS
        ========
        derivative of var with respect to sub_expr1
        """
        x = sub_expr1.val
        return 1/(1+x**2)

def arctan(expr):
    return Expression(Arctan, expr)

def logit(expr):
    return log(expr/(1-expr))

def sigmoid(expr):
    return 1/(1+exp(-expr))
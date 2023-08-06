import math
import numpy as np

class DiffObj(object):
    '''
    All functions will be represented by an instance of this class DiffObj, or by instances of
    classes which inherit from DiffObj (e.g. class Variable, class Constant etc.) DiffObj enforces
    that each class which inherits from it, must implement two functions:

    CLASS FUNCTIONS
    ==================
    The functions get_val and get_der are exposed to the user, that is, a user of our package can
    call these functions.

    (1) get_val:        This is used to evaluate the function represented by a DiffObj instance at
                        a particular point.
                        
    (2) get_der:        This is used to evalate the gradient of the function repreesnted by a DiffObj
                        instance, at a particular point.

    CLASS ATTRIBUTES
    ================
    The attributes are not meant to be used by an end-user of our package, and they are meant for internal
    computation.

    name_list:          A list of strings, where each item in the list represents the variables inside
                        the function represented by this DiffObj. E.g. for f(x,y) = x + y, the name_list
                        for a DiffObj representing f will be ['x', 'y'] (assuming the x.name_list = ['x']
                        and y.name_list = ['y'].
    operator:           A single string representing the "operator". By default, DiffObj assumes that it
                        represents two DiffObj's connected by an binary operator such as 'add'. However, 
                        we use the same definition for unary operators such as negation or cosine.
    operand_list:       A list of two DiffObjs, which together with self.operator, comprise this instance
                        of DiffObj.
    '''
    OVERLOADED_OPERATORS = ['add', 'subtract', 'multiply', 'divide',
            'power', 'neg', 'rdivide', 'rpower']
    def __init__(self, name_list, operator, operand_list):
        self.name_list = name_list
        self.operator = operator
        self.operand_list = operand_list
    def get_val(self, value_dict):
        '''
        INPUT
        ======
        value_dict:     A dictionary, whose keys are strings representing variables which feature
                        in the formula represented by this DiffObj. The values at those keys are
                        the values at which the formula representing this DiffObj will be evaluated.

                        E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                        argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======

        DOCTEST
        ======
        >>> z=x+y
        >>> z.get_val({'x':1,'y':1})
        2


        result:         A floating point number, which equals the evaluation of the function
                        represented by this DiffObj, at the variable values given by val_dict.
        '''
        if self.operator not in DiffObj.OVERLOADED_OPERATORS:
            raise ValueError('{} is not a supported operator'.format(self.operator))
        try:
            op1_val = self.operand_list[0].get_val(value_dict)
        except AttributeError:
            op1_val = self.operand_list[0]
        
        try:
            op2_val = self.operand_list[1].get_val(value_dict)
        except AttributeError:
            op2_val = self.operand_list[1]
        
        if self.operator == 'add':
            return op1_val + op2_val
        elif self.operator == 'subtract':
            return op1_val - op2_val
        elif self.operator == 'multiply':
            return op1_val*op2_val
        elif self.operator == 'divide':
            try:
                result = op1_val/op2_val
                return result
            except:
                raise ValueError('Division by zeros is not allowed')
        elif self.operator == 'rdivide':
            try:
                result = op2_val/op1_val
                return result
            except:
                raise ValueError('Division by zeros is not allowed')
        elif self.operator == 'power':
            return op1_val**op2_val
        elif self.operator == 'rpower':
            return op2_val**op1_val
        elif self.operator == 'neg':
            return -op1_val

    def get_der(self, value_dict, with_respect_to=None):
        '''
        INPUT
        ======
        value_dict:         A dictionary, whose keys are strings representing variables which feature
                            in the formula represented by this DiffObj. The values at those keys are
                            the values at which the gradient of formula representing this DiffObj will 
                            be evaluated.
                            
                            E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                            argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======
        result:             A dictionary, whose keys are strings representing variables which feature 
                            in the formula represented by this DiffObj. The value associated withe each
                            key is a floating point number which is the partial derivative of this DiffObj 
                            with respect to that variable.
        with_respect_to:    A list of strings representing variables, with respect to which we want the 
                            gradient of this DifObj. By default, if this list is not provided, then the
                            gradient with respect to all variables featuring in the DiffObj is returned.

        DOCTEST
        ======
        >>> z=x+y
        >>> z.get_der({'x':0,'y':0})
        {'y': 1, 'x': 1}

        '''
        if not with_respect_to: with_respect_to = self.name_list
        df = {}
        op1, op2 = self.operand_list[0], self.operand_list[1]
        try:
            op1_val = op1.get_val(value_dict)
        except AttributeError:
            op1_val = op1
        try:
            op2_val = op2.get_val(value_dict)
        except AttributeError:
            op2_val = op2

        if self.operator == 'add':
            for w in with_respect_to:
                try:
                    op2_der = op2.get_der(value_dict, [w])[w]
                except AttributeError:
                    op2_der = 0
                dw = op1.get_der(value_dict, [w])[w] + op2_der
                df[w] = dw
        elif self.operator == 'subtract':
            for w in with_respect_to:
                try:
                    op2_der = op2.get_der(value_dict, [w])[w]
                except AttributeError:
                    op2_der = 0 
                dw = op1.get_der(value_dict, [w])[w] - op2_der
                df[w] = dw
        elif self.operator == 'multiply':
            for w in with_respect_to:
                try:
                    op2_der = op2.get_der(value_dict, [w])[w]
                except AttributeError:
                    op2_der = 0  
                dw = op1.get_der(value_dict, [w])[w]*op2_val + op2_der*op1_val
                df[w] = dw
        elif self.operator == 'divide':
            try:
                one_by_op2_val = 1.0/op2_val
            except:
                raise ValueError('Division by zero is not allowed')
            for w in with_respect_to:
                try:
                    op2_der = op2.get_der(value_dict, [w])[w]
                except AttributeError:
                    op2_der = 0  
                try:
                    op1_der = op1.get_der(value_dict, [w])[w]
                except AttributeError:
                    op1_der = 0  
                dw = (op2_val*op1_der - op1_val*op2_der)/(op2_val**2)
                df[w] = dw
        elif self.operator == 'rdivide':
            try:
                one_by_op1_val = 1.0/op1_val
            except:
                raise ValueError('Division by zero is not allowed')
            for w in with_respect_to:
                try:
                    op2_der = op2.get_der(value_dict, [w])[w]
                except AttributeError:
                    op2_der = 0  
                try:
                    op1_der = op1.get_der(value_dict, [w])[w]
                except AttributeError:
                    op1_der = 0  
                dw = (op1_val*op2_der - op2_val*op1_der)/(op1_val**2)
                df[w] = dw
        elif self.operator == 'power':
            for w in with_respect_to:
                try:
                    op2_der = op2.get_der(value_dict, [w])[w]
                except AttributeError:
                    op2_der = 0  
                try:
                    op1_der = op1.get_der(value_dict, [w])[w]
                except AttributeError:
                    op1_der = 0  
                if op1_val < 0:
                    if (op2_val/1.0).is_integer() and op2_der == 0:
                        func_val = op1_val**op2_val
                        dw = func_val*op2_val/op1_val*op1_der
                    else:
                        raise ValueError('Base in Exponentiation should be positive.')
                else:
                    func_val = op1_val**op2_val
                    dw = func_val*((op2_val/op1_val)*op1_der + math.log(op1_val)*op2_der)
                df[w] = dw
        elif self.operator == 'rpower':
            for w in with_respect_to:
                try:
                    op2_der = op2.get_der(value_dict, [w])[w]
                except AttributeError:
                    op2_der = 0  
                try:
                    op1_der = op1.get_der(value_dict, [w])[w]
                except AttributeError:
                    op1_der = 0  
                if op2_val < 0:
                    if (op1_val/1.0).is_integer() and op1_der == 0:
                        func_val = op2_val**op1_val
                        dw = func_val*op1_val/op2_val*op2_der
                    else:
                        raise ValueError('Base in Exponentiation should be positive.')
                else:
                    func_val = op2_val**op1_val
                    dw = func_val*((op1_val/op2_val)*op2_der + math.log(op2_val)*op1_der)
                df[w] = dw
        elif self.operator == 'neg':
            for w in with_respect_to:
                dw = -op1.get_der(value_dict, [w])[w]
                df[w] = dw
        if len(df) == 0: df = {'' : 0}
        return df

    def getBinaryOperator(self, other, operator_name):
        try:
            this_name_list = self.name_list
        except AttributeError:
            this_name_list = []
        try:
            other_name_list = other.name_list
        except AttributeError:
            other_name_list = []
        if operator_name == 'neg': other_name_list = []
        return DiffObj(this_name_list + other_name_list,
                operator_name, [self, other])

    def __neg__(self):
        '''
        Overloads negation for objects of type DiffObj.
        INPUT
        =====
        Takes a single AutoDiff object (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object

        -a

        which uses our __neg__ method.
        a.__neg__()
        
        OUTPUT
        ======
        result:         A DiffObj, for which DiffObj.operator_name is 'neg', DiffObj.operand_list 
                        contains [a,a], and DiffObj.name_list is same as the original name_list of a.

        DOCTEST
        ======
        >>> z=-y
        >>> z.get_val({'x':3,'y':2})
        -2
        >>> z.get_der({'x':3,'y':2})
        {'y': -1}
                        
        '''
        return self.getBinaryOperator(self, 'neg')
    def __add__(self, other):
        '''
        Overloads the add operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):
    
        a = AutoDiff object
        b = AutoDiff object

        a + b

        which uses our __add__ method:

        a.__add__(b)

        OUTPUT
        ======
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'add', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the sum
        DiffObj.operand_list[0].get_val(val_dict) + DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the sum of the operands after
        their values are evaluated individually with respect to their own value dictionaries.

        DOCTEST
        ======
        >>> z=x+y
        >>> z.get_val({'x':3,'y':2})
        5
        >>> z.get_der({'x':3,'y':2})
        {'y': 1, 'x': 1}

        '''


        return self.getBinaryOperator(other, 'add')
    def __sub__(self, other):
        '''
        Overloads the subtract operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object
        b = AutoDiff object

        a - b

        which uses our __sub__ method:

        a.__sub__(b)

        OUTPUT
        ======
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'subtract', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the difference
        DiffObj.operand_list[0].get_val(val_dict) - DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the difference of the operands after
        their values are evaluated individually with respect to their own value dictionaries.

        DOCTEST
        ======
        >>> z=x-y
        >>> z.get_val({'x':3,'y':2})
        1
        >>> z.get_der({'x':3,'y':2})
        {'y': -1, 'x': 1}

        '''
        return self.getBinaryOperator(other, 'subtract')

    def __rsub__(self, other):
        return -self + other
    
    def __mul__(self, other):
        '''
        Overloads the multiply operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object
        b = AutoDiff object

        a * b

        which uses our __mul__ method:

        a.__mul__(b)

        OUTPUT
        ======  
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'multiply', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the product
        DiffObj.operand_list[0].get_val(val_dict) * DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the product of the operands after
        their values are evaluated individually with respect to their own value dictionaries.


        DOCTEST
        ======
        >>> z=x*y
        >>> z.get_val({'x':3,'y':2})
        6
        >>> z.get_der({'x':3,'y':2})
        {'y': 3, 'x': 2}

        '''
        return self.getBinaryOperator(other, 'multiply')

    def __truediv__(self, other):
        '''
        Overloads the division operator such that it works for DiffObj objects.

        INPUT
        =====
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, AutoDiff.Variable, or AutoDiff.MathOps):

        a = AutoDiff object
        b = AutoDiff object

        a / b

        which uses our __truediv__ method:

        a.__truediv__(b)

        OUTPUT
        ======
        Returns a DiffObj, where the DiffObj.name_list is the concatination of a.name_list and b.name_list,
        DiffObj.operator_name is 'divide', and DiffObj.operand_list is [a,b].

        When get_val is called on the resulting DiffObj, as in DiffObj.get_val(val_dict), the division
        DiffObj.operand_list[0].get_val(val_dict) / DiffObj.operand_list[1].get_val(val_dict) is returned.
        In other words, DiffObj.get_val(val_dict) returns the division of the operands after
        their values are evaluated individually with respect to their own value dictionaries.

        DOCTEST
        ======
        >>> z=x/y
        >>> z.get_val({'x':3,'y':2})
        1
        >>> z.get_der({'x':3,'y':2})
        {'y': -1, 'x': 0}
        >>> 


        '''
        return self.getBinaryOperator(other, 'divide')

    
    def __rtruediv__(self, other): 
        return self.getBinaryOperator(other, 'rdivide')

    def __div__(self,other):
        return self.__truediv__(other)
        '''
        __div__ for python2 support


        DOCTEST
        ======
        >>> z=x/y
        >>> z.get_val({'x':3,'y':2})
        1
        >>> z.get_der({'x':3,'y':2})
        {'y': -1, 'x': 0}
        >>> 

        '''

    def __pow__(self, other):
        '''
        Overloads the power operator such that it works for DiffObj objects.
        INPUT
        =====
        self, other:        Two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Constant, 
                            AutoDiff.Variable, or AutoDiff.MathOps

        Example Usage:
        If a and b are two AutoDiff Objects. Then a**b will use our __pow__ method.


        OUTPUT
        ======
        result:             A DiffObj where DiffObj.name_list is the concatenation of a.name_list and 
                            b.name_list, DiffObj.operator_name is 'power', and DiffObj.operand_list is
                            [a,b].

        DOCTEST
        ======
        >>> z=x*y
        >>> z.get_val({'x':3,'y':2})
        6
        >>> z.get_der({'x':3,'y':2})
        {'y': 3, 'x': 2}
        '''
        return self.getBinaryOperator(other, 'power')

    def __rpow__(self, other):
        return self.getBinaryOperator(other, 'rpower')

    __radd__ = __add__
    __rmul__ = __mul__
    
   
class Variable(DiffObj):
    '''
    All variables inside a function whose derivative and value a user wants to calculate, 
    will be instances of the Variable class, which inherits from DiffObj and implements
    get_val and get_der

    CLASS ATTRIBUTES
    ================
    var_name:           A string, which is unique to this Variable instance.
                        E.g. x = Variable('x')

    CLASS FUNCTIONS
    ===============
    This implements get_val and get_der, a description of which is provided in the 
    Super-class DiffObj.

    '''
    def __init__(self, var_name):
        self.var_name = var_name
        super(Variable, self).__init__([var_name], None, None)
    
    def get_val(self, value_dict):
        if self.var_name not in value_dict:
            raise ValueError('You have not provided a value for {}'.format(self.var_name))
        try:
            temp = value_dict[self.var_name] + 0.0
        except:
            raise TypeError('Only integer and float types are accepted as values.')
        return value_dict[self.var_name]
    
    def get_der(self, value_dict, with_respect_to=None):
        if not with_respect_to:
            return {self.var_name : 1}
        else:
            der_dict = {}
            for w in with_respect_to:
                der_dict[w] = int(w == self.var_name)
            return der_dict

class Constant(DiffObj):
    '''
    All constants inside a function whose derivative and value a user wants to calculate,
    will be instances of the Constant class, which inherits from DiffObj and implements
    get_val and get_der

    CLASS ATTRIBUTES
    ================
    const_name:         A string, which is unique to this Constant instance.
    const_val:          An int or float number, which will be the value assigned to this instance.

                        E.g. c = Constant('c', 10.0)

    CLASS FUNCTIONS
    ===============
    This implements get_val and get_der, a description of which is provided in the
    Super-class DiffObj. As expected, get_val simply returns self.const_val while
    get_der will return 0.
    '''
    def __init__(self, const_name, const_val):
        super(Constant, self).__init__([], None, None)
        self.const_name = const_name
        self.const_val = const_val
        self.name_list = []
    def get_val(self, value_dict):
        return self.const_val
    def get_der(self, value_dict, with_respect_to=None):
        if not with_respect_to:
            return {'' : 0}
        der_dict = {}
        for w in with_respect_to:
            der_dict[w] = 0
        return der_dict


class VectorFunction(DiffObj):
    '''
    Temporary vector function for use in root_finder.py until code supports vector valued functions
    ''' 
    def __init__(self, list_of_functions):
        self.list_of_functions = list_of_functions
        name_list = []
        for f in self.list_of_functions:
            name_list = name_list+f.name_list
        name_list = list(set(name_list))
        super(VectorFunction, self).__init__(name_list, None, None)


    def get_val(self, val_dict):
        return [f.get_val(val_dict) for f in self.list_of_functions]  
    def get_der(self, val_dict, with_respect_to=None):
        return [f.get_der(val_dict, with_respect_to) for f in self.list_of_functions] 

    # returns 2d array from list of dictionarys
    def dict_list_to_array(self,dict_list):
        arr = []
        for f_dict in dict_list:
            row = []
            for var in self.name_list:
                row.append(f_dict[var])
            arr.append(row)        
        return arr



class MathOps(DiffObj):
    '''
    This class inherits from the DiffObj class. It implements non-elementary unary functions 
    including: sin, cos, tan, log, exp.

    INSTANTIATION
    ===============
    If a is of type DiffObj, then the invoking the constructor as follows will return an 
    object b of type MathOps:

    b = MathOps.sin(a)

    CLASS ATTRIBUTES
    ================
    The attributes are not meant to be used by an end-user of our package, and they are meant for internal
    computation.

    name_list:          A list of strings, where each item in the list represents the variables inside
                        the function represented by this DiffObj. E.g. for f(x,y) = x + y, the name_list
                        for a DiffObj representing f will be ['x', 'y'] (assuming the x.name_list = ['x']
                        and y.name_list = ['y'].
    operator:           A string, such as 'sin' or 'log', which represents one of the unary math operators
                        implemented by this class.
    operand_list:       A list of length 1 containing the DiffObj which the user has passed as an argument
                        to one of the classmethods of MathOps.

    '''
    def __init__(self, name_list, operator, operand):
        super(MathOps, self).__init__(name_list, 
                operator, operand)
    @classmethod
    def getUnaryOperator(cls, operator, obj):
        try:
            name_list = obj.name_list
            return MathOps(name_list, operator, [obj]) 
        except:
            raise TypeError('Only objects of type DiffObj are permitted.')
    @classmethod
    def sin(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the sine function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this sin function.

        DOCTEST
        ======
        >>> z=MathOps.sin(x)
        >>> z.get_val({'x':math.pi})
        1.2246467991473532e-16
        >>> z.get_der({'x':math.pi})
        {'x': -1.0}
        
        '''
        return MathOps.getUnaryOperator('sin', obj)
    @classmethod
    def cos(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the cos function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'cos' and whose operand is
                    the DiffObj on which the user had called this cos function.
        DOCTEST
        ======
        
        >>> z=MathOps.cos(x)
        >>> z.get_val({'x':math.pi})
        -1.0
        >>> z.get_der({'x':math.pi})
        {'x': -1.2246467991473532e-16}
        '''
        return MathOps.getUnaryOperator('cos', obj)
    @classmethod
    def tan(cls,obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the tan function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this tan function.

        DOCTEST
        ======
        
        >>> z=MathOps.tan(x)
        >>> z.get_val({'x':0})
        0.0
        >>> z.get_der({'x':0})
        {'x': 1.0}
        '''

        return MathOps.getUnaryOperator('tan', obj)
    @classmethod
    def log(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural log function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this log function.

        DOCTEST
        ======
        >>> z=MathOps.log(x)
        >>> z.get_val({'x':1})
        0.0
        >>> z.get_der({'x':1})
        {'x': 1.0}
        '''

        return MathOps.getUnaryOperator('log', obj)
    @classmethod
    def exp(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural exponentiation function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sin' and whose operand is
                    the DiffObj on which the user had called this exp function.
        >>> z=MathOps.exp(x)
        >>> z.get_val({'x':0})
        1.0
        >>> z.get_der({'x':0})
        {'x': 1.0}
        '''

        return MathOps.getUnaryOperator('exp', obj)
    def get_val(self, value_dict):
        '''
        INPUT
        ======
        value_dict:     A dictionary, whose keys are strings representing variables which feature
                        in the formula represented by this DiffObj. The values at those keys are
                        the values at which the formula representing this DiffObj will be evaluated.

                        E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                        argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======
        result:         A floating point number, which equals the evaluation of the function
                        represented by this DiffObj, at the variable values given by val_dict.
        '''
 
        operand_val = self.operand_list[0].get_val(value_dict)
        if self.operator == 'sin':
            return math.sin(operand_val)
        elif self.operator == 'cos':
            return math.cos(operand_val)
        elif self.operator == 'tan':
            result = math.tan(operand_val)
            return result
        elif self.operator == 'log':
            try:
                result = math.log(operand_val)
                return result
            except:
                raise ValueError('Only positive values are permitted with log.')
        elif self.operator == 'exp':
            result = math.exp(operand_val)
            return result

    def get_der(self, value_dict, with_respect_to=None):
        '''
        INPUT
        ======
        value_dict:         A dictionary, whose keys are strings representing variables which feature
                            in the formula represented by this DiffObj. The values at those keys are
                            the values at which the gradient of formula representing this DiffObj will 
                            be evaluated.
                            
                            E.g. For a DiffObj which represents the function f(x,y) = x + y, the value_dict
                            argument may look like value_dict = {'x': 10, 'y': 5}
        OUTPUT
        ======
        result:             A dictionary, whose keys are strings representing variables which feature 
                            in the formula represented by this DiffObj. The value associated withe each
                            key is a floating point number which is the partial derivative of this DiffObj 
                            with respect to that variable.
        with_respect_to:    A list of strings representing variables, with respect to which we want the 
                            gradient of this DifObj. By default, if this list is not provided, then the
                            gradient with respect to all variables featuring in the DiffObj is returned.
        '''
 
        if not with_respect_to: with_respect_to = self.name_list
        df = {}
        op1 = self.operand_list[0]
        if self.operator == 'sin':
            for w in with_respect_to:
                dw = math.cos(op1.get_val(value_dict))*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'cos':
            for w in with_respect_to:
                dw = -math.sin(op1.get_val(value_dict))*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'tan':
            sec_x = 1.0/math.cos(op1.get_val(value_dict))
            for w in with_respect_to:
                dw = (sec_x**2)*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'log':
            try:
                one_by_var = 1.0/op1.get_val(value_dict)
            except:
                raise ValueError('Log cannot be evaluated at 0.')
            for w in with_respect_to:
                dw = one_by_var*op1.get_der(value_dict, [w])[w]
                df[w] = dw
        elif self.operator == 'exp':
            func_val = math.exp(op1.get_val(value_dict))
            for w in with_respect_to:
                dw = func_val*op1.get_der(value_dict, [w])[w]
                df[w] = dw

        if len(df) == 0: df = {'' : 0}
        return df

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'x': Variable('x'),'y':Variable('y')})

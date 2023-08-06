import math
import numpy as np

class DiffObj(object):
    '''
    All functions will be represented by an instance of this class DiffObj, or by instances of
    classes which inherit from DiffObj (e.g. class Variable etc.) DiffObj enforces
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
    def __init__(self, name_list, operator, operand_list, default_val=None):
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
        Takes a single AutoDiff object (can be of type AutoDiff.DiffObj, AutoDiff.Variable, or AutoDiff.MathOps):
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
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Variable, or AutoDiff.MathOps):
    
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
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Variable, or AutoDiff.MathOps):
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
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Variable, or AutoDiff.MathOps):
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
        Takes two AutoDiff objects (can be of type AutoDiff.DiffObj, AutoDiff.Variable, or AutoDiff.MathOps):
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

    def __pow__(self, other):
        '''
        Overloads the power operator such that it works for DiffObj objects.
        INPUT
        =====
        self, other:        Two AutoDiff objects (can be of type AutoDiff.DiffObj, 
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

    def get_dict_val(self):
        '''
        Returns the default value dictionary. Used to determine equality between DiffObj objects that have
        default variable values specified.  
        INPUT
        =====
        self:        Takes a AutoDiff object of type AutoDiff.DiffObj.
        Example Usage:
        Will be called only in (in)equality tests. For example, if a and b are AutoDiff.DiffObj 
        objects, a==b will call a.__eq__(b), which in turn will call a.get_dict_val() and b.get_dict_val().
        The derivative and value of a and b with then be calculated at their default variable values.
        OUTPUT
        ======
        result:             A dictionary, where each key is a value in name_list, and each value is the default
                            value that was supplied by the user.
        DOCTEST
        ======
        >>> x = Variable('x',5)
        >>> y = Variable('y',2)
        >>> f = x+y
        >>> f.get_dict_val()
        {'x': 5, 'y': 2}
        '''
        default_val_dict = {}
        val_list = self.name_list
        val_list = list(set(val_list))

        tree = self.operand_list
        current_tree = tree
        next_tree = []
        while True:
            if len(current_tree) == 0:

                # didnt find key for all variables 
                if not len(list(default_val_dict.keys())) == len(val_list):
                    raise ValueError("Missing {} default value(s).".format(len(val_list) -len(list(default_val_dict.keys()))))
                else:
                    return default_val_dict
            for item in current_tree:

                if isinstance(item,Variable):

                    # each variable should have only one default value
                    if item.var_name in default_val_dict:
                        if not default_val_dict[item.var_name] == item.default_val:
                            raise ValueError("Repeated key: ", item.var_name)
                    default_val_dict[item.var_name]=item.default_val
                elif isinstance(item,DiffObj):
                    for operand in item.operand_list:
                        next_tree.append(operand)
                elif isinstance(item, int):
                    pass
                else:
                    raise ValueError("Can't get default dict if no default values provided.")

            current_tree = next_tree
            next_tree = []
        raise ValueError("Impossible")


    '''
    EQUALITY OPERATOR BEHAVIOR
    ==========================
    __eq__      Returns True if DiffObj have the same derivative and value at their respective default
                Variable values. Variables must also have the same names. False otherwise.
    __ne__      Returns the boolean negation of __eq__.
    __gt__      Returns true if the left DiffObj value is greater than the right DiffObj value at their
                respective default Variable values. False otherwise. 
    __lt__      Returns true if the left DiffObj value is less than the right DiffObj value at their
                respective default Variable values. False otherwise. 
    __ge__      Returns true if the left DiffObj value is greater than or equal to the right DiffObj 
                value at their respective default Variable values. False otherwise. 
    __le__      Returns true if the left DiffObj value is less than or equal to the right DiffObj value 
                at their respective default Variable values. False otherwise. 
    DOCTEST
    =======
    >>> x = Variable('x',5)
    >>> y = Variable('y',3)
    >>> z = Variable('z',5)
    >>> f = 4*x
    >>> g = 8*y
    >>> h = 4*x
    >>> j = 4*z
    >>> f == g
    False
    >>> f == h
    True
    >>> f == j
    False
    >>> f == x
    False
    >>> f > g
    False
    >>> f < g
    True
    >>> h <= f
    True
    >>> g >= h
    True
    '''
    def __eq__(self,other):
        if not (type(self)==type(other)):
            return False 
        dict_val_self = self.get_dict_val()
        dict_val_other = other.get_dict_val()
        return (self.get_val(dict_val_self) == other.get_val(dict_val_other) and 
            self.get_der(dict_val_self) == other.get_der(dict_val_other))

    def __ne__(self,other):
        return not self.__eq__(other)

    def __gt__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) > other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __lt__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) < other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __ge__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) >= other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __le__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) <= other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))


   
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
    def __init__(self, var_name, default_val=None):
        self.var_name = var_name
        self.default_val = default_val
        super(Variable, self).__init__([var_name], None, {var_name: default_val})
    
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


    '''
    EQUALITY OPERATOR BEHAVIOR
    ==========================
    __eq__      Returns True if Variables have the same default values and variable names. 
                False otherwise.
    __ne__      Returns the boolean negation of __eq__.
    __gt__      Returns true if the left Variable default value is greater than the right Variable 
                default value. False otherwise. 
    __lt__      Returns true if the left Variable default value is less than the right Variable 
                default value. False otherwise. 
    __ge__      Returns true if the left Variable default value is greater than or equal to the 
                right Variable default value. False otherwise. 
    __le__      Returns true if the left Variable default value is less than or equal to the 
                right Variable default value. False otherwise. 
    DOCTEST
    =======
    >>> w = Variable('x',5)
    >>> x = Variable('x',5)
    >>> y = Variable('y',3)
    >>> z = Variable('z',5)
    >>> w == x
    True
    >>> x == z
    False
    >>> x == y
    False
    >>> x > y
    True
    >>> x < w
    False
    >>> x <= z
    True
    >>> x >= y
    True
    '''

    def __eq__(self,other):
        if not (type(self)==type(other)):
            return False 
        return (self.default_val == other.default_val and
            self.var_name == other.var_name)

    def __ne__(self,other):
        return not self.__eq__(other)

    def __le__(self,other):
        if (type(self)==type(other)):
            return self.default_val <= other.default_val
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __ge__(self,other):
        if (type(self)==type(other)):
            return self.default_val >= other.default_val
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __lt__(self,other):
        if (type(self)==type(other)):
            return self.default_val < other.default_val
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __gt__(self,other):
        if (type(self)==type(other)):
            return self.default_val > other.default_val
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

class VectorFunction(DiffObj):
    '''
    Vector function for use in root_finder.py.
    ''' 
    def __init__(self, list_of_functions):
        self.list_of_functions = list_of_functions
        name_list = []
        for f in self.list_of_functions:
            try:
                name_list = name_list+f.name_list
            # user added a constant to the vector   
            except:
                pass
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

    '''
    EQUALITY OPERATOR BEHAVIOR
    ==========================
    __eq__      Returns True if Vector objects have the same derivative and value at their respective default
                Variable values. Variables must also have the same names. False otherwise.
    __ne__      Returns the boolean negation of __eq__.
    __gt__      Returns true if the left Vector object value is greater than the right MathOps object value at their
                respective default Variable values in all dimensions. False otherwise. 
    __lt__      Returns true if the left Vector object value is less than the right MathOps object value at their
                respective default Variable values in all dimensions. False otherwise. 
    __ge__      Returns true if the left Vector object value is greater than or equal to the right MathOps object 
                value at their respective default Variable values in all dimensions. False otherwise. 
    __le__      Returns true if the left Vector object value is less than or equal to the right MathOps object value 
                at their respective default Variable values in all dimensions. False otherwise. 
    '''
    def __eq__(self,other):
        if not (type(self)==type(other)):
            return False 
        for i,func in enumerate(self.list_of_functions):
            if not other.list_of_functions[i] == func:
                return False 
        return True

    def __ne__(self,other):
        if (type(self)==type(other)):
            return not self.__eq__(other)
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __le__(self,other):
        if (type(self)==type(other)):
            for i,func in enumerate(self.list_of_functions):
                if func > other.list_of_functions[i]:
                    return False 
            return True
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __ge__(self,other):
        if (type(self)==type(other)):
            for i,func in enumerate(self.list_of_functions):
                if func < other.list_of_functions[i]:
                    return False 
            return True
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __lt__(self,other):
        if (type(self)==type(other)):
            for i,func in enumerate(self.list_of_functions):
                if func >= other.list_of_functions[i]:
                    return False 
            return True 
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __gt__(self,other):
        if (type(self)==type(other)):
            for i,func in enumerate(self.list_of_functions):
                if func <= other.list_of_functions[i]:
                    return False 
            return True 
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

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
        result:     A DiffObj, whose operator is 'tan' and whose operand is
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
    def arcsin(cls,obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the arcsin function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'arcsin' and whose operand is
                    the DiffObj on which the user had called this arcsin function.
        DOCTEST
        ======
        
        >>> z=MathOps.arcsin(x)
        >>> z.get_val({'x':0})
        0.0
        >>> z.get_der({'x':0})
        {'x': 1.0}
        '''
        return MathOps.getUnaryOperator('arcsin', obj)

    @classmethod
    def arccos(cls,obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the arccos function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'arccos' and whose operand is
                    the DiffObj on which the user had called this arccos function.
        DOCTEST
        ======
        
        >>> z=MathOps.arccos(x)
        >>> z.get_val({'x':0})
        math.pi/2
        >>> z.get_der({'x':0})
        {'x': -1.0}
        '''
        return MathOps.getUnaryOperator('arccos', obj)


    @classmethod
    def arctan(cls,obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the arctan function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'arctan' and whose operand is
                    the DiffObj on which the user had called this arctan function.
        DOCTEST
        ======
        
        >>> z=MathOps.arctan(x)
        >>> z.get_val({'x':0.0})
        0.0
        >>> z.get_der({'x':0.0})
        {'x': 1.0}
        '''
        return MathOps.getUnaryOperator('arctan', obj)


    @classmethod
    def sinh(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the hyperbolic sine function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'hsin' and whose operand is
                    the DiffObj on which the user had called this hyperbolic sin function.
        DOCTEST
        ======
        >>> z=MathOps.hsin(x)
        >>> z.get_val({'x':math.pi})
        1.2246467991473532e-16
        >>> z.get_der({'x':math.pi})
        {'x': -1.0}
        
        '''
        return MathOps.getUnaryOperator('sinh', obj)
    @classmethod
    def cosh(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the hyperbolic cos function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'hcos' and whose operand is
                    the DiffObj on which the user had called this hyperbolic cos function.
        DOCTEST
        ======
        
        >>> z=MathOps.cos(x)
        >>> z.get_val({'x':math.pi})
        -1.0
        >>> z.get_der({'x':math.pi})
        {'x': -1.2246467991473532e-16}
        '''
        return MathOps.getUnaryOperator('cosh', obj)
    @classmethod
    def tanh(cls,obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the hyperbolic tan function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'tanh' and whose operand is
                    the DiffObj on which the user had called this hyperbolic tan function.
        DOCTEST
        ======
        
        >>> z=MathOps.tanh(x)
        >>> z.get_val({'x':0})
        0.0
        >>> z.get_der({'x':0})
        {'x': 1.0}
        '''

        return MathOps.getUnaryOperator('tanh', obj)

    @classmethod
    def loge(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural log function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'log' and whose operand is
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
    def log(cls, obj, base=None):

        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural log function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'log' and whose operand is
                    the DiffObj on which the user had called this log function.

        DOCTEST
        ======
        >>> z=MathOps.log(x)
        >>> z.get_val({'x':1})
        0.0
        >>> z.get_der({'x':1})
        {'x': 1.0}
        '''

        natural_log = MathOps.getUnaryOperator('log', obj)
        if base is None:
            return natural_log
        else:
            if base <= 0:
                raise ValueError('Base needs to be a strictly positive real number.')
            else:
                return natural_log/math.log(base)
    
    
    @classmethod
    def exp(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural exponentiation function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'exp' and whose operand is
                    the DiffObj on which the user had called this exp function.
        >>> z=MathOps.exp(x)
        >>> z.get_val({'x':0})
        1.0
        >>> z.get_der({'x':0})
        {'x': 1.0}
        '''

        return MathOps.getUnaryOperator('exp', obj)

    @classmethod
    def logistic(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural exponentiation function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'exp' and whose operand is
                    the DiffObj on which the user had called this exp function.
        >>> z=MathOps.logistic(x)
        >>> z.get_val({'x':0})
        0.5
        >>> z.get_der({'x':0})
        {'x': 0.25}
        '''

        return 1/(1 + MathOps.getUnaryOperator('exp', -obj))



    @classmethod
    def sqrt(cls, obj):
        '''
        INPUT
        =====
        obj:        An object of type DiffObj, on which the user wants to
                    apply the natural exponentiation function.
        OUTPUT
        ======
        result:     A DiffObj, whose operator is 'sqrt' and whose operand is
                    the DiffObj on which the user had called this exp function.
        >>> z=MathOps.sqrt(x)
        >>> z.get_val({'x':4})
        2.0
        >>> z.get_der({'x':4})
        {'x': 8.0}
        '''

        return MathOps.getUnaryOperator('sqrt', obj)
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
        elif self.operator == 'arcsin':
            result = np.arcsin(operand_val)
            return result
        elif self.operator == 'arccos':
            result = np.arccos(operand_val)
            return result
        elif self.operator == 'arctan':
            result = np.arctan(operand_val)
            return result
        if self.operator == 'sinh':
            return np.sinh(operand_val)
        elif self.operator == 'cosh':
            return np.cosh(operand_val)
        elif self.operator == 'tanh':
            result = np.tanh(operand_val)
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
        elif self.operator == 'sqrt':  
            try:
                result = math.sqrt(operand_val)
                return result
            except:
                raise ValueError('Only positive values are permitted with square root.')

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

        elif self.operator == 'arcsin':
            for w in with_respect_to:
                try:
                    dw = (1/math.sqrt(1 - op1.get_val(value_dict)**2))* op1.get_der(value_dict, [w])[w]
                    df[w] = dw
                except:
                    raise ValueError('arcsin cannot be evaluated at 1,-1.')
        elif self.operator == 'arccos':
            for w in with_respect_to:
                try:
                    dw = -(1/math.sqrt(1 - op1.get_val(value_dict)**2))* op1.get_der(value_dict, [w])[w]
                    df[w] = dw
                except:
                    raise ValueError('arccos cannot be evaluated at 1,-1.')
        elif self.operator == 'arctan':
            for w in with_respect_to:
                dw = (1/(1 + op1.get_val(value_dict)**2))* op1.get_der(value_dict, [w])[w]
                df[w] = dw

        elif self.operator == 'sinh':
            for w in with_respect_to:
                dw = np.cosh(op1.get_val(value_dict))* op1.get_der(value_dict, [w])[w]
                df[w] = dw

        elif self.operator == 'cosh':
            for w in with_respect_to:
                dw = np.sinh(op1.get_val(value_dict))* op1.get_der(value_dict, [w])[w]
                df[w] = dw

        elif self.operator == 'tanh':
            for w in with_respect_to:
                dw = (1/(np.cosh(op1.get_val(value_dict))**2))* op1.get_der(value_dict, [w])[w]
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
        elif self.operator == 'sqrt':
            try:
                func_val = math.sqrt(op1.get_val(value_dict))
                for w in with_respect_to:
                    dw = ((1/2.0)* (op1.get_val(value_dict)**(-1/2.0))*(op1.get_der(value_dict, [w])[w]))
                    df[w] = dw
            except:
                raise ValueError('Square root cannot be evaluated on negative numbers.')
        if len(df) == 0: df = {'' : 0}
        return df

    '''
    EQUALITY OPERATOR BEHAVIOR
    ==========================
    __eq__      Returns True if MathOps objects have the same derivative and value at their respective default
                Variable values. Variables must also have the same names. False otherwise.
    __ne__      Returns the boolean negation of __eq__.
    __gt__      Returns true if the left MathOps object value is greater than the right MathOps object value at their
                respective default Variable values. False otherwise. 
    __lt__      Returns true if the left MathOps object value is less than the right MathOps object value at their
                respective default Variable values. False otherwise. 
    __ge__      Returns true if the left MathOps object value is greater than or equal to the right MathOps object 
                value at their respective default Variable values. False otherwise. 
    __le__      Returns true if the left MathOps object value is less than or equal to the right MathOps object value 
                at their respective default Variable values. False otherwise. 
    DOCTEST
    =======
    
    >>> x = Variable('x',MathOps.pi)
    >>> y = Variable('y',MathOps.pi)
    >>> z = Variable('z',1)
    >>> f = sin(x)
    >>> g = sin(y)
    >>> h = sin(z)
    >>> j = sin(x)
    >>> f == g
    False
    >>> f == h
    False
    >>> f == j
    True
    >>> f > g
    False
    >>> f < h
    True 
    >>> f >= g
    True
    >>> f <= j
    True 
    '''
    def __eq__(self,other):
        if not (type(self)==type(other)):
            return False 
        dict_val_self = self.get_dict_val()
        dict_val_other = other.get_dict_val()
        return (self.get_val(dict_val_self) == other.get_val(dict_val_other) and 
            self.get_der(dict_val_self) == other.get_der(dict_val_other))

    def __ne__(self,other):
        return not self.__eq__(other)

    def __gt__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) > other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __lt__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) < other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __ge__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) >= other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

    def __le__(self,other):
        if (type(self)==type(other)):
            dict_val_self = self.get_dict_val()
            dict_val_other = other.get_dict_val()
            return (self.get_val(dict_val_self) <= other.get_val(dict_val_other))
        else:
            raise ValueError("Can't compare objects of {} and {}".format(type(self),type(other)))

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'x': Variable('x'),'y':Variable('y')})

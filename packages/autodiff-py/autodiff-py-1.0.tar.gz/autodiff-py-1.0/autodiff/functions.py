#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from autodiff.scalar import Scalar

def vectorize(foo):
    """
    Decorator to handle vectors as inputs of our functions.
    Vectors are arrays of scalars.
    """
    def inner(*args, **kwargs):
        for arg in list(args) + list(kwargs.values()):
            if isinstance(arg, np.ndarray):
                return np.vectorize(foo)(*args, **kwargs)
        return foo(*args, **kwargs)
    return inner


@vectorize
def get_value(sclr):
    """
    Refer to getValue's docstring in Scalar class.
    Returns an array of values if called on a vector.
    """
    return sclr.getValue()


@vectorize
def get_deriv(sclr):
    """
    Refer to getDeriv's docstring in Scalar class.
    Returns an array of dictionaries if called on a vector.
    """
    return sclr.getDeriv()


@vectorize
def sin(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the sine function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    ======= 
    sclr: An int, float, or Scalar object on which the sine function will applied.
    
    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the sine function to  'sclr', is returned if the input is a Scalar object .
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the sine function to  'sclr'.

    EXAMPLES
    =========
    >>> x = Scalar('x', 2)
    >>> z = sin(x)
    >>> z._val
    0.9092974268256817
    >>> np.isclose(z._deriv['x'], -0.41614683654714241)
    True
    >>> y = 2
    >>> np.isclose(sin(y), 0.9092974268256817)
    True
    """
    try:
        result = Scalar(None, np.sin(sclr._val) ); #create new Scalar object with updated value
        result._deriv = sclr._deriv.copy(); #result's derivative map is a copy of the passed in Scalar
        #update derivatives for all of the variables in result by applying cos(deriv)
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = np.cos(sclr._val) * d;
        return result;
    except AttributeError: #dealing with an int/float
        return np.sin(sclr);
        

@vectorize
def cos(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the cosine function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    ======= 
    sclr: An int, float, or Scalar object on which the cosine function will applied.
    
    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the cosine function to  'sclr', is returned if the input is a Scalar object .
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the cosine function to  'sclr'.

    EXAMPLES
    =========
    >>> x = Scalar('x', 2)
    >>> z = cos(x)
    >>> z._val
    -0.4161468365471424
    >>> np.isclose(z._deriv['x'], -0.90929742682568171)
    True
    >>> y = 2
    >>> np.isclose(cos(y), -0.4161468365471424)
    True
    """
    try:
        result = Scalar(None, np.cos(sclr._val) ); #create new Scalar object with updated value
        result._deriv = sclr._deriv.copy(); #result's derivative map is a copy of the passed in Scalar
        #update derivatives for all of the variables in result by applying -sin(deriv)
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = -1 * np.sin(sclr._val) * d;
        return result;
    except AttributeError: #dealing with an int/float
        return np.cos(sclr);


@vectorize
def tan(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the tangent function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    ======= 
    sclr: An int, float, or Scalar object on which the tangent function will applied.
    
    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the tangent function to  'sclr', is returned if the input is a Scalar object .
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the tangent function to  'sclr'.

    EXAMPLES
    =========
    >>> x = Scalar('x', 2)
    >>> z = tan(x)
    >>> z._val
    -2.185039863261519
    >>> np.isclose(z._deriv['x'], 5.7743992040419174)
    True
    >>> y = 2
    >>> np.isclose(tan(y), -2.185039863261519)
    True
    """
    return sin(sclr) / cos(sclr);


@vectorize
def power(x, y):
    """
    This function takes in any combination of ints, floats, and Scalar objects. If only ints and floats are provided, then the function returns a float of value equal to raising 'x' to the power of 'y'. If at least one Scalar object is provided, the function returns a Scalar object representing the operation x ** y, where 'x' and 'y' can be a combination of an int/float and a Scalar object or two Scalar objects. Calculation of new Scalar's derivatives follow the rules for exponents and power rule of differentiation respectively. 
    
    INPUTS
    =======   
    x: int or float or Scalar object
    The constant/Scalar base that we raise 'y' to the power of
    y: int or float or Scalar
    The exponent that 'x' is raised to

    RETURNS
    ========
    float, Scalar
    A float is returned if both input are ints/floats. If at least one of the arguments is a Scalar object, then a new Scalar resulting from raising the base 'x' to the power of 'y' is returned.

    NOTES
    =====
    POST:
        - 'x' and 'y' are not changed by the function
        - returns a float or Scalar object, resulting from raising 'x' to the power of 'y'

    EXAMPLES
    =========
    >>> a = Scalar('a', 3)
    >>> b = power(2.0, a)
    >>> b._val
    8.0
    >>> np.isclose(b._deriv['a'], 5.5451774444795623)
    True
    >>> x = Scalar('x', 2)
    >>> x = Scalar('x', 2)
    >>> y = Scalar('y', 3)
    >>> z = power(x, y)
    >>> z._val
    8.0
    >>> z._deriv['x']
    12.0
    >>> np.isclose(z._deriv['y'], 5.545177444479562)
    True
    >>> power(3,4)
    81.0
    """
    if isinstance(x, Scalar) or isinstance(y, Scalar): #check if one of the inputs is a Scalar object
        return x**y;
    else:
        return float(x**y); #dealing with an ints/floats

@vectorize
def exp(sclr):
    """This function takes in an int, float, or Scalar object. If an int/float provided, then the function returns a float of value equal to raising 'e' to the power of 'x'. If a Scalar object is provided, the function returns a Scalar object representing the operation e^(sclr), where 'sclr' is the current Scalar object. Calculations of new Scalar's derivatives follow the power rule of differentiation.

    INPUTS
    =======   
    sclr: int or float or Scalar object
    The int/float/Scalar we raise 'e' to the power of.

    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int or float. If the input is a Scalar object, then a new Scalar resulting from raising 'e' to the power of 'sclr' is returned.

    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from raising 'e' to the power of 'sclr'

    EXAMPLES
    =========
    >>> x = Scalar('x', 2)
    >>> y = exp(x)
    >>> y._val
    7.38905609893065
    >>> np.isclose(y._deriv['x'], 7.38905609893065)
    True
    >>> np.isclose( exp(2), 7.38905609893065)
    True
    """
    try:
        result = Scalar(None, np.exp(sclr._val) ); #create new Scalar object with value = e^val
        result._deriv = sclr._deriv.copy(); #result's derivative map is a copy of the passed in Scalar
        #update derivatives for all of the variables in result by applying e^(deriv)
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = result._val * d;
        return result;
    except AttributeError: #dealing with an int/float
        return np.exp(sclr);


@vectorize
def sqrt(sclr):
    """
    Returns the square root of an int, float, ot Scalar objects.

    INPUTS
    =======
    sclr: int or float or Scalar object
    The constant/Scalar that we take the square root of.

    RETURNS
    ========
    float, Scalar
    A float is returned if both input is an int or float.
    Returns a Scalar object otherwise.

    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function

    EXAMPLES
    =========
    >>> a = Scalar('a', 4)
    >>> b = sqrt(a)
    >>> b._val
    2.0
    >>> b._deriv['a']
    0.25
    >>> sqrt(9)
    3.0
    """
    return power(sclr, .5)

@vectorize
def arcsin(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the arcsine function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the arcsine function will applied.
    
    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the arcsine function to  'sclr', is returned if the input is a Scalar object.
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the arcsine function to  'sclr'.
    """
    try:
        result = Scalar(None, np.arcsin(sclr._val));  # create new Scalar object with updated value
        result._deriv = sclr._deriv.copy();  # result's derivative map is a copy of the passed in Scalar
        # update derivatives for all of the variables in result by applying deriv * 1/(1-x**2)**0.5
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = 1 / np.sqrt(1 - sclr._val**2) * d;
        return result;
    except AttributeError:  # dealing with an int/float
        return np.arcsin(sclr);
    

@vectorize
def arccos(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the arccosine function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the arccosine function will applied.
    
    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the arccosine function to  'sclr', is returned if the input is a Scalar object.
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the arccosine function to  'sclr'.
    """
    try:
        result = Scalar(None, np.arccos(sclr._val));  # create new Scalar object with updated value
        result._deriv = sclr._deriv.copy();  # result's derivative map is a copy of the passed in Scalar
        # update derivatives for all of the variables in result by applying deriv * 1/(1-x**2)**0.5
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = -1 / np.sqrt(1 - sclr._val**2) * d;
        return result;
    except AttributeError:  # dealing with an int/float
        return np.arccos(sclr);    


@vectorize
def arctan(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the arctangent function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the arctangent function will applied.
    
    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the arctangent function to  'sclr', is returned if the input is a Scalar object.
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the arctangent function to  'sclr'.
    """
    try:
        result = Scalar(None, np.arctan(sclr._val));  # create new Scalar object with updated value
        result._deriv = sclr._deriv.copy();  # result's derivative map is a copy of the passed in Scalar
        # update derivatives for all of the variables in result by applying deriv * 1/(1+x**2)
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = 1 / (1 + sclr._val**2) * d;
        return result;
    except AttributeError:  # dealing with an int/float
        return np.arctan(sclr);    


@vectorize
def sinh(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the hyperbolic sine function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the hyperbolic sine function will applied.
    
    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the hyperbolic sine function to  'sclr', is returned if the input is a Scalar object .
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the hyperbolic sine function to  'sclr'.
    """
    try:
        result = Scalar(None, np.sinh(sclr._val));  # create new Scalar object with updated value
        result._deriv = sclr._deriv.copy();  # result's derivative map is a copy of the passed in Scalar
        # update derivatives for all of the variables in result by applying cosh(deriv)
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = np.cosh(sclr._val) * d;
        return result;
    except AttributeError:  # dealing with an int/float
        return np.sinh(sclr);


@vectorize
def cosh(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the hyperbolic cosine function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.
    
    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the hyperbolic cosine function will applied.
    
    RETURNS
    ========
    float, Scalar
    
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the hyperbolic cosine function to  'sclr', is returned if the input is a Scalar object .
    
    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the hyperbolic cosine function to  'sclr'.
    """
    try:
        result = Scalar(None, np.cosh(sclr._val));  # create new Scalar object with updated value
        result._deriv = sclr._deriv.copy();  # result's derivative map is a copy of the passed in Scalar
        # update derivatives for all of the variables in result by applying -sin(deriv)
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = np.sinh(sclr._val) * d;
        return result;
    except AttributeError:  # dealing with an int/float
        return np.cosh(sclr);


@vectorize
def tanh(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the hyperbolic tangent function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.

    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the hyperbolic tangent function will applied.

    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the hyperbolic tangent function to  'sclr', is returned if the input is a Scalar object .

    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the hyperbolic tangent function to  'sclr'.
    """
    return sinh(sclr) / cosh(sclr);


@vectorize
def logistic(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the logistic function to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.

    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the the logistic function will be applied.

    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the logistic function to 'sclr', is returned if the input is a Scalar object .

    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the logistic function to 'sclr'.
    """

    return 1 / (1 + exp(-sclr))


@vectorize
def log(sclr, base):
    """
    This function takes in an int, float, or Scalar object and applies the log with base to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.

    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the log with base function will applied.
    base: An int or float representing the base

    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the log with base function to 'sclr', is returned if the input is a Scalar object .

    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the log with base function to 'sclr'.
    """

    try:
        result = Scalar(None, np.log(sclr._val) / np.log(base));  # create new Scalar object with updated value
        result._deriv = sclr._deriv.copy();  # result's derivative map is a copy of the passed in Scalar
        # update derivatives for all of the variables in result by applying -sin(deriv)
        for key in result._deriv.keys():
            d = result._deriv[key];
            result._deriv[key] = d / (np.log(base) * sclr._val);
        return result;
    except AttributeError:  # dealing with an int/float
        return np.log(sclr) / np.log(base);

@vectorize
def ln(sclr):
    """
    This function takes in an int, float, or Scalar object and applies the natural log to the value. If the argument is an int or float, then the function returns a float. If the argument is a Scalar object, the function returns a new Scalar object with the updated value and derivative.

    INPUTS
    =======
    sclr: An int, float, or Scalar object on which the natural log function will applied.

    RETURNS
    ========
    float, Scalar
    A float is returned if the input is an int/float. A new Scalar object, resulting from applying the natural log function to 'sclr', is returned if the input is a Scalar object .

    NOTES
    =====
    POST:
        - 'sclr' is not changed by the function
        - returns a float or Scalar object, resulting from applying the natural log function to  'sclr'.
    """
    return log(sclr, np.e)
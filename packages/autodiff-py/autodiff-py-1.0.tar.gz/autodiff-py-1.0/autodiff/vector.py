import numpy as np
from autodiff.scalar import Scalar


def create_vector(vector_name, values, seed_vector = None):
    """
    Returns an array of Scalar containing the values
    with names derived from vector_name.

    INPUTS
    =======
    vector_name: string
    The constant or Scalar object we are multiplying the current Scalar object with

    values: list
    The values of the Scalar that will be in the output.

    RETURNS
    ========
    np.ndarray
    Returns the vector as a numpy array object.

    NOTES
    =====
    PRE:
         - vector_name is a string
         - values is a list of ints or floats
    POST:
         - vector_name is not changed by the function
         - values is not changed by the function

    EXAMPLES
    =========
    >>> w = create_vector('w', [2, 1, 3])
    >>> w[0]._val
    2.0
    >>> w[1].getDeriv()['w2']
    1.0
    """
    if seed_vector is None:
        return np.array([Scalar("%s%i" % (vector_name, i), value)
                         for i, value in enumerate(values, 1)])
    else:
        if len(values) != len(seed_vector):
            raise Exception("Values not the same length as seed vector!")
        return np.array([Scalar("%s%i" % (vector_name, i), value, seed_vector[i - 1])
                         for i, value in enumerate(values, 1)])


def get_jacobian(vector, variables):
    """
    Returns the jacobian of the vector w.r.t. the variables passed in.

    INPUTS
    =======
    variables: list
    A list of strings corresponding to the variable names.

    RETURNS
    ========
    jacobian: numpy array
    The numpy array that represents the jacobian of the vector w.r.t.
    the variables.

    EXAMPLES
    =========
    >>> x = create_vector('x', [1, 2, 3])
    >>> y = create_vector('y', [5, 8, -7])
    >>> z = x - y
    >>> jacobian = get_jacobian(z, ['x1', 'y2', 't'])
    >>> np.array_equal(jacobian, np.array([[1.,0.,0.],[0.,-1.,0.],[0.,0.,0.]]))
    True
    """

    return np.array([sclr.getGradient(variables) for sclr in vector])
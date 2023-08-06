import autodiff as ad
import numpy as np
from scipy.sparse.linalg import gmres
from scipy.sparse.linalg import LinearOperator

def gradient_descent(f, intial_guess, step_size = 0.01, max_iter = 10000, tol = 1e-12):
    """
    Implements gradient descent

    INPUTS
    ======= 
    f: function 
    The function that we are trying to find the minimum of. The function must take in single list/array that has the same dimension as len(initial_guess).
    
    initial_guess: List or array of ints/floats
    The initial position to begin the search for the minimum of the function 'f'.

    step_size: float
    The step size. In this case the step size will be constant
    
    max_iter: int
    The max number of iterations
    
    tol: float
    The tolerance. If the norm of the gradient is less than the tolerance, the algorithm will stop
    
    RETURNS
    ========
    Tuple
    A tuple with first entry which maps to the position of the minimum and second entry which maps to the number of iterations it took for the algorithm to stop
    """

    x = np.array(intial_guess)
    for i in range(max_iter):
        x_vector = ad.create_vector('x', x)
        fn_at_x = f(x_vector)
        gradient = fn_at_x.getGradient(['x{}'.format(i) for i in range(1, len(x) + 1)])
        if np.sqrt(np.abs(gradient).sum()) < tol:
            break
        x = x - step_size * gradient
    return (x, i + 1)

def line_search(f, x, p, tau = 0.1, c = 0.1, alpha = 1):
    """
    Implements Backtracking Line Search.  https://en.wikipedia.org/wiki/Backtracking_line_search

    INPUTS
    ======= 
    fn: Function 
    The function that we are trying to find the minimum of. The function must take in the same number of arguments as len(x)
    
    x: List or array of ints/floats
    The initial position 
    
    p: numpy array
    Descent direction

   	tau: float
   	Search control parameter tau

   	c: float
   	Search control parameter 

	alpha: float
	Starting alpha
    
    RETURNS
    ========
    float
    The alpha we found through backtracking line search
    """

    x = ad.create_vector('x', x)
    fn_val1 = f(x)
    fn_val2 = f(x + alpha * p)
    gradient = fn_val1.getGradient(['x{}'.format(i) for i in range(1, len(x) + 1)])
    m = (p * gradient).sum()
    t = -c * m
    while ad.get_value(fn_val1 - fn_val2) < alpha * t:
        alpha = tau * alpha 
        fn_val2 = f(x + alpha * p)
    return alpha
        

def quasi_newtons_method(f, initial_guess, max_iter = 10000, method = 'BFGS', tol = 1e-12):
    """
    Implements Quasi-Newton methods with different methods to estimate the inverse of the Hessian.
    Utilizes backtracking line search to determine step size.     
    https://en.wikipedia.org/wiki/Quasi-Newton_method

    INPUTS
    ======= 
    f: function 
    The function that we are trying to find the minimum of. The function must take in single list/array that has the same dimension as len(initial_guess).
    
    initial_guess: List or array of ints/floats
    The initial position to begin the search for the minimum of the function 'f'.
    
    max_iter: int
    The max number of iterations
    
    method: String
    The update method to update the estimate of the inverse of the Hessian.
    Currently, BFGS, DFP, and Broyden are implemented.
    
    tol: float
    The tolerance. If the norm of the gradient is less than the tolerance, the algorithm will stop
    
    RETURNS
    ========
    Tuple
    A tuple with first entry which maps to the position of the minimum and second entry which maps to the number of iterations it took for the algorithm to stop
    """
    
    if method not in ['BFGS', 'DFP', 'Broyden']:
            raise Exception("Not a valid method.")
    x = initial_guess
    H = np.identity(len(x))
    for i in range(max_iter):
        x_vector = ad.create_vector('x', x)
        fn_at_x = f(x_vector)
        gradient = fn_at_x.getGradient(['x{}'.format(i) for i in range(1, len(x) + 1)])

        p = -H @ gradient
        
        alpha = line_search(f, x, p)
        delta_x = alpha * p

        x = x + delta_x
        x_vector2 = ad.create_vector('x', x)
        fn_at_x2 = f(x_vector2)
        gradient2 = fn_at_x2.getGradient(['x{}'.format(i) for i in range(1, len(x) + 1)])
        if np.sqrt(np.abs(gradient2).sum()) < tol:
            break
        y = (gradient2 - gradient).reshape(-1, 1)
        delta_x = delta_x.reshape(-1, 1)
        if method == 'BFGS':
            H = (np.identity(len(H)) - (delta_x @ y.T) / (y.T @ delta_x)) @ H \
                @ (np.identity(len(H)) - (y @ delta_x.T) / (y.T @ delta_x)) + (delta_x @ delta_x.T) / (y.T @ delta_x)
        elif method == 'DFP':
            H = H + (delta_x @ delta_x.T) / (delta_x.T @ y) - (H @ y @ y.T @ H) / (y.T @ H @ y)
        elif method == 'Broyden':
            H = H + ((delta_x - H @ y) @ delta_x.T @ H) / (delta_x.T @ H @ y)

    return (x, i + 1)

def _newtons_method_gmres_action(f, initial_guess, max_iter=50, tol=1e-12):
    """
    Helper function to solve for the step size using a Linear Operator that is passed to scipy.sparse.linalg.gmres for Newton's method.
    
    INPUTS
    ======= 
    f: Function 
    The function that we are trying to find a root of. The function must take in single list/array that has the same dimension as len(initial_guess).
    
    initial_guess: List or array of ints/floats
    The initial position 
    
    max_iter: int
    The max number of iterations
    
    
    tol: float
    The tolerance. If the abs value of the steps for one iteration are less than the tol, then the algorithm stops
    
    RETURNS
    ========
    Tuple
    A tuple with first entry that maps to the position of the minimum and second entry, which is the number of iterations it took for the algorithm to stop.
    
    NOTES
    =====
    POST:
        - Returns a tuple. The first entry maps to the position of the minimum, and the second entry is the number of iterations it took for the algorithm to stop.
        - If the convergence is not reached by 'max_iter', then a RuntimeError is thrown to alert the user.
    """

    output_dim = len(f(initial_guess))
    
    @np.vectorize
    def sum_values(dictionary):
        return sum(dictionary.values())
    
    def create_action(x0):
        
        def L_fun(x):
            """
            Action
            Returns J_f(x0)*x by setting the values of 'x' as the initial derivatives for the variables in x0.
            """
        
            f_x0 = f(ad.create_vector('x0', x0, seed_vector=x));
            f_x0 = np.array(f_x0) #ensure that f_x0 is np.array
            action = sum_values(ad.get_deriv(f_x0))
            return action
        
        L = LinearOperator(shape=(output_dim, len(x0)), matvec=L_fun)
        
        return L
    
    x0 = initial_guess
    for iter_num in range(max_iter):
        L = create_action(x0)
        b = -1 * np.array(f(x0))
        if len(x0) == 1:
            b = np.array([b])
        step, _ = gmres(L, b, tol = tol, atol = 'legacy')
        xnext = x0 + step 
        if np.all(np.abs(xnext - x0) < tol):
            return (xnext, iter_num + 1);
        x0 = xnext
    
    raise RuntimeError("Failed to converge after {0} iterations, value is {1}".format(max_iter, x0) );


def newtons_method(f, initial_guess, max_iter = 1000, method = 'exact', tol =1e-12):
    """
    Implements Newton's method for root-finding with different methods to find the step at each iteration
    
    INPUTS
    ======= 
    f: Function 
    The function that we are trying to find a root of. The function must take in single list/array that has the same dimension as len(initial_guess).
    
    initial_guess: List or array of ints/floats
    The initial position to begin the search for the roots of the function 'f'.
    
    max_iter: int
    The max number of iterations
    
    method: String
    The method to solve Ax=b to find the step 'x' at each iteration.
    Options:
        'inverse' : calculate (A^-1)*b = x
        'exact' : Use np.linalg.solve(A, b)
        'gmres" : Use scipy.sparse.linalg.gmres(A, b), which finds a solution iteratively
        'gmres_action' :  Use np.linalg.gmres(L, b), where 'L' is a linear operator used to efficiently calculate A*x. Works well for functions with sparse Jacobian matrices.
    
    tol: float
    The tolerance. If the abs value of the steps for one iteration are less than the tol, then the algorithm stops
    
    RETURNS
    ========
    Tuple
    A tuple with first entry which maps to the position of the minimum and second entry which maps to the number of iterations it took for the algorithm to stop.
    
    NOTES
    =====
    POST:
        - Returns a tuple. The first entry maps to the position of the minimum, and the second entry is the number of iterations it took for the algorithm to stop.
        - If the convergence is not reached by 'max_iter', then a RuntimeError is thrown to alert the user.
    """

    if method not in ['inverse', 'exact', 'gmres', 'gmres_action']:
        raise Exception("Not a valid method.")
    if len(f(initial_guess)) != len(initial_guess):
        raise Exception('Output dimension of f should be the same as the input dimension of f.')
    if method == 'gmres_action':
        return _newtons_method_gmres_action(f, initial_guess, max_iter, tol)
    x0 = ad.create_vector('x0', initial_guess)
    for iter_num in range(max_iter):
        fn = np.array(f(x0)); #need convert the list/array that is passed back from function, so downstream autodiff functions for vectors work properly
        jacob = ad.get_jacobian(fn, ['x0{}'.format(i) for i in range(1, len(fn) + 1)])
        if method == 'inverse':
            step = np.linalg.inv(-jacob).dot(ad.get_value(fn))
        if method == 'exact':
            step = np.linalg.solve(-jacob, ad.get_value(fn))
        elif method == 'gmres':
            step, _ = gmres(jacob, -ad.get_value(fn), tol = tol, atol = 'legacy')
        xnext = x0 + step
        
        #check if we have converged
        if np.all(np.abs(ad.get_value(xnext) - ad.get_value(x0)) < tol):
            return (ad.get_value(xnext), iter_num + 1);
        
        #update x0 because we have not converged yet
        x0 = xnext
        
    raise RuntimeError("Failed to converge after {0} iterations, value is {1}".format(max_iter, ad.get_value(x0)) );

    
    


        

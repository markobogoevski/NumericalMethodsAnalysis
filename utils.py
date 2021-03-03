import inspect
from scipy.misc import derivative


def test_conditions_for_solution_existence(function, a, b):
    """
    This function checks the conditions for solution existence in the interval [a,b] for the provided function. The
    solution exists if f(a)*f(b)<0.
    :param function: The function for which the condition is to be tested
    :param a: The left side of the interval
    :param b: The right side of the interval
    :return: Throws an assertion error if not correct
    """
    print(f"Checking values of f(a) and f(b).")
    print(f"Value f(a) = {function(a)}")
    print(f"Value f(b) = {function(b)}")
    assert function(a) * function(b) <= 0, "If f(a)*f(b)>0, the function f has no zero (no solution). Meaning there " \
                                           "doesn't exist c e D(domain of f) such that f(c)=0 "


def convergence_criterion_1(epsilon, x_curr, x_prev):
    """
    This function checks the 1st convergence criterion from slide 23 from Numericka matemtika del 4
    :param epsilon: Iterative process error, error/precision rate
    :param x_curr: X in iteration k (current iteration)
    :param x_prev: X in iteration k-1 (previous iteration)
    :return: True/False
    """
    return abs(x_curr - x_prev) < epsilon


def convergence_criterion_2(epsilon, x_curr, function):
    """
    This function checks the 2nd convergence criterion from slide 23 from Numericka matemtika del 4
    :param epsilon: Iterative process error, error/precision rate
    :param x_curr: X in iteration k (current iteration)
    :param function: The function for which the convergence criterion is checked
    :return: True/False
    """
    return abs(function(x_curr)) < epsilon


def convergence_criterion_3(epsilon, x_curr, x_prev):
    """
    This function checks the 3rd convergence criterion from slide 24 from Numericka matemtika del 4
    :param epsilon: Iterative process error, error/precision rate
    :param x_curr: X in iteration k (current iteration)
    :param x_prev: X in iteration k-1 (previous iteration)
    :return: True/False
    """
    return abs((x_curr - x_prev) / x_curr) < epsilon


def convergence_criterion_4(epsilon, x_curr, function):
    """
    This function checks the 4th convergence criterion from slide 24 from Numericka matemtika del 4
    :param epsilon: Iterative process error, error/precision rate
    :param x_curr: X in iteration k (current iteration)
    :param function: The function for which the convergence criterion is checked
    :return: True/False
    """
    return abs(function(x_curr) / derivative(function, x_curr)) < epsilon


def get_one_line_function_print(function):
    """
    A utility function which is used to print text inside one-liner commented functions. The function should be
    commented by the ''' scheme.
    :param function: The one-liner function to print
    :return: The one-liner text after the return keyword in the function
    """
    return inspect.getsource(function).split('"""')[2].split("\n")[1].split("return ")[1]

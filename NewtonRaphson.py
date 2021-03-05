from utils import *
import datetime


def get_next_point_newton_raphson(function, x_prev):
    """
    Gets the next interval point using the newton-raphson method
    :param function: The function for which the method is supposed to be performed
    :param x_prev: The previous value of x
    :return: The next x value
    """
    return x_prev - (function(x_prev) / derivative(function, x_prev))


def get_initial_point_x0(function, a, b):
    """
    Gets the first interval point using the newton-raphson method
    :param function: The function for which the method is supposed to be performed
    :param a: The left side of the interval
    :param b: The right side of the interval
    :return: The first split point (First x)
    """
    second_derivative = derivative(function, a, n=2)
    if second_derivative * function(a) > 0:
        return a
    return b


def newton_raphson(function, a, b, epsilon, convergence_criterion):
    """
    A function which performs the numerical method Newton-Raphson on a function given an interval and rate of precision.
    :param function: The function to be solved with the numerical method
    :param a: The left x-coordinate point in the interval where the solution is to be searched in.
    :param b: The right x-coordinate point in the interval where the solution is to be searched in.
    :param epsilon: The rate of precision of the solution
    :param convergence_criterion: Dictates the convergence criterion. Can be 1, 2, 3 or 4. Further explanation given in
    the function get_convergence_criterion.
    :return: The solution of the function in the interval [a,b] if f(a)*f(b)<0 (if there is a solution in the interval)
    """
    solution_dict = dict()
    solution_array = list()
    function_print = get_one_line_function_print(function)
    print(f"\nPerforming Newton Raphson on the function: ({function_print}) on the interval [{a},{b}]...")
    if convergence_criterion == 1:
        convergence_criterion_print = get_one_line_function_print(convergence_criterion_1)
    elif convergence_criterion == 2:
        convergence_criterion_print = get_one_line_function_print(convergence_criterion_2)
    elif convergence_criterion == 3:
        convergence_criterion_print = get_one_line_function_print(convergence_criterion_3)
    else:
        convergence_criterion_print = get_one_line_function_print(convergence_criterion_4)
    print(f"Using convergence criterion: {convergence_criterion_print}.")
    print(f'First, checking test conditions for solution existence in the interval [{a},{b}].')
    test_conditions_for_solution_existence(function, a, b)
    print("There is a solution in the interval!")
    print(f"Finding solution given precision {epsilon}...\n")
    iteration_num = 0
    print(f"Newton Raphson start.\n")
    print(f'Iteration number: {iteration_num}')
    x_prev = get_initial_point_x0(function, a, b)  # Initialization step
    x_curr = get_next_point_newton_raphson(function, x_prev)
    solution_array.append(x_curr)
    print(f'======================================================================'
          f'======================================================================')
    print(f'X_prev: {x_prev}, X_curr: {x_curr}')
    print(f'======================================================================'
          f'======================================================================\n')
    start_time = datetime.datetime.now()
    while True:
        if convergence_criterion == 1:
            criterion_satisfied = convergence_criterion_1(epsilon, x_curr, x_prev)
        elif convergence_criterion == 2:
            criterion_satisfied = convergence_criterion_2(epsilon, x_curr, function)
        elif convergence_criterion == 3:
            criterion_satisfied = convergence_criterion_3(epsilon, x_curr, x_prev)
        else:
            criterion_satisfied = convergence_criterion_4(epsilon, x_curr, function)
        if criterion_satisfied:
            # Finish the iteration
            break
        x_prev = x_curr
        x_curr = get_next_point_newton_raphson(function, x_prev)
        solution_array.append(x_curr)
        iteration_num += 1
        print(f'Iteration number: {iteration_num}')
        print(f'======================================================================'
              f'======================================================================')
        print(f'X_prev: {x_prev}, X_curr: {x_curr}')
        print(f'======================================================================'
              f'======================================================================\n')
    print(f'Newton Raphson end.\n')
    end_time = datetime.datetime.now()
    time_elapsed = (end_time - start_time).total_seconds() * 1000
    print(
        f'The solution to the function ({function_print}) is {x_curr} with accuracy of {epsilon} by using convergence '
        f'test: ({convergence_criterion_print}).\n '
        f'Time of full iteration: {time_elapsed} ms.\nNumber of steps: {iteration_num}')
    solution_dict['solution'] = solution_array
    solution_dict['time_elapsed'] = time_elapsed
    solution_dict['num_iterations'] = iteration_num
    return solution_dict

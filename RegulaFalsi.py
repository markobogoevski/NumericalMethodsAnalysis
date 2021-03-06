import datetime
from utils import *


def get_new_split_point_regula_c(function, a, b):
    """
    Calculates a new split point for the interval [a,b] and the provided function by Regula Falsi method.
    The split point (c,0) is the point of intersection between the function and the x-coordinate on the interval [a,b]
    :param function: The function for which the split point is to be calculated
    :param a: The left side of the interval
    :param b: The right side of the interval
    :return: The split point
    """
    # By formula
    c = (a * function(b) - b * function(a)) / (function(b) - function(a))
    return c


def regula_falsi(function, a, b, epsilon, convergence_criterion):
    """
    A function which performs the numerical method Regula Falsi on a function given an interval and rate of precision.
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
    solution_dict['convergence'] = True
    max_iterations = 60
    function_print = get_one_line_function_print(function)
    print(f"\nPerforming Regula Falsi on the function: ({function_print}) on the interval [{a},{b}]...")
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
    x_prev = a
    c = a  # Initialization step
    start_time = datetime.datetime.now()
    iteration_num = 0
    print(f"Regula falsi start.\n")
    print(f'Iteration number: {iteration_num}')
    print(f'======================================================================'
          f'======================================================================')
    x_prev = c
    c = get_new_split_point_regula_c(function, a, b)
    solution_array.append(c)
    print(f'Current interval searched in: [{a},{b}]. Split point(c) for interval: {c}')

    iteration_num += 1
    # Define new a and b
    if function(a) * function(c) < 0:
        print(f'Since f(a)*f(c)<0 there must be a solution in [a,c]. Creating new interval [{a},{c}].')
        b = c
    else:
        print(f'Since f(c)*f(b)<0 there must be a solution in [c,b]. Creating new interval [{c},{b}].')
        a = c

    print(f'======================================================================'
          f'======================================================================\n')
    while True:
        if iteration_num == max_iterations:
            solution_dict['convergence'] = False
            print(f"The method still hasn't converged after 60 iterations...stopping.")
            break
        if convergence_criterion == 1:
            criterion_satisfied = convergence_criterion_1(epsilon, c, x_prev)
        elif convergence_criterion == 2:
            criterion_satisfied = convergence_criterion_2(epsilon, c, function)
        elif convergence_criterion == 3:
            criterion_satisfied = convergence_criterion_3(epsilon, c, x_prev)
        else:
            criterion_satisfied = convergence_criterion_4(epsilon, c, function)
        if criterion_satisfied:
            # Finish the iteration
            break
        print(f'Iteration number: {iteration_num}')
        print(f'======================================================================'
              f'======================================================================')
        x_prev = c
        c = get_new_split_point_regula_c(function, a, b)
        solution_array.append(c)
        print(f'Current interval searched in: [{a},{b}]. Split point(c) for interval: {c}')

        iteration_num += 1
        # Define new a and b
        if function(a) * function(c) < 0:
            print(f'Since f(a)*f(c)<0 there must be a solution in [a,c]. Creating new interval [{a},{c}].')
            b = c
        else:
            print(f'Since f(c)*f(b)<0 there must be a solution in [c,b]. Creating new interval [{c},{b}].')
            a = c

        print(f'======================================================================'
              f'======================================================================\n')
    print(f'Regula falsi end.\n')
    end_time = datetime.datetime.now()
    time_elapsed = (end_time - start_time).total_seconds() * 1000
    print(
        f'The solution to the function ({function_print}) is {c} with accuracy of {epsilon} by using convergence test: '
        f'({convergence_criterion_print}).\n '
        f'Time of full iteration: {time_elapsed} ms.\nNumber of steps: {iteration_num}')
    solution_dict['solution'] = solution_array
    solution_dict['time_elapsed'] = time_elapsed
    solution_dict['num_iterations'] = iteration_num
    return solution_dict

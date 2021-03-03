from RegulaFalsi import *
from NewtonRaphson import *
import os
import pandas as pd


def generate_comparative_report(function, a, b, report_path, convergence_met=True):
    precisions = [1e-2, 1e-3, 1e-5, 1e-10, 1e-20, 1e-30]
    convergence_crits = [1, 2, 3, 4]
    report_folder = "Reports"
    os.makedirs(report_folder, exist_ok=True)
    final_path_regula = os.path.join(report_folder, report_path + "_regula.csv")
    final_path_newt_raph = os.path.join(report_folder, report_path + "_newt_raph.csv")
    data_regula = pd.DataFrame(columns=["Function", "a", "b", "Epsilon", "Convergence Criterion", "Method", "Solution",
                                        "Number of iterations", "Time elapsed", "Convergence"])
    data_newton_raphson = pd.DataFrame(columns=["Function", "a", "b", "Epsilon", "Convergence Criterion", "Method",
                                                "Solution", "Number of iterations", "Time elapsed", "Convergence"])
    for precision in precisions:
        for convergence_crit in convergence_crits:
            solution_regula = regula_falsi(function, a, b, precision, convergence_crit)
            solution_newton_raphson = newton_raphson(function, a, b, precision, convergence_crit)
            function_print = get_one_line_function_print(function)
            if convergence_met:
                convergence_string = "Yes"
            else:
                convergence_string = "No"
            regula_row = pd.Series(data={'Function': function_print, 'a': a, 'b': b, 'Epsilon': precision,
                                         'Convergence Criterion': convergence_crit, "Method": "regula_falsi",
                                         'Solution': solution_regula['solution'],
                                         'Number of iterations': solution_regula['num_iterations'],
                                         'Time elapsed': solution_regula['time_elapsed'],
                                         'Convergence': convergence_string})
            newt_raph_row = pd.Series(data={'Function': function_print, 'a': a, 'b': b, 'Epsilon': precision,
                                            'Convergence Criterion': convergence_crit, "Method": "newton_raphson",
                                            'Solution': solution_newton_raphson['solution'],
                                            'Number of iterations': solution_newton_raphson['num_iterations'],
                                            'Time elapsed': solution_newton_raphson['time_elapsed'],
                                            'Convergence': convergence_string})
            data_regula = data_regula.append(regula_row, ignore_index=True)
            data_newton_raphson = data_newton_raphson.append(newt_raph_row, ignore_index=True)

    data_regula.to_csv(final_path_regula, index=False)
    data_newton_raphson.to_csv(final_path_newt_raph, index=False)


def test_function(x):
    """
    A one line function for which to test either the Regula Falsi or the NewtonRaphson method
    :param x: The argument of the function
    :return: The function itself
    """
    return x ** 3 - 3 * x ** 2 + 2


if __name__ == "__main__":
    a = -1
    b = 4
    epsilon = 1e-20
    convergence_criterion = 1
    # solution_regula = regula_falsi(test_function, a, b, epsilon, 1)
    # solution_newton = newton_raphson(test_function, a, b, epsilon, 1)
    generate_comparative_report(test_function, a, b, "starter_function")

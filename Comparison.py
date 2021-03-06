from RegulaFalsi import *
from NewtonRaphson import *
import os
import pandas as pd
import math


def generate_comparative_report(function, a, b, report_path, analytical_solution=None):
    """
    A function which generates reports for the provided function by using the numerical methods Regula Falsi and
    Newton Rhapson in the interval [a,b]. The function saves reports and visualizations plots under the folders
    Reports/report_path  and Visualizations/report_path
    :param function: The function to be solved by the two methods
    :param a: The left side of the interval
    :param b: The right side of the interval
    :param report_path: The name of the function under which to save the reports and plots
    :param analytical_solution: The analytical solution to the equation
    :return: None
    """
    precisions = [1e-1, 5e-2, 1e-2, 5e-3, 1e-3, 1e-4, 1e-5, 1e-6]
    convergence_crits = [1, 2, 3, 4]
    report_folder = "Reports"
    function_print = get_one_line_function_print(function)
    visualizations_folder = "Visualizations"
    report_path_folder = os.path.join(report_folder, report_path)
    os.makedirs(report_folder, exist_ok=True)
    os.makedirs(visualizations_folder, exist_ok=True)
    os.makedirs(report_path_folder, exist_ok=True)
    final_path_regula = os.path.join(report_path_folder, report_path + "_regula.csv")
    final_path_newt_raph = os.path.join(report_path_folder, report_path + "_newt_raph.csv")
    vis_path = os.path.join(visualizations_folder, report_path)
    os.makedirs(vis_path, exist_ok=True)
    func_path = os.path.join(vis_path, report_path)
    plot_function(function, a, b, function_print, func_path)
    vis_path_time = os.path.join(vis_path, "time_elapsed")
    os.makedirs(vis_path_time, exist_ok=True)
    vis_path_iterations = os.path.join(vis_path, "num_iterations")
    os.makedirs(vis_path_iterations, exist_ok=True)
    vis_path_solutions = os.path.join(vis_path, "solutions")
    vis_path_deltas = os.path.join(vis_path, "deltas")
    os.makedirs(vis_path_solutions, exist_ok=True)
    os.makedirs(vis_path_deltas, exist_ok=True)
    data_regula = pd.DataFrame(columns=["Function", "a", "b", "Epsilon", "Convergence Criterion", "Method", "Solution",
                                        "Number of iterations", "Time elapsed", "Convergence"])
    data_newton_raphson = pd.DataFrame(columns=["Function", "a", "b", "Epsilon", "Convergence Criterion", "Method",
                                                "Solution", "Number of iterations", "Time elapsed", "Convergence",
                                                "Precision to analytical met"])
    for convergence_crit in convergence_crits:
        regula_time = []
        newt_time = []
        regula_iterations = []
        newt_iterations = []
        for precision in precisions:
            solution_regula = regula_falsi(function, a, b, precision, convergence_crit)
            solution_newton_raphson = newton_raphson(function, a, b, precision, convergence_crit)
            function_print = get_one_line_function_print(function)
            solutions_reg = solution_regula['solution']
            solutions_newt = solution_newton_raphson['solution']
            convergence_regula = solution_regula['convergence']
            convergence_newt = solution_newton_raphson['convergence']

            if convergence_regula:
                convergence_string_reg = "Yes"
                if analytical_solution is not None:
                    if abs(solutions_reg[-1] - analytical_solution) <= precision:
                        precision_string_regula = "Yes"
                    else:
                        precision_string_regula = "No"
                else:
                    precision_string_regula = "No analytical solution provided!"
            else:
                convergence_string_reg = "No"
                precision_string_regula = "No, no convergence"
            if convergence_newt:
                convergence_string_newt = "Yes"
                if analytical_solution is not None:
                    if abs(solutions_newt[-1] - analytical_solution) <= precision:
                        precision_string_newt = "Yes"
                    else:
                        precision_string_newt = "No"
                else:
                    precision_string_newt = "No analytical solution provided!"
            else:
                convergence_string_newt = "No"
                precision_string_newt = "No, no convergence"

            regula_row = pd.Series(data={'Function': function_print, 'a': a, 'b': b, 'Epsilon': precision,
                                         'Convergence Criterion': convergence_crit, "Method": "regula_falsi",
                                         'Solution': solution_regula['solution'][-1],
                                         'Number of iterations': solution_regula['num_iterations'],
                                         'Time elapsed': solution_regula['time_elapsed'],
                                         'Convergence': convergence_string_reg,
                                         'Precision to analytical met': precision_string_regula})
            newt_raph_row = pd.Series(data={'Function': function_print, 'a': a, 'b': b, 'Epsilon': precision,
                                            'Convergence Criterion': convergence_crit, "Method": "newton_raphson",
                                            'Solution': solution_newton_raphson['solution'][-1],
                                            'Number of iterations': solution_newton_raphson['num_iterations'],
                                            'Time elapsed': solution_newton_raphson['time_elapsed'],
                                            'Convergence': convergence_string_newt,
                                            'Precision to analytical met': precision_string_newt})

            regula_time.append(solution_regula['time_elapsed'])
            newt_time.append(solution_newton_raphson['time_elapsed'])
            regula_iterations.append(solution_regula['num_iterations'])
            newt_iterations.append(solution_newton_raphson['num_iterations'])
            data_regula = data_regula.append(regula_row, ignore_index=True)
            data_newton_raphson = data_newton_raphson.append(newt_raph_row, ignore_index=True)
            solution_final_path = os.path.join(vis_path_solutions, f"convergence_"
                                                                   f"crit_{convergence_crit}_precision_{precision}.png")
            delta_final_path = os.path.join(vis_path_deltas, f"convergence_"
                                                             f"crit_{convergence_crit}_precision_{precision}.png")
            offset = abs(solutions_reg[-1])
            x_min_sol, x_max_sol = min(min(solutions_reg), min(solutions_newt)) - offset / 5, max(max(solutions_reg),
                                                                                                  max(solutions_newt)) \
                                   + offset / 5
            plot_solutions(solutions_reg, solutions_newt, x_label_1="Regula_solutions",
                           x_label_2="Newt_raphson_solutions",
                           title=function_print + ": Solutions", outpath=solution_final_path,
                           x_limits=(x_min_sol, x_max_sol))
            if analytical_solution is not None:
                deltas_reg = [abs(solution_reg - analytical_solution) for solution_reg in solutions_reg]
                deltas_newt = [abs(solution_newt - analytical_solution) for solution_newt in solutions_newt]
                y_limits = (min(min(deltas_reg), min(deltas_newt)), max(max(deltas_reg), max(deltas_newt)))
                plot_deltas(range(len(solutions_reg)), range(len(solutions_newt)), deltas_reg, deltas_newt,
                            "Number of iterations Regula-falsi", "Number of iterations Newton Raphson",
                            "Deltas for Regula-falsi", "Deltas for Newton Raphson",
                            function_print + ": Deltas", outpath=delta_final_path, y_limits=y_limits)

        vis_path_time_final = os.path.join(vis_path_time, "Convergence_crit_" + str(convergence_crit) + "_")
        vis_path_iterations_final = os.path.join(vis_path_iterations, "Convergence_crit_" + str(convergence_crit) + "_")
        y_min_time, y_max_time = min(min(regula_time), min(newt_time)) - 1, max(max(regula_time), max(newt_time)) + 1
        y_min_iter, y_max_iter = min(min(regula_iterations) - 4, min(newt_iterations)), max(max(regula_iterations),
                                                                                            max(newt_iterations)) + 4

        plot_scatter_bi(precisions, regula_time, newt_time, x_label="Precision", y_label_1="Regula_time",
                        y_label_2="Newt_raphson_time", title=function_print + ": Time elapsed",
                        outpath=vis_path_time_final + "_time_elapsed.png", y_limits=(y_min_time, y_max_time))
        plot_scatter_bi(precisions, regula_iterations, newt_iterations, x_label="Precision",
                        y_label_1="Regula_iterations", y_label_2="Newt_raphson_iterations",
                        title=function_print + ": Number of iterations",
                        outpath=vis_path_iterations_final + "_num_iterations.png", y_limits=(y_min_iter, y_max_iter))
    data_regula.to_csv(final_path_regula, index=False)
    data_newton_raphson.to_csv(final_path_newt_raph, index=False)


def starter_function(x):
    """
    A one line function for which to test either the Regula Falsi or the NewtonRaphson method
    :param x: The argument of the function
    :return: The function itself
    """
    return x ** 3 - 3 * x ** 2 + 2
    # Has an analytical solution of x1=1, x2/3 = += 1-np.sqrt(3)


def linear_function(x):
    """
    A linear function
    :param x: The argument of the function
    :return: The function itself
    """
    return 3 * (x - 3) + 3
    # Has an analytical solution of x=2


def quadratic_function(x):
    """
    A quadratic function
    :param x: The argument of the function
    :return: The function itself
    """
    return 2 * (x - 2) ** 2 - 10
    # Has an analytical solution of x1=2-sqrt(5) and x2=2+sqrt(5)


def cubic_function(x):
    """
    A cubic function
    :param x: The argument of the function
    :return: The function itself
    """
    return (-x) ** 3 + x ** 2 - 3
    # Has an analytical real solution of (1.0 / 3) * (1 - pow((2.0 / (79 - 9 * np.sqrt(77))), 1.0 / 3) - pow((1.0 / 2 *
    # (79 - 9 * np.sqrt(77))),1.0/3)


def root_function(x):
    """
    A root function
    :param x: The argument of the function
    :return: The function itself
    """
    return pow(x, (1.0 / 3)) - (1 / pow(x, (1.0 / 2))) - 3
    # Has an analytical real solution of (by digits) 32.0551400884145540883151584074125554591926050266913486210


def absolute_value_function(x):
    """
    An absolute value function
    :param x: The argument of the function
    :return: The function itself
    """
    return abs(x ** 2 - 3 * x + 8) - abs(pow(x / 2, (1.0 / 2))) - 10
    # Has an analytical real solution of (by digits) -0.700404229147059547116215842548458870154244129188475
    # and 3.87528794161629661393951658034464365520790087121135. Converges for [0.5,6] and diverges for [-2,-0.5]


def reciprocal_function(x):
    """
    A reciprocal function
    :param x: The argument of the function
    :return: The function itself
    """
    return 1 / (x ** 2) - 1 / (x ** 3) + 1 / (x ** 4) - 4
    # Has an analytical real solution of (by digits) -0.909469125804229275193458176920764345971697064
    # and 0.663848177210232222869705336414468422223096010


def logarithmic_function(x):
    """
    A logarithmic function
    :param x: The argument of the function
    :return: The function itself
    """
    return np.log(x ** 3 - x ** 2 + 1 / x - 1.0 / 2)
    # Has an analytical real solution of (by digits): 0.607939041215937491647310167310837792295480047


def exponential_function(x):
    """
    An exponential function
    :param x: The argument of the function
    :return: The function itself
    """
    return np.exp(3 * x ** 2 - 3 * x - 10) - np.exp(x)
    # Has analytical real solutions: 1/3*(2-sqrt(34)) and 1/3*(2+sqrt(34))


def trigonometric_function(x):
    """
    A trigonometric function
    :param x: The argument of the function
    :return: The function itself
    """
    return np.sin(3 * x + 2) + np.cos(4 * x ** 2 - 2)
    # Has 4 analytical real solutions with varying n e Z. Showing one of them: -3/8 + 1/8 * sqrt(9 - 8*π + 32*π)


if __name__ == "__main__":
    a = 0.5
    b = 1
    # solution_regula = regula_falsi(test_function, a, b, epsilon, 1)
    # solution_newton = newton_raphson(test_function, a, b, epsilon, 1)
    # analytical_sol = (1.0 / 3) * (
    #        1 - pow((2.0 / (79 - 9 * np.sqrt(77))), 1.0 / 3) - pow((1.0 / 2 * (79 - 9 * np.sqrt(77))), 1.0 / 3))
    analytical_sol = -3.0 / 8 + 1.0 / 8 + np.sqrt(9 - 8 * np.pi + 32 * np.pi)  # 0.7733563232...
    generate_comparative_report(trigonometric_function, a, b, "trigonometric_non_contig",
                                analytical_solution=analytical_sol)

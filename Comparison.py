from RegulaFalsi import *
from NewtonRaphson import *
import os
import pandas as pd


def generate_comparative_report(function, a, b, report_path, convergence_met=True, analytical_solution=None):
    """
    A function which generates reports for the provided function by using the numerical methods Regula Falsi and
    Newton Rhapson in the interval [a,b]. The function saves reports and visualizations plots under the folders
    Reports/report_path  and Visualizations/report_path
    :param function: The function to be solved by the two methods
    :param a: The left side of the interval
    :param b: The right side of the interval
    :param report_path: The name of the function under which to save the reports and plots
    :param convergence_met: Whether the function meets Newton-Rhapson convergence criterions
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

            if convergence_met:
                convergence_string = "Yes"
                if analytical_solution is not None:
                    if abs(solutions_reg[-1] - analytical_solution) <= precision:
                        precision_string_regula = "Yes"
                    else:
                        precision_string_regula = "No"
                    if abs(solutions_newt[-1] - analytical_solution) <= precision:
                        precision_string_newt = "Yes"
                    else:
                        precision_string_newt = "No"
                else:
                    precision_string_regula = precision_string_newt = "Yes"
            else:
                convergence_string = "No"
                precision_string_regula = precision_string_newt = "No"
            regula_row = pd.Series(data={'Function': function_print, 'a': a, 'b': b, 'Epsilon': precision,
                                         'Convergence Criterion': convergence_crit, "Method": "regula_falsi",
                                         'Solution': solution_regula['solution'][-1],
                                         'Number of iterations': solution_regula['num_iterations'],
                                         'Time elapsed': solution_regula['time_elapsed'],
                                         'Convergence': convergence_string,
                                         'Precision to analytical met': precision_string_regula})
            newt_raph_row = pd.Series(data={'Function': function_print, 'a': a, 'b': b, 'Epsilon': precision,
                                            'Convergence Criterion': convergence_crit, "Method": "newton_raphson",
                                            'Solution': solution_newton_raphson['solution'][-1],
                                            'Number of iterations': solution_newton_raphson['num_iterations'],
                                            'Time elapsed': solution_newton_raphson['time_elapsed'],
                                            'Convergence': convergence_string,
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
    analytical_sol = 1 - np.sqrt(3)
    generate_comparative_report(test_function, a, b, "starter_function", analytical_solution=analytical_sol)

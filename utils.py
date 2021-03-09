import inspect
from scipy.misc import derivative
import matplotlib.pyplot as plt
import numpy as np
import sys
import math


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
    return abs((x_curr - x_prev) / max(x_curr, 1e-6)) < epsilon


def convergence_criterion_4(epsilon, x_curr, function):
    """
    This function checks the 4th convergence criterion from slide 24 from Numericka matemtika del 4
    :param epsilon: Iterative process error, error/precision rate
    :param x_curr: X in iteration k (current iteration)
    :param function: The function for which the convergence criterion is checked
    :return: True/False
    """
    return abs(function(x_curr) / max(1e-6, derivative(function, x_curr, dx=1e-7))) < epsilon


def get_one_line_function_print(function):
    """
    A utility function which is used to print text inside one-liner commented functions. The function should be
    commented by the ''' scheme.
    :param function: The one-liner function to print
    :return: The one-liner text after the return keyword in the function
    """
    return inspect.getsource(function).split("return")[2].strip().split("\n")[0]


def plot_scatter_bi(x, y_1, y_2, x_label, y_label_1, y_label_2, title, outpath, y_limits):
    """
    Plots a (1,2) subplot scatterplot and saves the plot under outpath
    :param x: The x values
    :param y_1: The y values of the first subplot
    :param y_2: The y values of the second subplot
    :param x_label: The X label
    :param y_label_1: The Y label of the first subplot
    :param y_label_2: The Y label of the second subplot
    :param title: The title of the plot
    :param outpath: The path to which to save the plot
    :param y_limits: The limits(shared) of the y-axis of the 2 plots
    :return: None
    """
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.scatter(x, y_1, label=y_label_1, color="red",
                marker="*", s=60)
    ax2.scatter(x, y_2, label=y_label_2, color="green",
                marker="*", s=60)
    ax1.set(xlabel=x_label, ylabel=y_label_1)
    ax2.set(xlabel=x_label, ylabel=y_label_2)
    fig.suptitle(title)
    margins = plt.margins()
    new_margins = (margins[0] * 2, margins[1] * 2)
    ax1.margins(x=new_margins[0], y=new_margins[1])
    ax2.margins(x=new_margins[0], y=new_margins[1])
    if y_limits[0] != -math.inf and y_limits[1] != math.inf:
        plt.setp((ax1, ax2), xlim=(x[0] + 1e-2, x[-1] - 1e-2), ylim=y_limits)
    fig.savefig(outpath)


def plot_solutions(x_1, x_2, x_label_1, x_label_2, title, outpath, x_limits):
    """
    Plots a (1,2) subplot scatterplot and saves the plot under outpath for solutions
    :param x_1: Regula solutions
    :param x_2: Newton Raphson solutions
    :param x_label_1: The X label of the first subplot
    :param x_label_2: The X label of the second subplot
    :param title: The title of the plot
    :param outpath: The path to which to save the plot
    :param x_limits: The limits(shared) of the x-axis of the 2 plots
    :return: None
    """
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.scatter(x_1, range(len(x_1)), color="red", marker="*", s=60)
    ax2.scatter(x_2, range(len(x_2)), color="green", marker="*", s=60)
    y_label = "Iteration number"
    ax1.set(xlabel=x_label_1, ylabel=y_label)
    ax2.set(xlabel=x_label_2, ylabel=y_label)
    fig.suptitle(title)
    margins = plt.margins()
    new_margins = (margins[0] * 2, margins[1] * 2)
    ax1.margins(x=new_margins[0], y=new_margins[1])
    ax2.margins(x=new_margins[0], y=new_margins[1])
    if x_limits[0] != -math.inf and x_limits[1] != math.inf:
        plt.setp((ax1, ax2), xlim=x_limits)
    fig.savefig(outpath)


def plot_deltas(x_1, x_2, y_1, y_2, x_label_1, x_label_2, y_label_1, y_label_2, title, outpath, y_limits):
    """
    Plots a (1,2) subplot scatterplot and saves the plot under outpath for deltas
    :param y_limits: The limits(shared) of the y-axis of the 2 plots
    :param x_1: Regula number of iterations
    :param x_2: Newton number of iterations
    :param y_1: Regula deltas
    :param y_2: Newton Raphson deltas
    :param x_label_1: The X label of the first subplot
    :param x_label_2: The X label of the second subplot
    :param y_label_1: The Y label of the first subplot
    :param y_label_2: The Y label of the second subplot
    :param title: The title of the plot
    :param outpath: The path to which to save the plot
    :return: None
    """
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.scatter(x_1, y_1, color="red", marker="*", s=60)
    ax2.scatter(x_2, y_2, color="green", marker="*", s=60)
    ax1.set(xlabel=x_label_1, ylabel=y_label_1)
    ax2.set(xlabel=x_label_2, ylabel=y_label_2)
    fig.suptitle(title)
    margins = plt.margins()
    new_margins = (margins[0] * 2, margins[1] * 2)
    ax1.margins(x=new_margins[0], y=new_margins[1])
    ax2.margins(x=new_margins[0], y=new_margins[1])
    if y_limits[0] != -math.inf and y_limits[1] != math.inf:
        plt.setp((ax1, ax2), ylim=y_limits)
    fig.savefig(outpath)


def plot_function(function, a, b, function_print, outpath):
    """
    Plots the provided function in the interval [a,b] and saves the plot in outpath
    :param function: To function to plot
    :param a: Left side of the interval
    :param b: Rights side of the interval
    :param function_print: The name of the function
    :param outpath: The path to save the plot in
    :return: None
    """
    plt.figure(figsize=(15, 10))
    points = np.arange(a, b, 0.001)
    vals = [function(point) for point in points]
    plt.plot(points, vals)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(function_print)
    plt.savefig(outpath)

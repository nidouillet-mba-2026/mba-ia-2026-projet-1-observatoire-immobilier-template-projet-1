"""
Fonctions statistiques from scratch.
Reference : Joel Grus, "Data Science From Scratch", chapitre 5.

IMPORTANT : N'importez pas numpy, pandas ou statistics pour ces fonctions.
Implementez-les avec du Python pur (listes, boucles, math).
"""

import math


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def median(xs: list[float]) -> float:
    sorted_xs = sorted(xs)
    n = len(sorted_xs)
    mid = n // 2
    if n % 2 == 1:
        return sorted_xs[mid]
    return (sorted_xs[mid - 1] + sorted_xs[mid]) / 2


def variance(xs: list[float]) -> float:
    n = len(xs)
    x_bar = mean(xs)
    return sum((x - x_bar) ** 2 for x in xs) / n


def standard_deviation(xs: list[float]) -> float:
    return math.sqrt(variance(xs))


def covariance(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    x_bar = mean(xs)
    y_bar = mean(ys)
    return sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys)) / n


def correlation(xs: list[float], ys: list[float]) -> float:
    sd_x = standard_deviation(xs)
    sd_y = standard_deviation(ys)
    if sd_x == 0 or sd_y == 0:
        return 0
    return covariance(xs, ys) / (sd_x * sd_y)

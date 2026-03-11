import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.regression import predict, error, sum_of_sqerrors, least_squares_fit, r_squared


def test_predict_basic():
    assert predict(1, 2, 3) == 7


def test_predict_zero_beta():
    assert predict(5, 0, 10) == 5


def test_error_basic():
    assert error(1, 2, 3, 8) == 1


def test_error_zero():
    assert error(1, 2, 3, 7) == 0


def test_sum_of_sqerrors_perfect_fit():
    x = [1, 2, 3]
    y = [3, 5, 7]  # y = 1 + 2x
    assert sum_of_sqerrors(1, 2, x, y) == 0


def test_sum_of_sqerrors_non_zero():
    x = [1, 2, 3]
    y = [4, 6, 8]
    assert sum_of_sqerrors(1, 2, x, y) > 0


def test_least_squares_fit_basic():
    x = [1, 2, 3]
    y = [3, 5, 7]  # y = 1 + 2x

    alpha, beta = least_squares_fit(x, y)

    assert abs(alpha - 1.0) < 0.01
    assert abs(beta - 2.0) < 0.01


def test_least_squares_fit_horizontal_line():
    x = [1, 2, 3, 4]
    y = [5, 5, 5, 5]

    alpha, beta = least_squares_fit(x, y)

    assert abs(alpha - 5.0) < 0.01
    assert abs(beta - 0.0) < 0.01


def test_r_squared_perfect_fit():
    x = [1, 2, 3]
    y = [3, 5, 7]

    alpha, beta = least_squares_fit(x, y)

    assert abs(r_squared(alpha, beta, x, y) - 1.0) < 0.01


def test_r_squared_constant_y():
    x = [1, 2, 3]
    y = [5, 5, 5]

    assert r_squared(5, 0, x, y) == 0


def test_least_squares_fit_zero_variance():
    x = [2, 2, 2]
    y = [1, 2, 3]

    try:
        least_squares_fit(x, y)
        assert False
    except ValueError:
        assert True
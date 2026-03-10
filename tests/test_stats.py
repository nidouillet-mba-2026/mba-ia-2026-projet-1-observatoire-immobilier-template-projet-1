import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.stats import mean, median, variance, standard_deviation, covariance, correlation


def test_mean_basic():
    assert mean([1, 2, 3, 4, 5]) == 3.0


def test_mean_two_elements():
    assert mean([10, 20]) == 15.0


def test_mean_single():
    assert mean([7]) == 7.0


def test_median_odd():
    assert median([1, 2, 3, 4, 5]) == 3


def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_unsorted():
    assert median([5, 1, 3]) == 3


def test_median_single():
    assert median([42]) == 42


def test_variance_known():
    assert abs(variance([2, 4, 4, 4, 5, 5, 7, 9]) - 4.0) < 0.1


def test_variance_identical():
    assert variance([5, 5, 5, 5]) == 0.0


def test_standard_deviation_known():
    assert abs(standard_deviation([2, 4, 4, 4, 5, 5, 7, 9]) - 2.0) < 0.1


def test_standard_deviation_identical():
    assert standard_deviation([5, 5, 5, 5]) == 0.0


def test_covariance_identical_series():
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert abs(covariance(xs, xs) - variance(xs)) < 0.001


def test_covariance_negative():
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [5.0, 4.0, 3.0, 2.0, 1.0]
    assert covariance(xs, ys) < 0


def test_correlation_perfect_positive():
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert abs(correlation(xs, xs) - 1.0) < 0.01


def test_correlation_perfect_negative():
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [5.0, 4.0, 3.0, 2.0, 1.0]
    assert abs(correlation(xs, ys) - (-1.0)) < 0.01


def test_correlation_zero_std():
    xs = [1.0, 2.0, 3.0]
    ys = [5.0, 5.0, 5.0]
    assert correlation(xs, ys) == 0

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.scoring import (
    distance,
    knn_similar,
    price_per_sqm,
    neighborhood_median_sqm,
    gap_ratio,
    classify,
    opportunity_score,
)


def test_distance_same_point():
    assert distance([0, 0], [0, 0]) == 0.0


def test_distance_known_value():
    assert abs(distance([0, 0], [3, 4]) - 5.0) < 0.001


def test_distance_single_dimension():
    assert abs(distance([1], [4]) - 3.0) < 0.001


def test_knn_similar_returns_k_neighbors():
    dataset = [[1], [2], [3], [10], [11]]
    labels = ["A", "A", "A", "B", "B"]
    result = knn_similar([2], dataset, labels, k=3)
    assert len(result) == 3
    assert result.count("A") == 3


def test_knn_similar_closest_first():
    dataset = [[10], [1], [5]]
    labels = ["far", "close", "mid"]
    result = knn_similar([0], dataset, labels, k=2)
    assert result[0] == "close"


def test_price_per_sqm_normal():
    assert price_per_sqm(200000, 50) == 4000.0


def test_price_per_sqm_zero_surface():
    assert price_per_sqm(200000, 0) == 0.0


def test_price_per_sqm_negative_surface():
    assert price_per_sqm(200000, -10) == 0.0


def test_gap_ratio_underpriced():
    ratio = gap_ratio(180000, 200000)
    assert abs(ratio - (-0.10)) < 0.001


def test_gap_ratio_overpriced():
    ratio = gap_ratio(220000, 200000)
    assert abs(ratio - 0.10) < 0.001


def test_gap_ratio_zero_estimated():
    assert gap_ratio(100000, 0) == 0.0


def test_classify_opportunite():
    assert classify(-0.15) == "Opportunite"


def test_classify_surevalue():
    assert classify(0.20) == "Surevalue"


def test_classify_prix_marche():
    assert classify(0.0) == "Prix marche"
    assert classify(0.10) == "Prix marche"
    assert classify(-0.10) == "Prix marche"

import math

from analysis.stats import mean, median, standard_deviation
from analysis.regression import predict


def distance(v1: list[float], v2: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def knn_similar(
    target: list[float],
    dataset: list[list[float]],
    labels: list,
    k: int = 5,
) -> list:
    neighbors = sorted(
        zip(dataset, labels),
        key=lambda pair: distance(target, pair[0]),
    )
    return [label for _, label in neighbors[:k]]


def price_per_sqm(price: float, surface: float) -> float:
    if surface <= 0:
        return 0.0
    return price / surface


def neighborhood_median_sqm(prices: list[float], surfaces: list[float]) -> float:
    sqm_prices = [
        price_per_sqm(p, s) for p, s in zip(prices, surfaces) if s > 0
    ]
    if not sqm_prices:
        return 0.0
    return median(sqm_prices)


def gap_ratio(announced_price: float, estimated_price: float) -> float:
    if estimated_price <= 0:
        return 0.0
    return (announced_price - estimated_price) / estimated_price


def classify(ratio: float) -> str:
    if ratio < -0.10:
        return "Opportunite"
    elif ratio > 0.10:
        return "Surevalue"
    return "Prix marche"


def opportunity_score(
    announced_price: float,
    surface: float,
    alpha: float,
    beta: float,
    neighborhood_prices: list[float],
    neighborhood_surfaces: list[float],
) -> dict:
    estimated = predict(alpha, beta, surface)
    ratio = gap_ratio(announced_price, estimated)
    category = classify(ratio)

    med_sqm = neighborhood_median_sqm(neighborhood_prices, neighborhood_surfaces)
    ann_sqm = price_per_sqm(announced_price, surface)

    if med_sqm > 0:
        market_ratio = ann_sqm / med_sqm
    else:
        market_ratio = 1.0

    regression_score = max(0.0, min(50.0, 50.0 * (1.0 - ratio)))
    market_score = max(0.0, min(25.0, 25.0 * (2.0 - market_ratio)))
    base_score = regression_score + market_score

    score = max(0.0, min(100.0, base_score))

    return {
        "score": round(score, 1),
        "category": category,
        "estimated_price": round(estimated, 2),
        "gap_ratio": round(ratio, 4),
        "price_per_sqm": round(ann_sqm, 2),
        "median_sqm": round(med_sqm, 2),
    }

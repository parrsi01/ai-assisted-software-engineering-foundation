"""
Module 08: Data Science and Algorithms — Solutions
Uses stdlib + numpy + pandas where available, falls back to stdlib.
"""
import math
import statistics
from collections import Counter


# --- Statistics from scratch (stdlib only) ---

def mean(data: list[float]) -> float:
    return sum(data) / len(data)


def median(data: list[float]) -> float:
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return float(sorted_data[mid])


def mode(data: list) -> list:
    """Return all modes (most frequent values) as a sorted list."""
    counts = Counter(data)
    max_count = max(counts.values())
    return sorted(k for k, v in counts.items() if v == max_count)


def variance(data: list[float], population: bool = True) -> float:
    """Population variance (ddof=0) or sample variance (ddof=1)."""
    m = mean(data)
    n = len(data)
    ddof = 0 if population else 1
    return sum((x - m) ** 2 for x in data) / (n - ddof)


def std_dev(data: list[float], population: bool = True) -> float:
    return math.sqrt(variance(data, population))


def pearson_correlation(x: list[float], y: list[float]) -> float:
    """Pearson r: measures linear correlation between x and y."""
    assert len(x) == len(y) and len(x) > 1
    mx, my = mean(x), mean(y)
    numerator = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    denom = math.sqrt(
        sum((xi - mx) ** 2 for xi in x) *
        sum((yi - my) ** 2 for yi in y)
    )
    return numerator / denom if denom != 0 else 0.0


def z_score(value: float, data: list[float]) -> float:
    """Number of standard deviations value is from the mean."""
    m = mean(data)
    s = std_dev(data, population=True)
    return (value - m) / s if s != 0 else 0.0


def normalize_minmax(data: list[float]) -> list[float]:
    """Scale data to [0, 1] range."""
    lo, hi = min(data), max(data)
    if hi == lo:
        return [0.0] * len(data)
    return [(x - lo) / (hi - lo) for x in data]


# --- Data cleaning ---

def remove_outliers_iqr(data: list[float]) -> list[float]:
    """Remove values outside 1.5 * IQR from Q1 and Q3."""
    sorted_data = sorted(data)
    n = len(sorted_data)
    q1 = median(sorted_data[:n // 2])
    q3 = median(sorted_data[(n + 1) // 2:])
    iqr = q3 - q1
    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr
    return [x for x in data if lo <= x <= hi]


def fill_missing(data: list, strategy: str = "mean") -> list:
    """Replace None values with mean, median, or mode of non-None values."""
    clean = [x for x in data if x is not None]
    if not clean:
        return data
    if strategy == "mean":
        fill = mean(clean)
    elif strategy == "median":
        fill = median(clean)
    elif strategy == "mode":
        fill = mode(clean)[0]
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    return [fill if x is None else x for x in data]


# --- Time series ---

def moving_average(data: list[float], window: int) -> list[float]:
    """Simple moving average. Output length = len(data) - window + 1."""
    return [
        mean(data[i:i + window])
        for i in range(len(data) - window + 1)
    ]


def exponential_moving_average(data: list[float], alpha: float = 0.3) -> list[float]:
    """EMA: weights recent values more heavily. alpha in (0, 1)."""
    ema = [data[0]]
    for x in data[1:]:
        ema.append(alpha * x + (1 - alpha) * ema[-1])
    return ema


def detect_trend(data: list[float]) -> str:
    """Simple linear trend detection using Pearson r with time index."""
    n = len(data)
    time_idx = list(range(n))
    r = pearson_correlation(time_idx, data)
    if r > 0.7:
        return "upward"
    elif r < -0.7:
        return "downward"
    return "no clear trend"


# --- Frequency analysis ---

def frequency_table(data: list) -> list[tuple]:
    """Return sorted (value, count, percentage) tuples."""
    counts = Counter(data)
    total = len(data)
    return sorted(
        [(val, cnt, 100 * cnt / total) for val, cnt in counts.items()],
        key=lambda x: -x[1],
    )


if __name__ == "__main__":
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    assert mean(data) == 5.0
    assert median(data) == 4.5
    assert mode(data) == [4]
    assert abs(variance(data) - 3.5) < 1e-9
    assert abs(std_dev(data) - math.sqrt(3.5)) < 1e-9

    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    assert abs(pearson_correlation(x, y) - 1.0) < 1e-9  # perfect linear

    normalized = normalize_minmax([0, 5, 10])
    assert normalized == [0.0, 0.5, 1.0]

    data_with_none = [1.0, None, 3.0, None, 5.0]
    filled = fill_missing(data_with_none, "mean")
    assert all(x is not None for x in filled)
    assert filled[1] == mean([1.0, 3.0, 5.0])

    ma = moving_average([1, 2, 3, 4, 5], 3)
    assert ma == [2.0, 3.0, 4.0]

    trend = detect_trend([1, 2, 3, 4, 5, 6, 7, 8])
    assert trend == "upward"

    freq = frequency_table(["a", "b", "a", "c", "a"])
    assert freq[0][0] == "a" and freq[0][1] == 3

    print("All assertions passed.")

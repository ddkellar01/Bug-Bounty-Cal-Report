"""CVSS v3.1 base-score calculator.

Parses a CVSS:3.1 (or 3.0) vector string and computes the base score and
severity rating using the official FIRST.org equations, including the
spec-defined roundup. Pure stdlib, no dependencies.

Usage:
    calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    -> {"base_score": 9.8, "severity": "Critical", ...}

    calculate_cvss(av="N", ac="L", pr="N", ui="N", s="U",
                   c="H", i="H", a="H")   # same result, metric kwargs
"""

from __future__ import annotations

import math

# Metric value weights (CVSS v3.1 specification, FIRST.org).
AV_WEIGHTS = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}
AC_WEIGHTS = {"L": 0.77, "H": 0.44}
UI_WEIGHTS = {"N": 0.85, "R": 0.62}
CIA_WEIGHTS = {"H": 0.56, "L": 0.22, "N": 0.00}
# Privileges Required depends on Scope.
PR_WEIGHTS = {
    "U": {"N": 0.85, "L": 0.62, "H": 0.27},
    "C": {"N": 0.85, "L": 0.68, "H": 0.50},
}

METRIC_ORDER = ("AV", "AC", "PR", "UI", "S", "C", "I", "A")
VALID_VALUES = {
    "AV": set(AV_WEIGHTS),
    "AC": set(AC_WEIGHTS),
    "PR": {"N", "L", "H"},
    "UI": set(UI_WEIGHTS),
    "S": {"U", "C"},
    "C": set(CIA_WEIGHTS),
    "I": set(CIA_WEIGHTS),
    "A": set(CIA_WEIGHTS),
}


def severity_rating(score: float) -> str:
    """Map a CVSS base score to its qualitative severity rating."""
    if score <= 0.0:
        return "None"
    if score < 4.0:
        return "Low"
    if score < 7.0:
        return "Medium"
    if score < 9.0:
        return "High"
    return "Critical"


def _roundup(value: float) -> float:
    """CVSS spec roundup: smallest 1-decimal number >= value (100000 scale)."""
    int_input = int(round(value * 100000))
    if int_input % 10000 == 0:
        return int_input / 100000.0
    return (math.floor(int_input / 10000) + 1) / 10.0


def parse_vector(vector: str) -> dict:
    """Parse 'CVSS:3.1/AV:N/AC:L/...' into a metrics dict. Raises ValueError."""
    if not isinstance(vector, str) or not vector.strip():
        raise ValueError("CVSS vector must be a non-empty string")
    parts = vector.strip().split("/")
    header = parts[0].upper()
    if header not in ("CVSS:3.1", "CVSS:3.0"):
        raise ValueError(
            f"Unsupported vector header {parts[0]!r}: expected CVSS:3.1 or CVSS:3.0"
        )
    metrics = {}
    for part in parts[1:]:
        if ":" not in part:
            raise ValueError(f"Malformed vector segment {part!r}")
        key, _, raw = part.partition(":")
        key = key.strip().upper()
        raw = raw.strip().upper()
        if key not in VALID_VALUES:
            raise ValueError(f"Unknown CVSS metric {key!r}")
        if raw not in VALID_VALUES[key]:
            raise ValueError(f"Invalid value {raw!r} for metric {key}")
        metrics[key] = raw
    missing = [m for m in METRIC_ORDER if m not in metrics]
    if missing:
        raise ValueError(f"Vector is missing required metrics: {', '.join(missing)}")
    return metrics


def build_vector(metrics: dict) -> str:
    """Rebuild the canonical CVSS:3.1 vector string from a metrics dict."""
    return "CVSS:3.1/" + "/".join(f"{m}:{metrics[m]}" for m in METRIC_ORDER)


def _base_score(metrics: dict) -> float:
    scope = metrics["S"]
    av = AV_WEIGHTS[metrics["AV"]]
    ac = AC_WEIGHTS[metrics["AC"]]
    pr = PR_WEIGHTS[scope][metrics["PR"]]
    ui = UI_WEIGHTS[metrics["UI"]]
    c = CIA_WEIGHTS[metrics["C"]]
    i = CIA_WEIGHTS[metrics["I"]]
    a = CIA_WEIGHTS[metrics["A"]]

    isc = 1.0 - ((1.0 - c) * (1.0 - i) * (1.0 - a))
    if scope == "U":
        impact = 6.42 * isc
    else:
        impact = 7.52 * (isc - 0.029) - 3.25 * ((isc - 0.02) ** 15)
    exploitability = 8.22 * av * ac * pr * ui

    if impact <= 0:
        return 0.0
    if scope == "U":
        return _roundup(min(impact + exploitability, 10.0))
    return _roundup(min(1.08 * (impact + exploitability), 10.0))


def calculate_cvss(vector: str = None, **metric_kwargs) -> dict:
    """Compute the CVSS v3.1 base score.

    Pass either a full vector string or metric keyword arguments
    (av, ac, pr, ui, s, c, i, a). Returns a dict with base_score,
    severity, canonical vector string, and the parsed metrics.
    """
    if vector is not None and metric_kwargs:
        raise ValueError("Pass either a vector string or metric kwargs, not both")
    if vector is None:
        if not metric_kwargs:
            raise ValueError("No CVSS vector or metrics supplied")
        metrics = {}
        for key, raw in metric_kwargs.items():
            k = key.strip().upper()
            if k not in VALID_VALUES:
                raise ValueError(f"Unknown CVSS metric {key!r}")
            v = str(raw).strip().upper()
            if v not in VALID_VALUES[k]:
                raise ValueError(f"Invalid value {raw!r} for metric {k}")
            metrics[k] = v
        missing = [m for m in METRIC_ORDER if m not in metrics]
        if missing:
            raise ValueError(f"Missing required metrics: {', '.join(missing)}")
    else:
        metrics = parse_vector(vector)

    score = _base_score(metrics)
    return {
        "base_score": score,
        "severity": severity_rating(score),
        "vector": build_vector(metrics),
        "version": "3.1",
        "metrics": metrics,
    }
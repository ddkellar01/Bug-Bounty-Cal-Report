"""Engine tests: CVSS calculator against known FIRST.org reference scores."""

from src.modules.cvss_calculator import calculate_cvss, severity_rating

import pytest


def test_critical_network_vector_scores_9_8():
    result = calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    assert result["base_score"] == 9.8
    assert result["severity"] == "Critical"


def test_scope_changed_full_impact_scores_10_0():
    result = calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H")
    assert result["base_score"] == 10.0
    assert result["severity"] == "Critical"


def test_no_impact_scores_0_0():
    result = calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N")
    assert result["base_score"] == 0.0
    assert result["severity"] == "None"


def test_confidentiality_only_scores_7_5():
    result = calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N")
    assert result["base_score"] == 7.5
    assert result["severity"] == "High"


def test_reflected_xss_pattern_scores_6_1():
    result = calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N")
    assert result["base_score"] == 6.1
    assert result["severity"] == "Medium"


def test_metric_kwargs_match_vector_string():
    by_vector = calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    by_kwargs = calculate_cvss(
        av="N", ac="L", pr="N", ui="N", s="U", c="H", i="H", a="H"
    )
    assert by_kwargs["base_score"] == by_vector["base_score"]
    assert by_kwargs["vector"] == by_vector["vector"]


def test_invalid_vector_raises():
    with pytest.raises(ValueError):
        calculate_cvss("CVSS:3.1/AV:Z/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")


def test_missing_metrics_raise():
    with pytest.raises(ValueError):
        calculate_cvss("CVSS:3.1/AV:N/AC:L")


def test_severity_bands():
    assert severity_rating(0.0) == "None"
    assert severity_rating(3.9) == "Low"
    assert severity_rating(4.0) == "Medium"
    assert severity_rating(7.0) == "High"
    assert severity_rating(9.0) == "Critical"
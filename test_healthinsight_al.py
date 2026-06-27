import pytest
from HealthInsight_AI import User, HealthAnalyzer


def test_bmi():
    user = User("Harsh", 18, 70, 175, 2.5, 8)
    analyzer = HealthAnalyzer(user)
    assert round(analyzer.bmi(), 2) == 22.86


def test_bmi_status_normal():
    user = User("Harsh", 18, 70, 175, 2.5, 8)
    analyzer = HealthAnalyzer(user)
    assert analyzer.bmi_status() == "Normal weight"


def test_bmi_status_underweight():
    user = User("Harsh", 18, 45, 170, 2.5, 8)
    analyzer = HealthAnalyzer(user)
    assert analyzer.bmi_status() == "Under weight"


def test_health_score_perfect():
    user = User("Harsh", 18, 70, 175, 2.5, 8)
    analyzer = HealthAnalyzer(user)
    assert analyzer.health_score() == 100


def test_health_score_low():
    user = User("Harsh", 18, 90, 170, 1.5, 6)
    analyzer = HealthAnalyzer(user)
    assert analyzer.health_score() == 65


def test_recommendations():
    user = User("Harsh", 18, 90, 170, 1.5, 6)
    analyzer = HealthAnalyzer(user)

    assert "Increase physical activity." in analyzer.recommendations()
    assert "Sleep at least 7-9 hours." in analyzer.recommendations()
    assert "Drink more water" in analyzer.recommendations()


def test_ai_insight():
    user = User("Harsh", 18, 70, 175, 2.5, 8)
    analyzer = HealthAnalyzer(user)

    insight = analyzer.ai_insight()

    assert "Harsh" in insight
    assert "BMI" in insight
    assert "health score" in insight

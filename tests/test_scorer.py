from scorer import (
    calculate_final_score,
    get_decision
)


def test_final_score():

    score = calculate_final_score(
        critical_skill_score=80,
        supporting_skill_score=70,
        semantic_score=75,
        education_score=100,
        experience_score=100
    )

    assert 0 <= score <= 100


def test_strong_match():

    assert get_decision(85) == "Strong Match"


def test_good_match():

    assert get_decision(70) == "Good Match"


def test_moderate_match():

    assert get_decision(55) == "Moderate Match"


def test_weak_match():

    assert get_decision(40) == "Weak Match"
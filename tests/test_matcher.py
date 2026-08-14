from matcher import (
    skill_matches,
    calculate_critical_skill_score
)


def test_skill_matches():

    resume_skills = [
        "Python",
        "SQL",
        "FastAPI"
    ]

    assert skill_matches(
        "Python",
        resume_skills
    )


def test_skill_does_not_match():

    resume_skills = [
        "Python",
        "SQL"
    ]

    assert not skill_matches(
        "Java",
        resume_skills
    )


def test_critical_skill_score():

    required_skills = [
        "Python",
        "SQL"
    ]

    resume_skills = [
        "Python"
    ]

    result = calculate_critical_skill_score(
        required_skills,
        resume_skills
    )

    assert 0 <= result["critical_score"] <= 100
from aliases import expand_aliases
from semantic import analyze, label


def test_alias_expands_ml():
    assert "machine learning" in expand_aliases("I know ML")


def test_label_cutoffs():
    assert label(0.60) == "COVERED"
    assert label(0.40) == "PARTIAL"
    assert label(0.20) == "GAP"


def test_unrelated_job_is_never_strong_match():
    resume = "I build data dashboards with SQL and Excel for a retail team."
    job = ("Prepare fresh pasta and sauces daily in a busy restaurant kitchen. "
           "Maintain food safety standards at all times.")
    results = analyze(resume, job)
    assert all(score < 0.5 for status, score, text, evidence in results)
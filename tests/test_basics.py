from aliases import expand_aliases
from semantic import analyze, label
from semantic import get_job_chunks

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

def test_relevant_line_raises_score():
    job = "Hands-on experience building and training deep learning models in PyTorch."
    base = "I build data dashboards with SQL and Excel for a retail team."
    extra = base + "\nBuilt an image classifier in PyTorch and trained it on a small dataset."
    score_without = analyze(base, job)[0][1]
    score_with = analyze(extra, job)[0][1]
    assert score_with > score_without


def test_ml_abbreviation_matches_machine_learning():
    resume = "I have trained several ML models for classification tasks."
    job = "Experience with machine learning models and classification."
    results = analyze(resume, job)
    assert results[0][1] > 0.5


def test_headings_and_pay_lines_are_dropped():
    text = ("WHAT WE'RE LOOKING FOR\n"
            "Compensation: INR 25,000 per month\n"
            "Good to Have Skills:\n"
            "Experience building models in Python and SQL.")
    chunks = get_job_chunks(text)
    assert len(chunks) == 1


def test_empty_job_does_not_crash():
    results = analyze("I build data dashboards with SQL and Excel.", "")
    assert results == []
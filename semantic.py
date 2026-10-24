from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from chunks import split_into_chunks
from aliases import expand_aliases

model = SentenceTransformer("all-MiniLM-L6-v2")


def label(score):
    if score >= 0.50:
        return "COVERED"
    if score >= 0.35:
        return "PARTIAL"
    return "GAP"

SKIP_STARTS = ("compensation", "work hours", "location", "employment", "remote work",
               "minimum cgpa", "only students", "no salary", "experience level",
               "potential next step", "must be available")


def get_job_chunks(path):
    text = Path(path).read_text(encoding="utf-8")
    chunks = split_into_chunks(text)
    chunks = [c for c in chunks
              if not c.endswith(":")
              and not c.isupper()
              and "|" not in c
              and not c.lower().startswith(SKIP_STARTS)]
    return [expand_aliases(c) for c in chunks]


# Resume: prepared once
resume = expand_aliases(Path("private/resume.txt").read_text(encoding="utf-8"))
resume_chunks = split_into_chunks(resume)
resume_chunks = [c for c in resume_chunks if not c.lower().startswith(("interests", "hobbies"))]
resume_emb = model.encode(resume_chunks)

# Jobs: one report per file
for job_file in sorted(Path("private/jobs").glob("*.txt")):
    # YOUR TURN: replace the ... below with code that reads this job file
    # and expands aliases. Hint: matcher.py already reads a job_file.
    job_chunks = get_job_chunks(job_file)
    job_emb = model.encode(job_chunks)
    sims = util.cos_sim(job_emb, resume_emb)

    results = []
    print(f"\n===== {job_file.name} =====")
    for i, job_chunk in enumerate(job_chunks):
        best = sims[i].argmax().item()
        score = sims[i][best].item()
        status = label(score)
        results.append((status, score, job_chunk))
        print(f"[{status:7}] {score:.2f} | {job_chunk[:70]}")
        if status != "GAP":
            print(f"            evidence: {resume_chunks[best][:70]}")

    covered = sum(1 for r in results if r[0] == "COVERED")
    partial = sum(1 for r in results if r[0] == "PARTIAL")
    gaps = [r for r in results if r[0] == "GAP"]

    print(f"\nSUMMARY: {covered} covered, {partial} partial, {len(gaps)} gaps out of {len(results)} requirements")
    print("BIGGEST GAPS:")
    for _, score, text in sorted(gaps, key=lambda r: r[1])[:5]:
        print(f"  {score:.2f} | {text[:70]}")
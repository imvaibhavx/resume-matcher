from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from chunks import split_into_chunks
from aliases import expand_aliases

model = SentenceTransformer("all-MiniLM-L6-v2")

SKIP_STARTS = ("compensation", "work hours", "location", "employment", "remote work",
               "minimum cgpa", "only students", "no salary", "experience level",
               "potential next step", "must be available")


def label(score):
    if score >= 0.50:
        return "COVERED"
    if score >= 0.35:
        return "PARTIAL"
    return "GAP"


def get_job_chunks(text):
    chunks = split_into_chunks(text)
    chunks = [c for c in chunks
              if not c.endswith(":")
              and not c.isupper()
              and "|" not in c
              and not c.lower().startswith(SKIP_STARTS)]
    return [expand_aliases(c) for c in chunks]


def get_resume_chunks(text):
    chunks = split_into_chunks(text)
    chunks = [c for c in chunks if not c.lower().startswith(("interests", "hobbies"))]
    return [expand_aliases(c) for c in chunks]


def match_requirements(job_chunks, resume_chunks, resume_emb):
    job_emb = model.encode(job_chunks)
    sims = util.cos_sim(job_emb, resume_emb)
    results = []
    for i, job_chunk in enumerate(job_chunks):
        best = sims[i].argmax().item()
        score = sims[i][best].item()
        status = label(score)
        evidence = resume_chunks[best] if status != "GAP" else ""
        results.append((status, score, job_chunk, evidence))
    return results


def analyze(resume_text, job_text):
    resume_chunks = get_resume_chunks(resume_text)
    resume_emb = model.encode(resume_chunks)
    job_chunks = get_job_chunks(job_text)
    return match_requirements(job_chunks, resume_chunks, resume_emb)


if __name__ == "__main__":
    resume_text = Path("private/resume.txt").read_text(encoding="utf-8")
    resume_chunks = get_resume_chunks(resume_text)
    resume_emb = model.encode(resume_chunks)

    for job_file in sorted(Path("private/jobs").glob("*.txt")):
        job_text = job_file.read_text(encoding="utf-8")
        job_chunks = get_job_chunks(job_text)
        results = match_requirements(job_chunks, resume_chunks, resume_emb)

        print(f"\n===== {job_file.name} =====")
        for status, score, text, evidence in results:
            print(f"[{status:7}] {score:.2f} | {text[:70]}")
            if evidence:
                print(f"            evidence: {evidence[:70]}")

        covered = sum(1 for r in results if r[0] == "COVERED")
        partial = sum(1 for r in results if r[0] == "PARTIAL")
        gaps = [r for r in results if r[0] == "GAP"]

        print(f"\nSUMMARY: {covered} covered, {partial} partial, {len(gaps)} gaps out of {len(results)} requirements")
        print("BIGGEST GAPS:")
        for r in sorted(gaps, key=lambda r: r[1])[:5]:
            print(f"  {r[1]:.2f} | {r[2][:70]}")
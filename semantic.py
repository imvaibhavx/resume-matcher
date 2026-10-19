from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from chunks import split_into_chunks
from aliases import expand_aliases

model = SentenceTransformer("all-MiniLM-L6-v2")

resume = expand_aliases(Path("private/resume.txt").read_text(encoding="utf-8"))
job = expand_aliases(Path("private/jobs/job1.txt").read_text(encoding="utf-8"))

resume_chunks = split_into_chunks(resume)
job_chunks = split_into_chunks(job)

resume_chunks = [c for c in resume_chunks if not c.lower().startswith(("interests", "hobbies"))]
job_chunks = [c for c in job_chunks if not c.endswith(":")]

resume_emb = model.encode(resume_chunks)
job_emb = model.encode(job_chunks)

sims = util.cos_sim(job_emb, resume_emb)

def label(score):
    if score >= 0.50:
        return "COVERED"
    if score >= 0.35:
        return "PARTIAL"
    return "GAP"


for i, job_chunk in enumerate(job_chunks):
    best = sims[i].argmax().item()
    score = sims[i][best].item()
    status = label(score)
    print(f"[{status:7}] {score:.2f} | {job_chunk[:70]}")
    if status != "GAP":
        print(f"            evidence: {resume_chunks[best][:70]}")
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from chunks import split_into_chunks

model = SentenceTransformer("all-MiniLM-L6-v2")

resume = Path("private/resume.txt").read_text(encoding="utf-8")
job = Path("private/jobs/job1.txt").read_text(encoding="utf-8")

resume_chunks = split_into_chunks(resume)
job_chunks = split_into_chunks(job)

resume_emb = model.encode(resume_chunks)
job_emb = model.encode(job_chunks)

sims = util.cos_sim(job_emb, resume_emb)

for i, job_chunk in enumerate(job_chunks):
    best = sims[i].argmax().item()
    score = sims[i][best].item()
    print(f"{score:.2f} | {job_chunk[:70]}")
    print(f"       closest resume line: {resume_chunks[best][:70]}")
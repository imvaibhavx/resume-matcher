from pathlib import Path
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

resume = Path("samples/resume.txt").read_text(encoding="utf-8")
resume_embedding = model.encode(resume)

for job_file in sorted(Path("samples/jobs").glob("*.txt")):
    job = job_file.read_text(encoding="utf-8")
    job_embedding = model.encode(job)
    score = util.cos_sim(resume_embedding, job_embedding).item()
    print(f"{job_file.name}: {score:.2f}")
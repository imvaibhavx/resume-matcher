from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from skills import load_skills, find_skills

model = SentenceTransformer("all-MiniLM-L6-v2")
skills = load_skills()

resume = Path("samples/resume.txt").read_text(encoding="utf-8")
resume_embedding = model.encode(resume)
resume_skills = find_skills(resume, skills)

for job_file in sorted(Path("samples/jobs").glob("*.txt")):
    job = job_file.read_text(encoding="utf-8")
    score = util.cos_sim(resume_embedding, model.encode(job)).item()
    job_skills = find_skills(job, skills)
    matched = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)

    print(f"\n{job_file.name} | match score: {score:.2f}")
    print(f"  Skills matched ({len(matched)}/{len(job_skills)}): {', '.join(matched) or 'none'}")
    print(f"  Skills missing: {', '.join(missing) or 'none'}")
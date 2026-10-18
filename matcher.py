from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from skills import load_skills, find_skills

model = SentenceTransformer("all-MiniLM-L6-v2")
skills = load_skills()

resume = Path("samples/resume.txt").read_text(encoding="utf-8")
resume_embedding = model.encode(resume)
resume_skills = find_skills(resume, skills)

results = []
for job_file in sorted(Path("samples/jobs").glob("*.txt")):
    job = job_file.read_text(encoding="utf-8")
    score = util.cos_sim(resume_embedding, model.encode(job)).item()
    job_skills = find_skills(job, skills)
    matched = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)
    results.append((score, job_file.name, matched, missing))

results.sort(reverse=True)

print("\n=== RESUME MATCH REPORT ===")
for rank, (score, name, matched, missing) in enumerate(results, start=1):
    print(f"\n#{rank}  {name}  (match score: {score:.2f})")
    print(f"   Matched ({len(matched)}): {', '.join(matched) or 'none'}")
    print(f"   Missing ({len(missing)}): {', '.join(missing) or 'none'}")
import re
from pathlib import Path


def load_skills(path="skills.txt"):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return [line.strip().lower() for line in lines if line.strip()]


def find_skills(text, skills):
    text = text.lower()
    found = set()
    for skill in skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.add(skill)
    return found


if __name__ == "__main__":
    skills = load_skills()
    resume = Path("samples/resume.txt").read_text(encoding="utf-8")
    resume_skills = find_skills(resume, skills)

    for job_file in sorted(Path("samples/jobs").glob("*.txt")):
        job = job_file.read_text(encoding="utf-8")
        job_skills = find_skills(job, skills)

        matched = job_skills & resume_skills
        missing = job_skills - resume_skills

        print(f"\n{job_file.name}")
        print("  matched:", sorted(matched))
        print("  missing:", sorted(missing))
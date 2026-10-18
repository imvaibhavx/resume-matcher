# Resume-to-Job Matcher

An AI tool that compares your resume against a job description and tells you how well you match, which skills you're missing, and what to improve before you apply.

## Why I'm building this

Job applications are a guessing game: you never know what's missing until you get rejected. This tool makes that gap visible before you hit submit. I'm building it to learn applied NLP and take a real AI project from idea to deployment.

## How it will work

1. Paste your resume and a job description
2. The tool converts both into text embeddings and calculates a match score
3. It extracts key skills from the job description and lists the ones missing from your resume
4. It gives suggestions on what to learn or add

## Tech stack (planned)

- Python
- NLP: sentence embeddings for text similarity
- Streamlit for the web interface
- Docker for deployment

## Roadmap

- [x] Week 1: Compare two texts and output a similarity score
- [ ] Week 2: Skill extraction and missing-skills list
- [ ] Week 3: Streamlit web app and live deployment
- [ ] Week 4: Docker, tests, and write-up

## Status

Just getting started. Building in public, one small commit at a time.
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("samples/resume.txt", encoding="utf-8") as f:
    resume = f.read()

with open("samples/job.txt", encoding="utf-8") as f:
    job = f.read()

embeddings = model.encode([resume, job])
score = util.cos_sim(embeddings[0], embeddings[1]).item()

print(f"Match score: {score:.2f}")
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

resume = "I know Python and machine learning"
good_job = "Looking for a Python and ML intern"
bad_job = "Chef needed for a busy restaurant"

embeddings = model.encode([resume, good_job, bad_job])

print("resume vs good job:", util.cos_sim(embeddings[0], embeddings[1]).item())
print("resume vs bad job: ", util.cos_sim(embeddings[0], embeddings[2]).item())
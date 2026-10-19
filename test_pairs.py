from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

pairs = [
    ("machine learning", "ML"),
    ("machine learning", "I trained ML models for a class project"),
    ("large language models", "LLMs"),
    ("PyTorch", "TensorFlow"),
    ("Python", "Java"),
    ("machine learning", "video editing and Canva"),
    ("machine learning", "cooking and hiking"),
]

for a, b in pairs:
    score = util.cos_sim(model.encode(a), model.encode(b)).item()
    print(f"{score:.2f} | {a}  <->  {b}")
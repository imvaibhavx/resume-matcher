from sentence_transformers import SentenceTransformer, util
from aliases import expand_aliases
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
    score = util.cos_sim(model.encode(expand_aliases(a)), model.encode(expand_aliases(b))).item()
    print(f"{score:.2f} | {a}  <->  {b}")
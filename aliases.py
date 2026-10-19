import re

ALIASES = {
    "ml": "machine learning",
    "dl": "deep learning",
    "llm": "large language model",
    "llms": "large language models",
    "nlp": "natural language processing",
    "ai": "artificial intelligence",
    "rl": "reinforcement learning",
    "sklearn": "scikit-learn",
    "k8s": "kubernetes",
}


def expand_aliases(text):
    for short, full in ALIASES.items():
        pattern = r"(?<!\w)" + re.escape(short) + r"(?!\w)"
        text = re.sub(pattern, full, text, flags=re.IGNORECASE)
    return text
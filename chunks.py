import re
from pathlib import Path

def clean_text(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    text = re.sub(r"(?<!\w)\*(\S[^*\n]*?)\*(?!\w)", r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"^\s*(?:[-*•·]|\d+[.)])\s+", "", text, flags=re.MULTILINE)
    return text

def split_into_chunks(text, min_words=4):
    text = clean_text(text)
    parts = re.split(r"[\n\r]+|(?<=[.!?])\s+", text)
    chunks = [p.strip(" -•*\t") for p in parts]
    return [c for c in chunks if len(c.split()) >= min_words]


if __name__ == "__main__":
    for path in ["private/resume.txt", "private/jobs/job1.txt"]:
        text = Path(path).read_text(encoding="utf-8")
        chunks = split_into_chunks(text)
        print(f"\n{path}: {len(chunks)} chunks")
        for chunk in chunks[:8]:
            print(" -", chunk)
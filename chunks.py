import re
from pathlib import Path


def split_into_chunks(text, min_words=4):
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
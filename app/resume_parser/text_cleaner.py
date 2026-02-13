import re
from typing import List, Tuple

def normalize_whitespace(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n\n", text)       # collapse many blank lines
    text = re.sub(r"[ \t]+", " ", text)         # collapse spaces
    return text.strip()

def split_to_lines(text: str) -> List[str]:
    lines = text.split("\n")
    # Clean each line
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line:
            clean_lines.append(line)
    return clean_lines

def clean_text(text: str) -> Tuple[str, List[str]]:
    """
    Returns:
      - cleaned full text as single string
      - list of cleaned non-empty lines
    """
    normalized = normalize_whitespace(text)
    lines = split_to_lines(normalized)
    return "\n".join(lines), lines
import re
from typing import Dict, List
from .skills_data import TECHNICAL_SKILLS

def normalize(text: str) -> str:
    return text.lower()

def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Simple keyword-based matcher.
    Returns dict: category -> list of matched skills
    """
    text_norm = normalize(text)
    found = {}

    for category, skills in TECHNICAL_SKILLS.items():
        matches = set()
        for skill in skills:
            # Word boundary match for single words,
            # substring for multi-word terms like 'machine learning'
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text_norm):
                matches.add(skill)
        if matches:
            found[category] = sorted(matches)

    # Flatten all skills for a 'all_skills' field if needed
    all_skills = sorted({s for sub in found.values() for s in sub})
    found["all_skills"] = all_skills

    return found
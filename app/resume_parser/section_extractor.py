from typing import List, Dict
import re

SECTION_HEADERS = [
    "SUMMARY",
    "PROFILE",
    "OBJECTIVE",
    "EXPERIENCE",
    "WORK EXPERIENCE",
    "PROFESSIONAL EXPERIENCE",
    "EMPLOYMENT",
    "EDUCATION",
    "SKILLS",
    "TECHNICAL SKILLS",
    "PROJECTS",
    "CERTIFICATIONS",
    "AWARDS",
    "PUBLICATIONS",
    "INTERNSHIPS",
]

def is_section_header(line: str) -> bool:
    stripped = line.strip()
    upper = stripped.upper()
    if upper in SECTION_HEADERS:
        return True
    # Detect patterns like "SKILLS & INTERESTS", "EDUCATION AND TRAINING"
    if re.match(r"^[A-Z][A-Z &/]+$", stripped) and len(stripped.split()) <= 5:
        return True
    return False

def normalize_header(line: str) -> str:
    upper = line.strip().upper()
    for header in SECTION_HEADERS:
        if upper == header:
            return header
    # fallback: return uppercased line
    return upper

def extract_sections(lines: List[str]) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {}
    current_header = "GENERAL"

    for line in lines:
        if is_section_header(line):
            current_header = normalize_header(line)
            if current_header not in sections:
                sections[current_header] = []
        else:
            if current_header not in sections:
                sections[current_header] = []
            sections[current_header].append(line)

    # Join lines back into text per section
    joined_sections = {header: "\n".join(content).strip()
                       for header, content in sections.items()
                       if content and content[0].strip()}

    return joined_sections
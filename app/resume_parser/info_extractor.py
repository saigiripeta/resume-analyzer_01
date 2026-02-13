import re
from typing import Dict, List

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_REGEX = re.compile(
    r"(\+?\d{1,3}[\s-]?)?(\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}"
)
LINKEDIN_REGEX = re.compile(r"(https?://)?(www\.)?linkedin\.com/[A-Za-z0-9_/.-]+", re.I)
GITHUB_REGEX = re.compile(r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_/.-]+", re.I)

def extract_email(text: str) -> str:
    match = EMAIL_REGEX.search(text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    matches = PHONE_REGEX.findall(text)
    if not matches:
        return ""
    # Take first match and flatten tuple
    raw = "".join(matches[0])
    cleaned = re.sub(r"[^\d+]", "", raw)
    return cleaned

def extract_urls(regex, text: str) -> List[str]:
    return list(set(m.group(0) for m in regex.finditer(text)))

def guess_name(lines: List[str], email: str) -> str:
    """
    Heuristic: first 1–3 lines, excluding lines that are just contact info.
    """
    # Extract local part of email for comparison
    email_local = email.split("@")[0] if email else ""
    candidates = []

    for line in lines[:5]:
        # Skip if looks like contact info or headline with job title
        if EMAIL_REGEX.search(line):
            continue
        if any(keyword in line.lower() for keyword in ["phone", "mobile", "linkedin", "github", "email"]):
            continue
        if len(line.split()) > 6:
            continue
        candidates.append(line)

    if not candidates:
        return ""

    # Simple heuristic: choose the line that shares tokens with email local part
    def score(candidate: str) -> int:
        name_parts = re.split(r"\W+", candidate.lower())
        email_parts = re.split(r"\W+|_", email_local.lower())
        return len(set(name_parts) & set(email_parts))

    best = max(candidates, key=score)
    return best.strip()

def extract_basic_info(lines: List[str]) -> Dict[str, str]:
    full_text = "\n".join(lines)

    email = extract_email(full_text)
    phone = extract_phone(full_text)
    linkedin_urls = extract_urls(LINKEDIN_REGEX, full_text)
    github_urls = extract_urls(GITHUB_REGEX, full_text)
    name = guess_name(lines, email)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin_urls[0] if linkedin_urls else "",
        "github": github_urls[0] if github_urls else "",
    }
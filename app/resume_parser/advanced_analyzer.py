from typing import List, Dict, Any, Optional, Tuple
import re
from datetime import date

# ---------- Degree detection patterns ----------

DEGREE_PATTERNS: Dict[str, str] = {
    # PhD / Doctorate
    r"\bphd\b": "PhD",
    r"\bph\.?\s*d\.?\b": "PhD",
    r"\bdoctor of philosophy\b": "PhD",
    r"\bdoctoral (degree|studies|candidate)\b": "PhD",
    r"\bdphil\b": "PhD",

    # Master's level
    r"\bmaster[’']?s?\s+degree\b": "Master",
    r"\bm\.?\s*tech\b": "Master",
    r"\bmaster of technology\b": "Master",
    r"\bm\.?\s*e\b": "Master",
    r"\bmaster of engineering\b": "Master",
    r"\bm\.?\s*sc\b": "Master",
    r"\bmaster of science\b": "Master",
    r"\bm\.?\s*a\b": "Master",
    r"\bmaster of arts\b": "Master",
    r"\bm\.?\s*com\b": "Master",
    r"\bmaster of commerce\b": "Master",
    r"\bmca\b": "Master",
    r"\bmaster of computer applications\b": "Master",
    r"\bmba\b": "Master",
    r"\bmaster of business administration\b": "Master",
    r"\bmpm\b": "Master",
    r"\bmpa\b": "Master",
    r"\bpgdm\b": "Master",
    r"\bpost[-\s]graduate diploma\b": "Master",
    r"\bpost[-\s]graduation\b": "Master",

    # Bachelor's level
    r"\bb\.?\s*tech\b": "Bachelor",
    r"\bbtech\b": "Bachelor",
    r"\bb\.?\s*e\b": "Bachelor",
    r"\bbachelor of engineering\b": "Bachelor",
    r"\bb\.?\s*sc\b": "Bachelor",
    r"\bbachelor of science\b": "Bachelor",
    r"\bbsc\b": "Bachelor",
    r"\bb\.?\s*a\b": "Bachelor",
    r"\bbachelor of arts\b": "Bachelor",
    r"\bb\.?\s*com\b": "Bachelor",
    r"\bbachelor of commerce\b": "Bachelor",
    r"\bbcom\b": "Bachelor",
    r"\bbca\b": "Bachelor",
    r"\bbachelor of computer applications\b": "Bachelor",
    r"\bbba\b": "Bachelor",
    r"\bbachelor of business administration\b": "Bachelor",
    r"\bbs\b": "Bachelor",
    r"\bb\.?\s*s\b": "Bachelor",

    # Diploma / School
    r"\bdiploma\b": "Diploma",
    r"\bpolytechnic\b": "Diploma",
    r"\bassociate degree\b": "Diploma",
    r"\bintermediate\b": "HighSchool",
    r"\bsenior secondary\b": "HighSchool",
    r"\bhigher secondary\b": "HighSchool",
    r"\bhigh school\b": "HighSchool",
    r"\b10th\s*(class|standard|grade)\b": "HighSchool",
    r"\b12th\s*(class|standard|grade)\b": "HighSchool",
    r"\bssc\b": "HighSchool",
    r"\bhsc\b": "HighSchool",
}

DEGREE_PRIORITY: Dict[str, int] = {
    "HighSchool": 1,
    "Diploma": 2,
    "Bachelor": 3,
    "Master": 4,
    "PhD": 5,
}

DEGREE_REGEXES = [(re.compile(pat, re.IGNORECASE), degree) for pat, degree in DEGREE_PATTERNS.items()]

# ---------- Department keywords ----------

DEPARTMENT_KEYWORDS: Dict[str, str] = {
    # Commerce / Management
    "department of commerce": "Commerce",
    "m.com": "Commerce",
    "b.com": "Commerce",
    "commerce": "Commerce",
    "accounting and finance": "Commerce",
    "accounting": "Commerce",
    "auditing": "Commerce",
    "financial management": "Commerce",
    "business studies": "Commerce",
    "business administration": "Management",
    "school of management": "Management",
    "department of management": "Management",

    # English / Humanities
    "english language and literature": "English",
    "department of english language and literature": "English",
    "english literature": "English",
    "department of english": "English",
    "m.a (english)": "English",
    "ma (english)": "English",
    "b.a (english)": "English",
    "b.a (english literature)": "English",
    "ba (english)": "English",

    # Computer Science / IT
    "computer science and engineering": "Computer Science",
    "computer science & engineering": "Computer Science",
    "computer science": "Computer Science",
    "information technology": "Computer Science",
    "information systems": "Computer Science",
    "cse": "Computer Science",
    "it engineering": "Computer Science",
    "data science": "Computer Science",
    "data structures": "Computer Science",
    "algorithms": "Computer Science",
    "machine learning": "Computer Science",
    "artificial intelligence": "Computer Science",
    "operating systems": "Computer Science",
    "database systems": "Computer Science",
    "databases": "Computer Science",
    "software engineering": "Computer Science",

    # Electronics / Electrical
    "electronics and communication": "Electronics",
    "electronics & communication": "Electronics",
    "ece": "Electronics",
    "electronics engineering": "Electronics",
    "vlsi": "Electronics",
    "signal processing": "Electronics",
    "embedded systems": "Electronics",
    "electrical engineering": "Electrical",
    "eee": "Electrical",

    # Mechanical
    "mechanical engineering": "Mechanical",
    "thermal engineering": "Mechanical",
    "thermodynamics": "Mechanical",
    "fluid mechanics": "Mechanical",

    # Civil
    "civil engineering": "Civil",
    "structural engineering": "Civil",

    # Sciences
    "applied physics": "Physics",
    "physics": "Physics",
    "applied mathematics": "Mathematics",
    "mathematics": "Mathematics",
    "statistics": "Mathematics",
    "chemistry": "Chemistry",
    "biotechnology": "Biotechnology",
}

EDU_SECTION_TITLES: List[str] = [
    "education",
    "educational qualification",
    "educational qualifications",
    "academic background",
    "academic qualifications",
    "qualifications",
    "education & training",
]

SECTION_BOUNDARY_TITLES: List[str] = [
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "work history",
    "projects",
    "skills",
    "technical skills",
    "publications",
    "research",
    "certifications",
    "achievements",
    "summary",
    "objective",
    "profile",
    "declaration",
]

YEAR_RANGE_RE = re.compile(
    r"(?P<start>(?:19|20)\d{2})\s*(?:[-–/]|to)\s*"
    r"(?P<end>(?:19|20)\d{2}|present|current|ongoing|till date|now)",
    re.IGNORECASE,
)
SINGLE_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
DATE_WITH_YEAR_RE = re.compile(r"\d{1,2}[./-]\d{1,2}[./-](\d{2,4})")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_BLOCK_RE = re.compile(r"\+?\d[\d\-\s/]{8,}\d")

COUNTRY_HINT_RE = re.compile(
    r"\b(india|usa|united states|canada|uk|united kingdom|australia|germany|france|italy|spain|"
    r"singapore|uae|dubai|qatar|saudi arabia|china|japan)\b",
    re.IGNORECASE,
)

NUMERIC_RANGE_RE = re.compile(
    r"(?P<from_d>\d{1,2})[./-]\s*(?P<from_m>\d{1,2})[./-]\s*(?:[A-Za-z]{0,2})?(?P<from_y>\d{2,4})\s*"
    r"(?:to|[-–])\s*"
    r"(?:(?P<to_d>\d{1,2})[./-]\s*(?P<to_m>\d{1,2})[./-]\s*(?:[A-Za-z]{0,2})?(?P<to_y>\d{2,4})|"
    r"(?P<to_label>Present|Currently Working|Current|Till Date|Till today|Today|Now|till today))",
    re.IGNORECASE,
)

MONTH_ABBR = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}

INDIAN_STATES = [
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka",
    "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya",
    "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim",
    "tamil nadu", "telangana", "tripura", "uttar pradesh", "uttarakhand",
    "west bengal",
    "andaman and nicobar islands", "chandigarh", "dadra and nagar haveli",
    "daman and diu", "delhi", "lakshadweep", "puducherry", "ladakh", "jammu and kashmir"
]


def normalize_year(year_str: str) -> int:
    y = int(year_str)
    if len(year_str) == 4:
        return y
    cur_yy = date.today().year % 100
    if y <= cur_yy:
        return 2000 + y
    return 1900 + y

# ---------- Education helpers ----------

def extract_education_section(text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return text

    start_idx: Optional[int] = None
    for i, line in enumerate(lines):
        ll = line.strip().lower()
        if any(title in ll for title in EDU_SECTION_TITLES):
            start_idx = i
            break

    if start_idx is None:
        return text

    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        ll = lines[j].strip().lower()
        if not ll:
            continue
        if any(title in ll for title in SECTION_BOUNDARY_TITLES):
            end_idx = j
            break

    section = "\n".join(lines[start_idx:end_idx]).strip()
    return section or text


def detect_degrees_simple(text: str) -> List[str]:
    found: List[str] = []
    for regex, degree_name in DEGREE_REGEXES:
        if regex.search(text):
            if degree_name not in found:
                found.append(degree_name)
    return found


def determine_highest_degree(degrees: List[str]) -> str:
    if not degrees:
        return "Unknown"
    best_degree = "Unknown"
    best_priority = 0
    for d in degrees:
        priority = DEGREE_PRIORITY.get(d, 0)
        if priority > best_priority:
            best_priority = priority
            best_degree = d
    return best_degree


def get_phd_status(text: str) -> Optional[str]:
    low = text.lower()
    statuses: List[str] = []

    for m in re.finditer(r"ph\.?\s*d\.?|phd", low):
        window = low[max(0, m.start() - 100): m.end() + 100]
        if "awarded" in window:
            return "Awarded"
        if "thesis submitted" in window or "submitted thesis" in window:
            statuses.append("Thesis Submitted")
        if any(w in window for w in ["pursuing", "ongoing", "currently", "in progress"]):
            statuses.append("Pursuing")

    return statuses[0] if statuses else None


def extract_years_from_text(text: str) -> Tuple[Optional[int], Optional[int]]:
    m = YEAR_RANGE_RE.search(text)
    if m:
        start_year = int(m.group("start"))
        end_raw = m.group("end")
        if end_raw.isdigit():
            end_year = int(end_raw)
        else:
            end_year = None
        return start_year, end_year

    years = SINGLE_YEAR_RE.findall(text)
    if years:
        return None, int(years[-1])

    dt_matches = DATE_WITH_YEAR_RE.findall(text)
    if dt_matches:
        yr = normalize_year(dt_matches[-1])
        return None, yr

    return None, None


def extract_field_and_institution(block_text: str) -> Tuple[Optional[str], Optional[str]]:
    field: Optional[str] = None
    institution: Optional[str] = None

    paren = re.search(r"\(([^)]+)\)", block_text)
    if paren:
        raw = paren.group(1).strip()
        if len(raw) > 2 and not re.search(r"\d{2,4}", raw):
            field = raw

    if field is None:
        low = block_text.lower()
        if " in " in low:
            idx = low.find(" in ")
            after_orig = block_text[idx + 4:]
            for sep in [",", "|", "-", "–", " at ", " from "]:
                if sep in after_orig:
                    after_orig = after_orig.split(sep)[0]
                    break
            f = after_orig.strip(" ,.-–")
            if len(f) > 2 and not re.search(r"\d{2,4}", f):
                field = f

    inst_match = re.search(
        r"([A-Z][A-Za-z0-9&., ]+\b(?:University|College|Institute|School|Academy|Polytechnic|High School))",
        block_text,
    )
    if not inst_match:
        inst_match = re.search(
            r"\b(?:at|from)\s+([A-Z][A-Za-z0-9&., ]{3,})",
            block_text,
        )

    if inst_match:
        institution = inst_match.group(1).strip(" ,.-")

    return field, institution


ORG_ENTITY_RE = re.compile(
    r"([A-Z][A-Za-z0-9&(). ]+\b(?:University|College|Institute|School|Academy|Bank|Limited|Ltd|Company|"
    r"Corporation|Supermarts|Retail|Group|Technologies|Solutions|Systems|Hospital|Centre|Center|"
    r"Laboratories|Labs))"
)


def parse_role_org_location(header: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    hdr = re.sub(r"\s+", " ", header).strip(" ,.-–")
    if not hdr:
        return None, None, None

    role: Optional[str] = None
    org: Optional[str] = None
    location: Optional[str] = None

    org_matches = list(ORG_ENTITY_RE.finditer(hdr))
    if org_matches:
        m = org_matches[-1]
        org = m.group(1).strip(" ,.-–")
        before = hdr[:m.start()].strip(" ,.-–")
        after = hdr[m.end():].strip(" ,.-–")
        role = before or None
        location = after or None
    else:
        parts = [p.strip() for p in re.split(r"[-–]", hdr, maxsplit=1)]
        if len(parts) == 2:
            role = parts[0] or None
            rest = parts[1]
        else:
            rest = hdr

        segments = [s.strip() for s in rest.split(",") if s.strip()]
        if segments:
            if len(segments) >= 2:
                org = ", ".join(segments[:-1])
                location = segments[-1]
            else:
                org = segments[0]

    if org:
        low_org = org.lower()
        ua = "university administration"
        idx = low_org.find(ua)
        if idx != -1:
            prefix = org[: idx + len(ua)].strip(" ,.-–")
            remainder = org[idx + len(ua):].strip(" ,.-–")
            if remainder:
                org = remainder
            else:
                org = None
            if prefix:
                role = (f"{role} {prefix}".strip() if role else prefix)

    if location and location.lower().startswith("of ") and "," in location:
        first_part, rest = location.split(",", 1)
        org = (org + " " + first_part).strip() if org else first_part.strip()
        location = rest.strip() if rest.strip() else None

    if location:
        location = location.lstrip(" ,.-–")

    return role, org, location


def extract_degrees_detail(education_text: str, full_text: str) -> List[Dict[str, Any]]:
    lines = [ln.strip() for ln in education_text.splitlines() if ln.strip()]
    if not lines:
        return []

    blocks: List[List[str]] = []
    current: List[str] = []

    inst_keywords = ["university", "college", "institute", "school", "academy", "polytechnic"]

    for line in lines:
        ll = line.lower()

        has_degree_kw = any(regex.search(ll) for regex, _ in DEGREE_REGEXES)
        has_year = bool(SINGLE_YEAR_RE.search(ll))
        has_inst = any(k in ll for k in inst_keywords)
        starts_new_block = has_degree_kw or (has_year and has_inst)

        if starts_new_block:
            if current:
                blocks.append(current)
            current = [line]
        else:
            if current:
                current.append(line)

    if current:
        blocks.append(current)

    phd_status_global = get_phd_status(full_text)
    detailed: List[Dict[str, Any]] = []

    for block in blocks:
        full = " ".join(block)
        full_low = full.lower()

        degrees_here = detect_degrees_simple(full)
        if not degrees_here:
            degrees_here = detect_degrees_simple(block[0])
        if not degrees_here:
            continue

        degree_type = determine_highest_degree(degrees_here)
        start_year, end_year = extract_years_from_text(full)
        field, institution = extract_field_and_institution(full)

        status = "Completed"
        if any(w in full_low for w in ["pursuing", "ongoing", "currently", "in progress", "present"]):
            status = "Pursuing"
        if end_year is None and start_year is not None:
            status = "Pursuing"

        phd_thesis_submitted = False
        phd_awarded = False

        if degree_type == "PhD":
            if phd_status_global == "Awarded":
                status = "Awarded"
                phd_awarded = True
            elif phd_status_global == "Thesis Submitted":
                status = "Thesis Submitted"
                phd_thesis_submitted = True
            elif phd_status_global == "Pursuing":
                status = "Pursuing"

            if "thesis submitted" in full_low:
                status = "Thesis Submitted"
                phd_thesis_submitted = True
            if "awarded" in full_low:
                status = "Awarded"
                phd_awarded = True

        detailed.append(
            {
                "degree_type": degree_type,
                "raw_text": full,
                "field_of_study": field,
                "institution": institution,
                "start_year": start_year,
                "end_year": end_year,
                "status": status,
                "phd_thesis_submitted": phd_thesis_submitted if degree_type == "PhD" else None,
                "phd_awarded": phd_awarded if degree_type == "PhD" else None,
            }
        )

    return detailed


def infer_department_from_fields(fields_of_study: List[str]) -> str:
    for field in fields_of_study:
        f_low = field.lower()
        for keyword, department in DEPARTMENT_KEYWORDS.items():
            if keyword in f_low:
                return department
    return "Unknown"


def infer_department_from_text(text: str) -> str:
    text_low = text.lower()
    for keyword, department in DEPARTMENT_KEYWORDS.items():
        if keyword in text_low:
            return department
    return "Unknown"


def score_resume(
    has_phd_flag: bool,
    highest_degree: str,
    department: str,
    target_department: Optional[str] = None,
) -> int:
    score = 0
    if has_phd_flag:
        score += 50
    elif highest_degree == "Master":
        score += 35
    elif highest_degree == "Bachelor":
        score += 25
    elif highest_degree in ("Diploma", "HighSchool"):
        score += 15
    else:
        score += 10

    if target_department:
        if department.lower() == target_department.lower():
            score += 30
        else:
            score += 10
    return score

# ---------- Personal info & global lists ----------

def extract_email(text: str) -> Optional[str]:
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None


def extract_all_emails(text: str) -> List[str]:
    emails = EMAIL_RE.findall(text)
    seen = set()
    result_list = []
    for e in emails:
        if e.lower() not in seen:
            seen.add(e.lower())
            result_list.append(e)
    return result_list


def extract_phone(text: str) -> Optional[str]:
    lines = text.splitlines()
    top = "\n".join(lines[:25])

    def from_scope(scope: str) -> Optional[str]:
        for cand in PHONE_BLOCK_RE.findall(scope):
            for part in re.split(r"[\/,|]", cand):
                part = part.strip()
                if not part:
                    continue
                digits = re.sub(r"\D", "", part)
                if 10 <= len(digits) <= 13:
                    return part
        return None

    phone = from_scope(top)
    if phone:
        return phone
    return from_scope(text)


def extract_all_phones(text: str) -> List[str]:
    seen_digits = set()
    results: List[str] = []

    for cand in PHONE_BLOCK_RE.findall(text):
        for part in re.split(r"[\/,|]", cand):
            part = part.strip()
            if not part:
                continue
            digits = re.sub(r"\D", "", part)
            if 10 <= len(digits) <= 13 and digits not in seen_digits:
                seen_digits.add(digits)
                results.append(part)
    return results


def extract_name(text: str) -> Optional[str]:
    lines = text.splitlines()

    prefixes = ["mr ", "ms ", "mrs ", "dr ", "dr. ", "prof. ", "prof "]
    bad_words = ["resume", "curriculum vitae", "curriculum vitæ", "bio-data", "biodata", "profile", "cv"]

    for line in lines[:30]:
        name = line.strip()
        if not name:
            continue

        low = name.lower()
        if any(bw in low for bw in bad_words):
            continue
        if "@" in name or re.search(r"\d", name):
            continue

        for p in prefixes:
            if low.startswith(p):
                name = name[len(p):].strip()
                break

        if 1 <= len(name.split()) <= 4:
            return name

    return None


def extract_location(text: str) -> Optional[str]:
    lines = text.splitlines()

    for line in lines[:25]:
        raw = line.strip()
        if not raw:
            continue
        low = raw.lower()

        if "location" in low or "address" in low:
            part = raw.split(":", 1)[-1].strip()
            part = part.split("|")[-1].strip()
            if part:
                return part

        if COUNTRY_HINT_RE.search(low):
            if "|" in raw:
                cand = raw.split("|")[-1].strip()
            else:
                cand = raw
            return cand

        if "," in raw and "@" not in raw and not re.search(r"\d", raw):
            return raw

    return None


def extract_indian_states(text: str) -> List[str]:
    low = text.lower()
    found = []
    for st in INDIAN_STATES:
        if st in low:
            found.append(st.title())
    seen = set()
    result_list = []
    for s in found:
        if s not in seen:
            seen.add(s)
            result_list.append(s)
    return result_list


def extract_current_organization(text: str) -> Optional[str]:
    lines = text.splitlines()

    work_start = None
    for i, line in enumerate(lines):
        ll = line.lower()
        if any(k in ll for k in ["work experience", "professional experience", "experience", "employment history"]):
            work_start = i
            break
    start_idx = work_start if work_start is not None else 0

    org_keywords = [
        "university", "college", "institute", "school", "company", "pvt", "ltd", "limited",
        "inc", "solutions", "technologies", "labs", "systems", "corp", "corporation", "llc"
    ]

    month_pattern = (
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)"
    )
    present_pattern = re.compile(
        rf"^(?P<role_org>.+?)\s+{month_pattern}\s+\d{{4}}\s*[-–]\s*"
        r"(?:Present|Current|Currently Working|Till Date|Now)\b",
        re.IGNORECASE,
    )

    for line in lines[start_idx:]:
        m = present_pattern.search(line.strip())
        if not m:
            continue
        role_org = m.group("role_org").strip(" -•")
        parts = [p.strip() for p in role_org.split(",") if p.strip()]
        if len(parts) > 1:
            return parts[-1]
        low = role_org.lower()
        if any(k in low for k in org_keywords):
            return role_org

    for i in range(start_idx, len(lines)):
        ll = lines[i].lower()
        if "currently working" in ll or "present" in ll or "till today" in ll:
            for j in range(max(start_idx, i - 3), i + 2):
                if j < 0 or j >= len(lines):
                    continue
                cand = lines[j].strip()
                if cand and any(k in cand.lower() for k in org_keywords):
                    return cand

    for i in range(start_idx, min(start_idx + 25, len(lines))):
        ll = lines[i].lower()
        if any(k in ll for k in org_keywords):
            cand = lines[i].strip()
            if cand:
                return cand

    return None

# ---------- Experience breakdown (years only) ----------

def calculate_experience_breakdown(text: str) -> Dict[str, Optional[float]]:
    month_pattern = (
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)"
    )
    month_range_pattern = (
        rf"(?:(?:From|from|Since|since)\s+)?"
        rf"(?P<from_day>\d{{1,2}}(?:st|nd|rd|th)?\s+)?"
        rf"(?P<from_month>{month_pattern})\s+(?P<from_year>\d{{4}})\s*"
        rf"(?:[-–]|to)\s*"
        rf"(?:(?P<to_day>\d{{1,2}}(?:st|nd|rd|th)?\s+)?"
        rf"(?P<to_month>{month_pattern})\s+(?P<to_year>\d{{4}})|"
        r"(?P<to_label>Present|Currently Working|Current|Till Date|Till date|Now|till date))"
    )
    month_range_re = re.compile(month_range_pattern, re.IGNORECASE)

    month_map = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }

    teaching_keywords = [
        "professor", "assistant professor", "associate professor",
        "lecturer", "teacher", "faculty", "school", "college", "university",
        "institute", "academy"
    ]
    industry_keywords = [
        "developer", "software", "engineer", "company", "pvt", "ltd", "limited",
        "solutions", "consultant", "analyst", "manager", "industry",
        "it services", "technologies", "firm", "corporation", "llc", "startup",
        "audit", "auditor", "accounts", "accountant", "bank", "retail",
        "supermarts"
    ]

    teaching_months = 0
    industry_months = 0
    other_months = 0

    today = date.today()

    for m in month_range_re.finditer(text):
        fm_str = m.group("from_month")[:3].lower()
        from_month = month_map.get(fm_str)
        from_year = int(m.group("from_year"))
        if from_month is None:
            continue

        if m.group("to_month"):
            tm_str = m.group("to_month")[:3].lower()
            to_month = month_map.get(tm_str)
            to_year = int(m.group("to_year"))
        else:
            to_month = today.month
            to_year = today.year

        months = (to_year - from_year) * 12 + (to_month - from_month)
        if months <= 0:
            continue

        ctx = text[max(0, m.start() - 120): m.end() + 120].lower()
        if any(kw in ctx for kw in teaching_keywords):
            teaching_months += months
        elif any(kw in ctx for kw in industry_keywords):
            industry_months += months
        else:
            other_months += months

    for m in NUMERIC_RANGE_RE.finditer(text):
        from_month = int(m.group("from_m"))
        from_year = normalize_year(m.group("from_y"))
        if not (1 <= from_month <= 12):
            continue

        if m.group("to_label"):
            to_year = today.year
            to_month = today.month
        else:
            to_month = int(m.group("to_m"))
            to_year = normalize_year(m.group("to_y"))
            if not (1 <= to_month <= 12):
                continue

        months = (to_year - from_year) * 12 + (to_month - from_month)
        if months <= 0:
            continue

        ctx = text[max(0, m.start() - 120): m.end() + 120].lower()
        if any(kw in ctx for kw in teaching_keywords):
            teaching_months += months
        elif any(kw in ctx for kw in industry_keywords):
            industry_months += months
        else:
            other_months += months

    for m in YEAR_RANGE_RE.finditer(text):
        from_year = int(m.group("start"))
        end_raw = m.group("end")
        if end_raw.isdigit():
            to_year = int(end_raw)
            to_month = 12
        else:
            to_year = today.year
            to_month = today.month
        months = (to_year - from_year) * 12 + (to_month - 1)
        if months <= 0:
            continue

        ctx = text[max(0, m.start() - 120): m.end() + 120].lower()
        if any(kw in ctx for kw in teaching_keywords):
            teaching_months += months
        elif any(kw in ctx for kw in industry_keywords):
            industry_months += months
        else:
            other_months += months

    def months_to_years(m: int) -> Optional[float]:
        if m <= 0:
            return None
        return round(m / 12.0, 1)

    total_months = teaching_months + industry_months + other_months

    return {
        "teaching_years": months_to_years(teaching_months),
        "industry_years": months_to_years(industry_months),
        "other_years": months_to_years(other_months),
        "total_years": months_to_years(total_months),
    }

# ---------- Experience history (detailed list) ----------

def extract_experience_history(text: str) -> List[Dict[str, Any]]:
    lines = text.splitlines()
    if not lines:
        return []

    month_pattern = (
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)"
    )
    month_range_pattern = (
        rf"(?:(?:From|from|Since|since)\s+)?"
        rf"(?P<from_day>\d{{1,2}}(?:st|nd|rd|th)?\s+)?"
        rf"(?P<from_month>{month_pattern})\s+(?P<from_year>\d{{4}})\s*"
        rf"(?:[-–]|to)\s*"
        rf"(?:(?P<to_day>\d{{1,2}}(?:st|nd|rd|th)?\s+)?"
        rf"(?P<to_month>{month_pattern})\s+(?P<to_year>\d{{4}})|"
        r"(?P<to_label>Present|Currently Working|Current|Till Date|Till date|Now|till date))"
    )
    month_range_re = re.compile(month_range_pattern, re.IGNORECASE)

    month_map = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }

    today = date.today()

    JOB_TITLE_KEYWORDS = [
        "assistant professor", "associate professor", "professor",
        "lecturer", "teacher", "head of the department", "hod",
        "consultant", "manager", "executive", "engineer", "developer",
        "associate", "officer", "analyst", "instructor", "faculty",
        "accounts", "accountant", "audit", "auditor"
    ]

    TEACHING_KEYWORDS = [
        "professor", "assistant professor", "associate professor",
        "lecturer", "teacher", "faculty", "school", "college", "university",
        "institute", "academy"
    ]
    INDUSTRY_KEYWORDS = [
        "developer", "software", "engineer", "company", "pvt", "ltd", "limited",
        "solutions", "consultant", "analyst", "manager", "industry",
        "it services", "technologies", "firm", "corporation", "llc", "startup",
        "audit", "auditor", "accounts", "accountant", "bank", "retail",
        "supermarts"
    ]

    STOP_HEADINGS = EDU_SECTION_TITLES + SECTION_BOUNDARY_TITLES + [
        "research experience", "journal papers", "publications",
        "faculty development programs", "fdp", "fdps", "conferences",
    ]

    BULLET_PREFIXES = ("•", "◦", "●", "○", "■", "▪", "►", "", "-", "*")

    def parse_line_date(line: str):
        m = month_range_re.search(line)
        if m:
            fm_str = m.group("from_month")[:3].lower()
            from_month = month_map.get(fm_str)
            from_year = int(m.group("from_year"))
            if from_month is None:
                return None
            if m.group("to_month"):
                tm_str = m.group("to_month")[:3].lower()
                to_month = month_map.get(tm_str)
                to_year = int(m.group("to_year"))
                ongoing = False
            else:
                to_month = None
                to_year = None
                ongoing = True
            return {
                "from_year": from_year,
                "from_month": from_month,
                "to_year": to_year,
                "to_month": to_month,
                "ongoing": ongoing,
                "date_text": m.group(0),
            }

        m = NUMERIC_RANGE_RE.search(line)
        if m:
            from_month = int(m.group("from_m"))
            from_year = normalize_year(m.group("from_y"))
            if not (1 <= from_month <= 12):
                return None
            if m.group("to_label"):
                to_year = None
                to_month = None
                ongoing = True
            else:
                to_month = int(m.group("to_m"))
                to_year = normalize_year(m.group("to_y"))
                if not (1 <= to_month <= 12):
                    return None
                ongoing = False
            return {
                "from_year": from_year,
                "from_month": from_month,
                "to_year": to_year,
                "to_month": to_month,
                "ongoing": ongoing,
                "date_text": m.group(0),
            }

        m = YEAR_RANGE_RE.search(line)
        if m:
            from_year = int(m.group("start"))
            end_raw = m.group("end")
            if end_raw.isdigit():
                to_year = int(end_raw)
                to_month = 12
                ongoing = False
            else:
                to_year = None
                to_month = None
                ongoing = True
            return {
                "from_year": from_year,
                "from_month": 1,
                "to_year": to_year,
                "to_month": to_month,
                "ongoing": ongoing,
                "date_text": m.group(0),
            }

        return None

    experiences: List[Dict[str, Any]] = []

    for idx, line in enumerate(lines):
        date_info = parse_line_date(line)
        if not date_info:
            continue

        date_text = date_info["date_text"]
        date_line = line.strip()

        base_header_wo_date = date_line.replace(date_text, " ").strip(" ,.-–")
        header_parts = [base_header_wo_date]

        for offset in (1, 2):
            prev_idx = idx - offset
            if prev_idx < 0:
                break
            prev = lines[prev_idx].strip()
            if not prev:
                continue
            if parse_line_date(prev):
                continue
            if prev.lstrip().startswith(BULLET_PREFIXES):
                continue
            if re.match(r"^\d+[\).\s]", prev):
                continue
            low_prev = prev.lower()
            if any(h in low_prev for h in STOP_HEADINGS):
                continue
            has_job_kw = any(kw in low_prev for kw in JOB_TITLE_KEYWORDS)
            has_org_kw = any(
                k in low_prev
                for k in [
                    "university", "college", "institute", "school",
                    "academy", "company", "limited", "ltd",
                    "supermarts", "retail", "bank"
                ]
            )
            if has_job_kw or has_org_kw:
                header_parts.insert(0, prev)
                break

        header_wo_date = " ".join(header_parts).strip()

        header_lower = header_wo_date.lower()
        cut_positions = []
        for kw in JOB_TITLE_KEYWORDS:
            pos = header_lower.find(kw)
            if pos != -1:
                cut_positions.append(pos)
        for m_org in ORG_ENTITY_RE.finditer(header_wo_date):
            cut_positions.append(m_org.start())
        if cut_positions:
            first_pos = min(cut_positions)
            if first_pos > 0:
                header_wo_date = header_wo_date[first_pos:].lstrip(" ,.-–")

        desc_lines: List[str] = []
        for k in range(idx + 1, min(idx + 10, len(lines))):
            nxt = lines[k].strip()
            if not nxt:
                if desc_lines:
                    break
                else:
                    continue
            if parse_line_date(nxt):
                break
            low_nxt = nxt.lower()
            if any(h in low_nxt for h in STOP_HEADINGS):
                break
            desc_lines.append(nxt)

        combined_for_keywords = (header_wo_date + " " + " ".join(desc_lines)).lower()
        if not any(kw in combined_for_keywords for kw in JOB_TITLE_KEYWORDS):
            continue

        title, organization, location = parse_role_org_location(header_wo_date)

        fy = date_info["from_year"]
        fm = date_info["from_month"]
        if date_info["ongoing"]:
            ty = today.year
            tm = today.month
        else:
            ty = date_info["to_year"]
            tm = date_info["to_month"] or 12

        if ty is None or tm is None:
            duration_months = None
        else:
            duration_months = (ty - fy) * 12 + (tm - fm)
            if duration_months <= 0:
                continue

        if any(kw in combined_for_keywords for kw in TEACHING_KEYWORDS):
            category = "Teaching"
        elif any(kw in combined_for_keywords for kw in INDUSTRY_KEYWORDS):
            category = "Industry"
        else:
            category = "Other"

        title_org = ((title or "") + " " + (organization or "")).lower()
        strong_industry_kw = [
            "manager", "executive", "associate", "analyst", "engineer",
            "developer", "audit", "auditor", "accounts", "accountant",
            "process associate", "supermarts", "retail", "bank", "pvt", "ltd", "limited"
        ]
        strong_teaching_kw = [
            "professor", "lecturer", "teacher", "faculty",
            "school", "college", "university", "institute", "academy"
        ]
        if any(kw in title_org for kw in strong_industry_kw):
            category = "Industry"
        elif any(kw in title_org for kw in strong_teaching_kw):
            category = "Teaching"

        start_month = fm
        start_year = fy
        end_month = date_info["to_month"]
        end_year = date_info["to_year"]

        def fmt_date(yy: Optional[int], mm: Optional[int]) -> Optional[str]:
            if yy is None:
                return None
            if mm is None:
                return str(yy)
            abbr = MONTH_ABBR.get(mm, str(mm))
            return f"{abbr} {yy}"

        exp_entry = {
            "title": title,
            "organization": organization,
            "location": location,
            "category": category,
            "start_year": start_year,
            "start_month": start_month,
            "end_year": end_year,
            "end_month": end_month,
            "ongoing": bool(date_info["ongoing"]),
            "duration_months": duration_months,
            "start_date_str": fmt_date(start_year, start_month),
            "end_date_str": fmt_date(end_year, end_month) if not date_info["ongoing"] else "Present",
            "description": " ".join(desc_lines) if desc_lines else None,
            "raw_text": date_line + (" " + " ".join(desc_lines) if desc_lines else ""),
        }
        experiences.append(exp_entry)

    def sort_key(e: Dict[str, Any]) -> Tuple[int, int]:
        sy = e.get("start_year") or 0
        sm = e.get("start_month") or 0
        return (-sy, -sm)

    return sorted(experiences, key=sort_key)

# ---------- Publications breakdown ----------

def count_publications_breakdown(text: str) -> Dict[str, int]:
    lines = text.splitlines()
    start = None
    end = len(lines)

    for i, line in enumerate(lines):
        ll = line.lower()
        if any(
            kw in ll
            for kw in [
                "details of research publications",
                "research publications",
                "research experience",
                "journal papers",
            ]
        ):
            start = i
            break

    if start is None:
        return {"total": 0, "articles": 0, "books": 0, "conferences": 0}

    for j in range(start + 1, len(lines)):
        ll = lines[j].lower()
        if any(
            kw in ll
            for kw in [
                "faculty development",
                "refresher courses",
                "work experience",
                "professional experience",
                "employment history",
                "teaching",
                "declaration",
            ]
        ):
            end = j
            break

    total = 0
    articles = 0
    books = 0
    conferences = 0

    for line in lines[start:end]:
        if not re.match(r"^\s*(\d+\s*[).]|-\s)", line):
            continue
        total += 1
        low = line.lower()
        if "book" in low or "isbn" in low or "chapter" in low:
            books += 1
        elif any(k in low for k in ["journal", "volume", "issue", "issn", "paper published"]):
            articles += 1
        elif "conference" in low or "seminar" in low or "symposium" in low:
            conferences += 1
        else:
            articles += 1

    return {
        "total": total,
        "articles": articles,
        "books": books,
        "conferences": conferences,
    }

# ---------- MAIN PUBLIC FUNCTION ----------

def analyze_resume_text(
    text: str, target_department: Optional[str] = None
) -> Dict[str, Any]:
    education_text = extract_education_section(text)
    degrees_info = extract_degrees_detail(education_text, text)

    degree_types = [d["degree_type"] for d in degrees_info]
    degrees_detected = sorted(
        set(degree_types or detect_degrees_simple(text)),
        key=lambda d: DEGREE_PRIORITY.get(d, 0),
        reverse=True,
    )
    highest_deg = determine_highest_degree(degrees_detected)
    has_phd_flag = "PhD" in degrees_detected

    phd_start_year = None
    phd_end_year = None
    for d in degrees_info:
        if d["degree_type"] == "PhD":
            phd_start_year = d.get("start_year")
            phd_end_year = d.get("end_year")
            break

    fields_of_study: List[str] = []
    seen_fields = set()
    for d in degrees_info:
        f = d.get("field_of_study")
        if f:
            f_low = f.lower()
            if f_low not in seen_fields:
                seen_fields.add(f_low)
                fields_of_study.append(f)

    department = infer_department_from_fields(fields_of_study)
    if department == "Unknown":
        department = infer_department_from_text(text)

    experience_history_raw = extract_experience_history(text)
    experience_history = sorted(
        experience_history_raw,
        key=lambda e: ((e.get("start_year") or 0), (e.get("start_month") or 0)),
    )

    def build_exp_row(e: Dict[str, Any]) -> Dict[str, Any]:
        duration_years = None
        if e.get("duration_months") is not None:
            duration_years = round(e["duration_months"] / 12.0, 1)

        return {
            "organization": e.get("organization") or "-",
            "joining_date": e.get("start_date_str") or "-",
            "relieving_date": "Present" if e.get("ongoing") else (e.get("end_date_str") or "-"),
            "experience_type": e.get("category") or "Other",
            "duration_years": duration_years,
        }

    experience_rows = [build_exp_row(e) for e in experience_history]
    exp_breakdown = calculate_experience_breakdown(text)

    name = extract_name(text)
    email = extract_email(text)
    all_emails = extract_all_emails(text)
    phone = extract_phone(text)
    all_phones = extract_all_phones(text)
    location = extract_location(text)
    indian_states_found = extract_indian_states(text)

    current_org = extract_current_organization(text)
    current_role = None
    if experience_history:
        current_job = next(
            (e for e in experience_history if e.get("ongoing")),
            experience_history[-1],
        )
        if current_job.get("organization"):
            current_org = current_job["organization"]
        current_role = current_job.get("title")

    if not experience_rows and current_org:
        org_low = current_org.lower()
        if any(k in org_low for k in ["college", "school", "university", "institute", "academy"]):
            exp_type = "Teaching"
        else:
            exp_type = "Industry"

        experience_rows = [
            {
                "organization": current_org,
                "joining_date": "-",
                "relieving_date": "Present",
                "experience_type": exp_type,
                "duration_years": None,
            }
        ]
        experience_history = [
            {
                "title": current_role,
                "organization": current_org,
                "location": None,
                "category": exp_type,
                "start_year": None,
                "start_month": None,
                "end_year": None,
                "end_month": None,
                "ongoing": True,
                "duration_months": None,
                "start_date_str": "-",
                "end_date_str": "Present",
                "description": None,
                "raw_text": current_org,
            }
        ]

    pubs = count_publications_breakdown(text)
    score = score_resume(has_phd_flag, highest_deg, department, target_department)

    result: Dict[str, Any] = {
        "name": name,
        "email": email,
        "all_emails": all_emails,
        "phone": phone,
        "all_phones": all_phones,
        "current_location": location,
        "indian_states_found": indian_states_found,
        "current_organization": current_org,
        "current_role": current_role,

        "teaching_experience_years": exp_breakdown["teaching_years"],
        "industry_experience_years": exp_breakdown["industry_years"],
        "other_experience_years": exp_breakdown["other_years"],
        "total_experience_years": exp_breakdown["total_years"],

        "experience_history": experience_history,
        "experience_rows": experience_rows,

        "publications_total_count": pubs["total"],
        "research_articles_count": pubs["articles"],
        "books_count": pubs["books"],
        "conference_papers_count": pubs["conferences"],
        "has_phd": has_phd_flag,
        "highest_degree": highest_deg,
        "phd_start_year": phd_start_year,
        "phd_end_year": phd_end_year,
        "department": department,
        "degrees_detected": degrees_detected,
        "degrees_info": degrees_info,
        "fields_of_study": fields_of_study,
        "score": score,
    }
    return result
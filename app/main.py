from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import uuid
import json
import re
import html

from .resume_parser.text_cleaner import clean_text
from .resume_parser.section_extractor import extract_sections
from .resume_parser.skill_extractor import extract_skills
from .resume_parser.advanced_analyzer import analyze_resume_text
from .utils.file_extractor import extract_text_from_bytes

main_bp = Blueprint("main", __name__)


def allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in current_app.config["ALLOWED_EXTENSIONS"]


def build_highlighted_text(raw_text: str, advanced: dict) -> str:
    """
    Build HTML version of raw_text with degree-related parts and
    experience-related parts highlighted using <mark> tags.
    Degree highlights -> .hl-degree
    Experience highlights -> .hl-exp
    """
    # Start from HTML-escaped text for safety
    text_html = html.escape(raw_text)

    degree_phrases = set()
    exp_phrases = set()

    # Collect degree-related phrases
    for deg in advanced.get("degrees_info", []):
        if deg.get("raw_text"):
            degree_phrases.add(deg["raw_text"])
        if deg.get("institution"):
            degree_phrases.add(deg["institution"])
        if deg.get("field_of_study"):
            degree_phrases.add(deg["field_of_study"])

    # Collect experience-related phrases
    for exp in advanced.get("experience_history", []):
        if exp.get("raw_text"):
            exp_phrases.add(exp["raw_text"])
        if exp.get("organization"):
            exp_phrases.add(exp["organization"])
        if exp.get("title"):
            exp_phrases.add(exp["title"])

    # Clean and sort phrases by length (longest first)
    degree_list = sorted(
        [p for p in degree_phrases if len(p.strip()) >= 3],
        key=len,
        reverse=True,
    )
    exp_list = sorted(
        [p for p in exp_phrases if len(p.strip()) >= 3],
        key=len,
        reverse=True,
    )

    # Apply highlights for degree phrases
    for phrase in degree_list:
        escaped_phrase = re.escape(html.escape(phrase))
        text_html = re.sub(
            escaped_phrase,
            r'<mark class="hl-degree">\g<0></mark>',
            text_html,
            flags=re.IGNORECASE,
        )

    # Apply highlights for experience phrases
    for phrase in exp_list:
        escaped_phrase = re.escape(html.escape(phrase))
        text_html = re.sub(
            escaped_phrase,
            r'<mark class="hl-exp">\g<0></mark>',
            text_html,
            flags=re.IGNORECASE,
        )

    return text_html


@main_bp.route("/", methods=["GET", "POST"])
def index():
    # --------- POST: user uploaded a resume ---------
    if request.method == "POST":
        if "resume" not in request.files:
            flash("No file part in the request", "error")
            return redirect(request.url)

        file = request.files["resume"]
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Unsupported file type. Allowed: PDF, DOCX, TXT", "error")
            return redirect(request.url)

        # Save & extract text
        filename = secure_filename(file.filename)
        ext = Path(filename).suffix
        unique_name = f"{uuid.uuid4().hex}{ext}"
        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        file_path = upload_folder / unique_name

        # Read file into memory once
        file_bytes = file.read()

        # Save file for reference
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        try:
            # 1) Text extraction (PyMuPDF + pdfplumber + DOCX/TXT)
            raw_text = extract_text_from_bytes(file_bytes, filename)

            # 2) Clean/normalize
            cleaned_text, lines = clean_text(raw_text)

            # 3) Sections and skills
            sections = extract_sections(lines)
            skills = extract_skills(cleaned_text)

            # 4) Advanced analysis (your big analyzer)
            advanced = analyze_resume_text(cleaned_text)

            # 5) Highlighted HTML version of resume text
            highlighted_text = build_highlighted_text(cleaned_text, advanced)

            # 6) Build result object passed to template
            analysis_result = {
                "file_name": filename,
                "sections": sections,
                "skills": skills,
                "raw_text": cleaned_text,
                "raw_preview": "\n".join(lines[:40]),
                "advanced": advanced,
                "highlighted_text": highlighted_text,
            }

            json_result = json.dumps(analysis_result, indent=4, ensure_ascii=False)

            # THIS is the line you asked about: it lives here,
            # inside the POST branch, returning the result page.
            return render_template(
                "result.html",
                result=analysis_result,
                json_result=json_result,
            )

        except Exception as e:
            flash(f"Error processing file: {e}", "error")
            return redirect(request.url)

    # --------- GET: just show the upload form ---------
    return render_template("index.html")
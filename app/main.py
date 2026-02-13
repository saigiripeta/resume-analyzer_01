from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import uuid
import json

import re            # <--- add
import html          # <--- add

# We no longer use the old path-based extractor
# from .resume_parser.file_reader import extract_text_from_file

from .resume_parser.text_cleaner import clean_text
from .resume_parser.section_extractor import extract_sections
from .resume_parser.skill_extractor import extract_skills
from .resume_parser.advanced_analyzer import analyze_resume_text
from .utils.file_extractor import extract_text_from_bytes   # <--- NEW

main_bp = Blueprint("main", __name__)


def allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in current_app.config["ALLOWED_EXTENSIONS"]


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # ---- basic validation ----
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

        # ---- save & extract text (THIS IS THE BLOCK YOU ASKED ABOUT) ----
        filename = secure_filename(file.filename)
        ext = Path(filename).suffix
        unique_name = f"{uuid.uuid4().hex}{ext}"
        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        file_path = upload_folder / unique_name

        # Read file once into memory
        file_bytes = file.read()

        # Save file bytes for reference
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Extract text using PyMuPDF + pdfplumber + docx/txt
        try:
            raw_text = extract_text_from_bytes(file_bytes, filename)

            # ---- downstream analysis ----
            cleaned_text, lines = clean_text(raw_text)

            sections = extract_sections(lines)
            skills = extract_skills(cleaned_text)

            # advanced_analyzer: name, phones, experience, degrees, etc.
            advanced = analyze_resume_text(cleaned_text)

            analysis_result = {
                "file_name": filename,
                "sections": sections,
                "skills": skills,
                "raw_text": cleaned_text,
                "raw_preview": "\n".join(lines[:40]),
                "advanced": advanced,
            }

            json_result = json.dumps(analysis_result, indent=4, ensure_ascii=False)

            return render_template(
                "result.html",
                result=analysis_result,
                json_result=json_result,
            )

        except Exception as e:
            flash(f"Error processing file: {e}", "error")
            return redirect(request.url)

    # GET -> just show upload form
    return render_template("index.html")
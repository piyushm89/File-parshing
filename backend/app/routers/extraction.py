import os
import shutil
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from app.services.parser_services import (
    extract_text_from_pdf,
    extract_text_from_docx,
)

from app.services.llm_service import extract_fields

router = APIRouter()

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/extract")
async def extract(
    file: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None),
):
    # Validate input
    if file is None and (text is None or text.strip() == ""):
        return {
            "status": "error",
            "message": "Please upload a PDF/DOCX file or enter text."
        }

    # ---------- User pasted text ----------
    if file is None:
        structured_data = extract_fields(text)

        if isinstance(structured_data, dict) and structured_data.get("status") == "error":
            return {
                "status": "error",
                "message": structured_data.get("message", "Failed to extract data from text.")
            }

        return {
            "status": "success",
            "input_type": "text",
            "data": structured_data
        }

    # ---------- Validate extension before saving ----------
    safe_filename = os.path.basename(file.filename)
    extension = os.path.splitext(safe_filename)[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return {
            "status": "error",
            "message": "Only PDF and DOCX files are supported."
        }

    # ---------- Create uploads folder ----------
    os.makedirs("uploads", exist_ok=True)

    # ---------- Save uploaded file ----------
    upload_path = os.path.join("uploads", safe_filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- Extract text based on extension ----------
    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(upload_path)
    else:
        extracted_text = extract_text_from_docx(upload_path)

    # ---------- Send text to Mistral ----------
    structured_data = extract_fields(extracted_text)

    if isinstance(structured_data, dict) and structured_data.get("status") == "error":
        return {
            "status": "error",
            "message": structured_data.get("message", "Failed to extract data from document.")
        }

    # ---------- Return response ----------
    return {
        "status": "success",
        "input_type": "file",
        "filename": safe_filename,
        "content_type": file.content_type,
        "data": structured_data
    }

    
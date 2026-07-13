import os
import shutil
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from app.services.parser_services import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_excel,
)

from app.services.llm_service import extract_fields

router = APIRouter()

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".xlsx",
}


@router.post("/extract")
async def extract(
    file: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None),
):

    # -----------------------------
    # Validate Input
    # -----------------------------
    if file is None and (text is None or text.strip() == ""):
        return {
            "status": "error",
            "message": "Please upload a PDF, DOCX, XLSX file or enter text."
        }

    # -----------------------------
    # User Entered Text
    # -----------------------------
    if file is None:

        structured_data = extract_fields(text)

        if (
            isinstance(structured_data, dict)
            and structured_data.get("status") == "error"
        ):
            return {
                "status": "error",
                "message": structured_data.get(
                    "message",
                    "Failed to extract data from text."
                )
            }

        return {
            "status": "success",
            "input_type": "text",
            "data": structured_data
        }

    # -----------------------------
    # File Validation
    # -----------------------------
    safe_filename = os.path.basename(file.filename)

    extension = os.path.splitext(safe_filename)[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return {
            "status": "error",
            "message": "Only PDF, DOCX and XLSX files are supported."
        }

    # -----------------------------
    # Create Upload Folder
    # -----------------------------
    os.makedirs("uploads", exist_ok=True)

    upload_path = os.path.join("uploads", safe_filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # Extract Text
    # -----------------------------
    try:

        if extension == ".pdf":

            extracted_text = extract_text_from_pdf(upload_path)

        elif extension == ".docx":

            extracted_text = extract_text_from_docx(upload_path)

        elif extension == ".xlsx":

            extracted_text = extract_text_from_excel(upload_path)

        else:

            return {
                "status": "error",
                "message": "Unsupported file type."
            }

    except Exception as e:

        return {
            "status": "error",
            "message": f"Failed to read file: {str(e)}"
        }

    # -----------------------------
    # LLM Extraction
    # -----------------------------
    structured_data = extract_fields(extracted_text)

    if (
        isinstance(structured_data, dict)
        and structured_data.get("status") == "error"
    ):
        return {
            "status": "error",
            "message": structured_data.get(
                "message",
                "Failed to extract data from document."
            )
        }

    # -----------------------------
    # Optional Cleanup
    # -----------------------------
    try:
        os.remove(upload_path)
    except Exception:
        pass

    # -----------------------------
    # Response
    # -----------------------------
    return {
        "status": "success",
        "input_type": "file",
        "filename": safe_filename,
        "content_type": file.content_type,
        "data": structured_data
    }
import os
import shutil
import time
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from app.services.parser_services import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_excel,
)

from app.utils.text_cleaner import clean_text
from app.services.regex_service import extract_simple_fields
from app.services.keyword_service import extract_relevant_sections
from app.services.llm_service import extract_fields

router = APIRouter()

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx"}


@router.post("/extract")
async def extract(
    file: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None),
):
    request_start = time.perf_counter()

    print("\n" + "=" * 60)
    print(" New Extraction Request")
    print("=" * 60)

    if file is None and (text is None or text.strip() == ""):
        return {
            "status": "error",
            "message": "Please upload a PDF, DOCX, XLSX file or enter text."
        }

    safe_filename = None
    content_type = None

    if file is None:
        print(" Input Type : Text")
        raw_text = text
    else:
        safe_filename = os.path.basename(file.filename)
        extension = os.path.splitext(safe_filename)[1].lower()

        if extension not in SUPPORTED_EXTENSIONS:
            return {
                "status": "error",
                "message": "Only PDF, DOCX and XLSX files are supported."
            }

        print(f" File : {safe_filename}")
        content_type = file.content_type

        os.makedirs("uploads", exist_ok=True)
        upload_path = os.path.join("uploads", safe_filename)

        save_start = time.perf_counter()
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        save_end = time.perf_counter()
        print(f" File Save Time : {save_end - save_start:.2f} sec")

        try:
            parse_start = time.perf_counter()

            if extension == ".pdf":
                raw_text = extract_text_from_pdf(upload_path)
            elif extension == ".docx":
                raw_text = extract_text_from_docx(upload_path)
            elif extension == ".xlsx":
                raw_text = extract_text_from_excel(upload_path)
            else:
                return {"status": "error", "message": "Unsupported file type."}

            parse_end = time.perf_counter()
            print(f" Text Extraction : {parse_end - parse_start:.2f} sec")
            print(f" Extracted Characters : {len(raw_text):,}")

        except Exception as e:
            return {"status": "error", "message": f"Failed to read file: {str(e)}"}

        finally:
            try:
                os.remove(upload_path)
            except Exception:
                pass

    # ---------------------------------------------------
    # Step 1: Clean Text
    # ---------------------------------------------------
    clean_start = time.perf_counter()
    cleaned_text = clean_text(raw_text)
    clean_end = time.perf_counter()
    clean_time = clean_end - clean_start

    # ---------------------------------------------------
    # Step 2: Regex Extraction (deterministic fields)
    # ---------------------------------------------------
    regex_start = time.perf_counter()
    regex_data = extract_simple_fields(cleaned_text)
    regex_end = time.perf_counter()
    regex_time = regex_end - regex_start

    # ---------------------------------------------------
    # Step 3: Keyword Extraction (reduce LLM context)
    # ---------------------------------------------------
    keyword_start = time.perf_counter()
    _, relevant_context = extract_relevant_sections(cleaned_text)
    keyword_end = time.perf_counter()
    keyword_time = keyword_end - keyword_start

    if len(relevant_context) > len(cleaned_text):
        relevant_context = cleaned_text

    print("\nREGEX DATA")
    print("-" * 40)
    print(regex_data)
    print("-" * 40)

    # ---------------------------------------------------
    # Step 4: LLM Extraction (only complex fields)
    # Extract_fields merges regex_data into final result internally
    # ---------------------------------------------------
    llm_start = time.perf_counter()
    merged_data = extract_fields(relevant_context, regex_data)
    llm_end = time.perf_counter()
    llm_time = llm_end - llm_start

    if isinstance(merged_data, dict) and merged_data.get("status") == "error":
        return {
            "status": "error",
            "message": merged_data.get("message", "Failed to extract data from document.")
        }

    print("\nFINAL DATA")
    print("-" * 40)
    print(merged_data)
    print("-" * 40)
    # ---------------------------------------------------
    # Timing Summary
    # ---------------------------------------------------
    request_end = time.perf_counter()
    total_time = request_end - request_start

    print("-" * 60)
    print(" Pipeline Timing Summary")
    print("-" * 60)
    print(f" Text Cleaner    : {clean_time:.2f} sec")
    print(f" Regex           : {regex_time:.2f} sec")
    print(f" Keyword         : {keyword_time:.2f} sec")
    print(f" LLM             : {llm_time:.2f} sec")
    print(f" Total           : {total_time:.2f} sec")
    print("=" * 60)

    if file is None:
        return {
            "status": "success",
            "input_type": "text",
            "data": merged_data,
        }

    return {
        "status": "success",
        "input_type": "file",
        "filename": safe_filename,
        "content_type": content_type,
        "data": merged_data,
    }

import fitz
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)

    text = ""

    # Extract paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text.strip() + "\n"

    # Extract tables
    for table in document.tables:
        for row in table.rows:
            row_data = []

            for cell in row.cells:
                value = cell.text.strip()

                if value:
                    row_data.append(value)

            if row_data:
                text += " : ".join(row_data) + "\n"

    return text
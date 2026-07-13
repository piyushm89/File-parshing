import re
from collections import Counter

UNWANTED_SECTIONS = [
    "Certificate Details",
    "Thumbprint",
    "General Terms & Conditions",
    "General Terms and Conditions",
    "(n)Procure Support team",
    "Tender Documents",
    "Digital Certificate",
    "Vendor Training",
    "Free vendor training camp",
    "E-mail :",
    "Email :",
    "TOLL FREE NUMBER",
    "Support Contact",
    "Help Desk",
    "Technical Support",
    "Customer Support",
]

HEADER_FOOTER_THRESHOLD = 3


def remove_unwanted_sections(text: str) -> str:
    lower_text = text.lower()
    cut_position = len(text)
    for section in UNWANTED_SECTIONS:
        idx = lower_text.find(section.lower())
        if idx != -1:
            cut_position = min(cut_position, idx)
    return text[:cut_position]


def remove_page_numbers(text: str) -> str:
    patterns = [
        r"Page\s+\d+\s+of\s+\d+",
        r"Page\s+\d+",
        r"\n\s*\d{1,4}\s*\n",
        r"(?<!\d)-\s*\d{1,3}\s*-(?!\d)",
    ]
    for pattern in patterns:
        text = re.sub(pattern, "\n", text, flags=re.IGNORECASE)
    return text


def remove_repeated_headers_footers(text: str) -> str:
    lines = text.splitlines()
    line_counts = Counter(line.strip() for line in lines if line.strip())
    repeated = {line for line, count in line_counts.items() if count >= HEADER_FOOTER_THRESHOLD}
    cleaned = []
    for line in lines:
        if line.strip() in repeated:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def remove_duplicate_lines(text: str) -> str:
    cleaned = []
    previous = ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line == previous:
            continue
        cleaned.append(line)
        previous = line
    return "\n".join(cleaned)


def remove_extra_spaces(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def remove_urls_and_emails(text: str) -> str:
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"www\.\S+", "", text)
    return text


def remove_phone_numbers(text: str) -> str:
    text = re.sub(r"\b\d{10}\b", "", text)
    text = re.sub(r"\b\d{11,13}\b", "", text)
    text = re.sub(r"\+91[\s-]?\d{10}", "", text)
    return text


def normalize_currency(text: str) -> str:
    text = text.replace("Rs.", "INR")
    text = text.replace("Rs ", "INR ")
    text = text.replace("₹", "INR ")
    return text


def clean_text(text: str) -> str:
    original_length = len(text)

    text = remove_unwanted_sections(text)
    text = remove_page_numbers(text)
    text = remove_repeated_headers_footers(text)
    text = remove_urls_and_emails(text)
    text = remove_phone_numbers(text)
    text = normalize_currency(text)
    text = remove_duplicate_lines(text)
    text = remove_extra_spaces(text)

    cleaned_length = len(text)

    print("")
    print(" Text Cleaner")
    print("-" * 40)
    print(f"Original Characters : {original_length:,}")
    print(f"Cleaned Characters  : {cleaned_length:,}")

    reduction = original_length - cleaned_length
    print(f"Reduced Characters  : {reduction:,}")

    if original_length > 0:
        percent = (reduction / original_length) * 100
        print(f"Reduction           : {percent:.2f}%")
    print("-" * 40)

    return text

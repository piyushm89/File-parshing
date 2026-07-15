import re
from typing import Dict

# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(text: str) -> str:
    """
    Normalize extracted text while preserving line structure.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove duplicate blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ==========================================================
# CLEAN VALUE
# ==========================================================

def clean_value(value: str) -> str:

    if not value:
        return ""

    value = value.replace("\n", " ")

    value = re.sub(r"\s+", " ", value)

    value = value.strip()

    value = value.rstrip(":")
    value = value.rstrip("-")

    return value.strip()


# ==========================================================
# EXTRACT BETWEEN TWO LABELS
# ==========================================================

def extract_between(
    text: str,
    start_label: str,
    end_label: str | None = None,
) -> str:

    start = text.lower().find(start_label.lower())

    if start == -1:
        return ""

    start += len(start_label)

    if end_label:

        end = text.lower().find(end_label.lower(), start)

        if end == -1:
            value = text[start:]
        else:
            value = text[start:end]

    else:
        value = text[start:]

    return clean_value(value)


# ==========================================================
# EXTRACT USING REGEX
# ==========================================================

def extract_regex(pattern: str, text: str) -> str:

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    if not match:
        return ""

    return clean_value(match.group(1))


# ==========================================================
# DATE CLEANER
# ==========================================================

def clean_date(value: str) -> str:

    match = re.search(
        r"\d{2}[-/]\d{2}[-/]\d{4}(?:\s+\d{2}:\d{2})?",
        value,
    )

    if match:
        return match.group()

    return clean_value(value)


# ==========================================================
# MONEY CLEANER
# ==========================================================

def clean_money(value: str) -> str:

    match = re.search(
        r"[\d,]+(?:\.\d+)?\s*INR",
        value,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group()

    match = re.search(
        r"[\d,]+(?:\.\d+)?",
        value,
    )

    if match:
        return match.group()

    return clean_value(value)


# ==========================================================
# YES / NO CLEANER
# ==========================================================

def clean_yes_no(value: str) -> str:

    value = clean_value(value)

    if value.lower().startswith("yes"):
        return "Yes"

    if value.lower().startswith("no"):
        return "No"

    return value

# ==========================================================
# FIELD BOUNDARIES
# ==========================================================

FIELD_BOUNDARIES = {

    "tender_id": (
        "Tender ID",
        "View BOQ"
    ),

    "authority_name": (
        "Organization Name",
        "Location"
    ),

    "district": (
        "Location",
        "Department"
    ),

    "department": (
        "Department",
        "Sub Department"
    ),

    "tender_reference_no": (
        "IFB/Tender Notice No",
        "Tender Type"
    ),

    "tender_type": (
        "Tender Type",
        "Tender title/Name Of Project"
    ),

    "tender_title": (
        "Tender title/Name Of Project",
        "Description of Material/Name of Work"
    ),

    "tender_description": (
        "Description of Material/Name of Work",
        "Sector Category"
    ),

    "sector": (
        "Sector Category",
        "Form of Contract"
    ),

    "contract_type": (
        "Form of Contract",
        "Product Category"
    ),

    "tender_category": (
        "Tender Category",
        "Tender Currency Type"
    ),

    "currency": (
        "Tender Currency Setting",
        "Period of Completion/Delivery Period"
    ),

    "delivery_period": (
        "Period of Completion/Delivery Period",
        "Procurement Type"
    ),

    "procurement_type": (
        "Procurement Type",
        "Consortium / Joint Venture"
    ),

    "document_download_start": (
        "Bid Document Download Start Date",
        "Bid document download End Date"
    ),

    "document_download_end": (
        "Bid document download End Date",
        "Bid Submission Start Date"
    ),

    "submission_start_date": (
        "Bid Submission Start Date",
        "Bid Submission Closing Date"
    ),

    "submission_deadline": (
        "Bid Submission Closing Date",
        "Tender NIT View Date"
    ),

    "bid_validity": (
        "Bid validity",
        "Amount Details"
    ),

    "tender_fee": (
        "Bidding Processing Fee ( OFFLINE)",
        "Bidding Processing Fee Payable to"
    ),

    "emd_amount": (
        "Bid Security/EMD/Proposal Security INR ( OFFLINE)",
        "Bid Security/EMD/Proposal Security INR Payable to"
    ),

    "emd_type": (
        "EMD Fee Exempted",
        "Bank Guarantee Minimum"
    ),

    "authority_type": (
        "Authority Type",
        "Department"
    ),

    "state_ut": (
        "State",
        "District"
    ),

    "bid_open_date": (
        "Evaluation Date",
        "Minimum Forms for Submission"
    ),
}


# ==========================================================
# SPECIAL FIELD HANDLERS
# ==========================================================

DATE_FIELDS = {
    "document_download_start",
    "document_download_end",
    "submission_start_date",
    "submission_deadline",
    "bid_open_date",
}

MONEY_FIELDS = {
    "emd_amount",
    "tender_fee",
}

YES_NO_FIELDS = {
    "emd_type",
}

# ==========================================================
# MAIN EXTRACTION FUNCTION
# ==========================================================

def extract_simple_fields(text: str) -> Dict:

    text = normalize_text(text)

    result = {}

    print("")
    print("Regex Extraction")
    print("-" * 50)

    found = 0

    for field, (start_label, end_label) in FIELD_BOUNDARIES.items():

        value = extract_between(
            text=text,
            start_label=start_label,
            end_label=end_label,
        )

        if field in DATE_FIELDS:
            value = clean_date(value)

        elif field in MONEY_FIELDS:
            value = clean_money(value)

        elif field in YES_NO_FIELDS:
            value = clean_yes_no(value)

        result[field] = value

        if value:
            found += 1
            print(f"✅ {field:30} : {value}")

    # ------------------------------------------------------
    # FALLBACK REGEX EXTRACTION
    # ------------------------------------------------------

    if not result["state_ut"]:

        state = extract_regex(
            r"ST=([^,\n]+)",
            text,
        )

        result["state_ut"] = state

    if not result["sector"]:

        sector = extract_regex(
            r"Sector Category\s*(.*?)\s*Form of Contract",
            text,
        )

        result["sector"] = sector

    if not result["contract_type"]:

        contract = extract_regex(
            r"Form of Contract\s*(.*?)\s*Product Category",
            text,
        )

        result["contract_type"] = contract

    if not result["currency"]:

        currency = extract_regex(
            r"Tender Currency Setting\s*(.*?)\s*Period of Completion",
            text,
        )

        result["currency"] = currency

    if not result["procurement_type"]:

        procurement = extract_regex(
            r"Procurement Type\s*(.*?)\s*Consortium",
            text,
        )

        result["procurement_type"] = procurement

    if not result["department"]:

        department = extract_regex(
            r"Department\s*(.*?)\s*Sub Department",
            text,
        )

        result["department"] = department

    if not result["district"]:

        district = extract_regex(
            r"Location\s*(.*?)\s*Department",
            text,
        )

        result["district"] = district

    if not result["authority_name"]:

        authority = extract_regex(
            r"Organization Name\s*(.*?)\s*Location",
            text,
        )

        result["authority_name"] = authority

    if not result["tender_reference_no"]:

        ref = extract_regex(
            r"IFB/Tender Notice No\s*(.*?)\s*Tender Type",
            text,
        )

        result["tender_reference_no"] = ref

    print("-" * 50)
    print(f"Regex Fields Found : {found}/{len(FIELD_BOUNDARIES)}")
    print("-" * 50)

    return result

# ==========================================================
# EXTRACTION HELPERS FOR COMPLEX FIELDS
# ==========================================================

def extract_mandatory_documents(text: str) -> str:

    pattern = (
        r"Documents required for Stage.*?"
        r"Mandatory(.*?)(?:Commercial Stage|Certificate Details|$)"
    )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return ""

    section = match.group(1)

    docs = []

    for line in section.splitlines():

        line = clean_value(line)

        if not line:
            continue

        if "yes" in line.lower():

            line = re.sub(r"^\d+\s*", "", line)

            line = re.sub(r"\s+Yes$", "", line, flags=re.I)

            docs.append(line)

    return ", ".join(dict.fromkeys(docs))


def extract_submission_mode(text: str) -> str:

    modes = []

    lower = text.lower()

    if "electronic format" in lower:
        modes.append("Electronic")

    if "physical submission" in lower:
        modes.append("Physical")

    if "speed post" in lower:
        modes.append("Speed Post")

    if "rpad" in lower:
        modes.append("RPAD")

    if "in person" in lower:
        modes.append("In Person")

    return ", ".join(modes)


def extract_evaluation_method(text: str) -> str:

    lower = text.lower()

    if "technical bid" in lower and "price bid" in lower:
        return "Technical Bid + Price Bid"

    if "qcbs" in lower:
        return "QCBS"

    if "l1" in lower:
        return "L1"

    return ""


def extract_disqualification(text: str) -> str:

    keywords = [
        "blacklisted",
        "debarred",
        "liable to rejection",
        "rejected",
        "terminated",
    ]

    found = []

    lower = text.lower()

    for word in keywords:

        if word in lower:
            found.append(word)

    return ", ".join(found)


# ==========================================================
# ENRICH REGEX RESULT
# ==========================================================

def enrich_fields(result: Dict, text: str) -> Dict:

    result["mandatory_documents"] = extract_mandatory_documents(text)

    result["submission_mode"] = extract_submission_mode(text)

    result["document_submission_mode"] = result["submission_mode"]

    result["evaluation_method"] = extract_evaluation_method(text)

    result["disqualification_clauses"] = extract_disqualification(text)

    return result
import re


FIELD_PATTERNS = {
    "tender_id": [
        r"Tender[ \t]*ID[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Tender[ \t]*No[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Tender[ \t]*Number[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Bid[ \t]*No[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "tender_reference_no": [
        r"IFB/Tender Notice No[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Tender Reference No[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Tender Ref(?:erence)? No[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"NIT No[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Bid Reference[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Notice No[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Reference No[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "authority_name": [
        r"Organization Name[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Authority Name[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Organisation Name[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Inviting Authority[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"(?:Name of )(?:the )?Authority[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "authority_type": [
        r"Authority Type[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Organization Type[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "department": [
        r"^Department[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Office Name[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "tender_title": [
        r"Tender title/Name Of Project[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Tender Title[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Name of Work[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Project Name[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "tender_type": [
        r"Tender Type[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Type of Tender[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "tender_category": [
        r"Tender Category[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"^Category[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "procurement_type": [
        r"Procurement Type[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Type of Procurement[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "sector": [
        r"Sector Category[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"^Sector[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"ST=([^,\n]+)",
    ],

    "contract_type": [
        r"Form of Contract[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Contract Type[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Type of Contract[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "state_ut": [
        r"ST=([^,\n]+)",
        r"State/UT[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"^State[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "district": [
        r"Location[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"District[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "currency": [
        r"Tender Currency Setting[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"^Currency[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "emd_amount": [
        r"Bid Security/EMD.*?([\d,]+(?:\s*INR)?)",
        r"EMD Amount[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Earnest Money Deposit[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"EMD[ \t]*[:\-]?[ \t]*(?:INR[ \t]*)?([\d,]+)",
    ],

    "emd_type": [
        r"EMD Fee Exempted[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"EMD Type[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Bid Security[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "tender_fee": [
        r"Bidding Processing Fee.*?([\d,]+(?:\s*INR)?)",
        r"Tender Fee[ \t]*[:\-]?[ \t]*(?!(?:Payment|payment))([^\n]+)",
        r"Cost of Tender[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Tender Cost[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "tender_fee_payment_mode": [
        r"Tender Fee Payment Mode[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Payment Mode[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Fee Payment Mode[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "bid_validity": [
        r"Bid validity[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Bid Validity[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Validity Period[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "delivery_period": [
        r"Period of Completion/Delivery Period[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Delivery Period[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Period of Completion[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "submission_deadline": [
        r"Bid Submission Closing Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Submission Deadline[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Closing Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Last Date for Submission[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "submission_start_date": [
        r"Bid Submission Start Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Submission Start Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Start Date[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "document_download_start": [
        r"Bid Document Download Start Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Document Download Start[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Download Start Date[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "document_download_end": [
        r"Bid document download End Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Document Download End[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Download End Date[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],

    "bid_open_date": [
        r"Evaluation Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Bid Opening Date[ \t]*[:\-]?[ \t]*([^\n]+)",
        r"Bid Open Date[ \t]*[:\-]?[ \t]*([^\n]+)",
    ],
}


def clean_value(value: str) -> str:
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    value = value.strip()

    STOP_WORDS = [
        "View BOQ",
        "Organization Name",
        "Organisation Name",
        "Authority Name",
        "Location",
        "Department",
        "Sub Department",
        "Tender Type",
        "Tender title",
        "Tender Title",
        "Name Of Project",
        "Project Name",
        "Tender Category",
        "Procurement Type",
        "Sector",
        "Contract Type",
        "State",
        "District",
        "Currency",
        "EMD",
        "Tender Fee",
        "Payment Mode",
        "Bid validity",
        "Delivery Period",
        "Bid Submission",
        "Document Download",
        "Evaluation Date",
    ]

    for word in STOP_WORDS:
        index = value.lower().find(word.lower())
        if index > 0:
            value = value[:index].strip()

    return value.rstrip(":- ").strip()


def extract_simple_fields(text: str) -> dict:
    result = {}

    print("")
    print(" Regex Extraction")
    print("-" * 40)

    found = 0

    for field, patterns in FIELD_PATTERNS.items():
        result[field] = ""

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.MULTILINE,
            )

            if match:
                value = clean_value(match.group(1))

                if value:
                    result[field] = value
                    found += 1
                    print(f" {field} : {value}")
                    break

    print("-" * 40)
    print(f"Regex Fields Found : {found}/{len(FIELD_PATTERNS)}")
    print("-" * 40)

    return result
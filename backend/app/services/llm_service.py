import os
import json

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def extract_fields(document_text: str):

    prompt = f"""
You are an expert AI specialized in extracting structured information from Indian Government Tender, NIT, RFP, RFQ, Procurement and e-Tender documents.

The document may contain:
- Tables
- Bullet Lists
- OCR errors
- Multi-column layouts
- Headers and Footers
- Corrigendum / Addendum
- Annexures
- Repeated values
- Historical values
- Different date formats
- Currency symbols (₹, INR, Rs.)
- Information scattered across multiple pages

YOUR OBJECTIVE

Extract ONLY the required fields listed below.

RULES

1. Read the COMPLETE document before answering.
2. Search BOTH tables and paragraphs.
3. Search ALL pages before deciding a field is missing.
4. Ignore headers, footers, page numbers and repeated OCR text.
5. If multiple values exist, choose the LATEST VALID VALUE.
6. Corrigendum always overrides previous information.
7. Preserve dates exactly as written.
8. Preserve currency exactly as written.
9. Preserve abbreviations like QCBS, EPC, EMD, GST, BOQ, NIT.
10. Never invent or guess values.
11. If a field does not exist, return an empty string "".
12. Return ONLY valid JSON.
13. Do NOT return markdown.
14. Do NOT wrap the response inside ```json.
15. Do NOT explain anything.
16. Every key below MUST exist in the response.

Return EXACTLY this JSON:

{{
    "tender_reference_no": "",
    "authority_name": "",
    "authority_type": "",
    "department": "",

    "tender_title": "",
    "tender_description": "",
    "tender_type": "",
    "tender_category": "",
    "procurement_type": "",
    "sector": "",
    "contract_type": "",

    "state_ut": "",
    "district": "",

    "tender_publish_date": "",
    "document_download_start": "",
    "document_download_end": "",
    "submission_start_date": "",
    "submission_deadline": "",
    "bid_open_date": "",
    "delivery_period": "",
    "bid_validity": "",

    "currency": "",
    "emd_amount": "",
    "emd_type": "",
    "tender_fee": "",
    "tender_fee_payment_mode": "",

    "submission_mode": "",
    "mandatory_documents": "",
    "document_submission_mode": "",

    "evaluation_method": "",
    "disqualification_clauses": ""
}}

Extraction Guidelines

- Tender Reference Number may appear as:
  Tender Ref No
  Tender Reference No
  NIT No
  Bid Reference
  Reference Number

- Authority Name may appear under:
  Organization
  Department
  Authority
  Office
  Procuring Entity

- Tender Fee and EMD may appear inside tables.

- State and District may appear inside the address.

- Delivery Period may also appear as:
  Completion Period
  Work Completion
  Project Duration
  Time for Completion

- Submission Deadline may also appear as:
  Last Date of Submission
  Bid Closing Date
  Bid Due Date

- Bid Opening may also appear as:
  Technical Bid Opening
  Financial Bid Opening
  Opening Date

- Mandatory Documents are usually bullet points or numbered lists.

- Evaluation Method may appear as:
  QCBS
  L1
  Least Cost
  Technical Evaluation
  Quality & Cost Based Selection

Examples

Example 1

EMD Amount : ₹5,00,000

Return

"emd_amount": "₹5,00,000"

-----------------------------------

Example 2

Tender Fee : Rs. 2500 + GST

Return

"tender_fee": "Rs. 2500 + GST"

-----------------------------------

Example 3

Completion Period : 180 Days

Return

"delivery_period": "180 Days"

-----------------------------------

Example 4

Bid Opening : Refer Corrigendum

Return

"bid_open_date": ""

-----------------------------------

Example 5

If a field is missing anywhere in the document:

Return

"field_name": ""

Document:

{document_text}
"""

    model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        return {
            "status": "error",
            "message": "Invalid JSON returned by Mistral.",
            "raw_response": content,
        }
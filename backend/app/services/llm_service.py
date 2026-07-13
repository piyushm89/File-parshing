import os
import json
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

COMPLEX_FIELDS = [
    "tender_description",
    "mandatory_documents",
    "document_submission_mode",
    "submission_mode",
    "evaluation_method",
    "disqualification_clauses",
]


def build_prompt(context: str, regex_data: dict) -> str:
    remaining = [f for f in COMPLEX_FIELDS if not regex_data.get(f)]

    regex_preview = {k: v for k, v in regex_data.items() if k in COMPLEX_FIELDS and v}

    return (
        "Extract Indian Government Tender fields from the context below.\n\n"
        f"Regex already extracted: {json.dumps(regex_preview)}\n\n"
        f"Extract ONLY: {json.dumps(remaining)}\n\n"
        "Return JSON only. Use empty string for missing fields.\n\n"
        f"Context:\n{context}"
    )


def extract_fields(context: str, regex_data: dict | None = None) -> dict:
    if regex_data is None:
        regex_data = {}

    prompt = build_prompt(context, regex_data)
    model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid JSON returned by Mistral.",
            "raw_response": content,
        }

    final_data = regex_data.copy()

    for field in COMPLEX_FIELDS:
        if not final_data.get(field):
            final_data[field] = data.get(field, "")

    return final_data

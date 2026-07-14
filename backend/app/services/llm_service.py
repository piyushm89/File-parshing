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

    regex_preview = {
        k: v
        for k, v in regex_data.items()
        if k in COMPLEX_FIELDS and v
    }

    return (
        "Extract Indian Government Tender fields from the context below.\n\n"
        f"Regex already extracted: {json.dumps(regex_preview)}\n\n"
        f"Extract ONLY: {json.dumps(remaining)}\n\n"
        "Return ONLY valid JSON.\n"
        "Do not write explanations.\n"
        "Do not wrap JSON inside markdown.\n"
        "Use empty string for missing fields.\n\n"
        f"Context:\n{context}"
    )


def extract_fields(context: str, regex_data: dict | None =None) -> dict:

    if regex_data is None:
        regex_data = {}

    prompt = build_prompt(context, regex_data)

    model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    print("\n" + "=" * 80)
    print("USING MODEL :", model)
    print("=" * 80)

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

    print("\n" + "=" * 80)
    print("RAW MISTRAL RESPONSE")
    print("=" * 80)
    print(repr(content))
    print("=" * 80)

    if not isinstance(content, str):
        print("WARNING : Content is not a string")
        print(type(content))

        try:
            content = str(content)
        except Exception:
            return {
                "status": "error",
                "message": "Unexpected response type from Mistral.",
                "raw_response": repr(content),
            }

    try:
        data = json.loads(content)

    except json.JSONDecodeError as e:

        print("\nJSON PARSE ERROR")
        print(e)

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
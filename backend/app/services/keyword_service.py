import re

KEYWORDS = {
    "mandatory_documents": [
        "mandatory document",
        "documents required",
        "supporting documents",
        "required documents",
        "document required",
        "scan copy",
        "certificate",
        "technical bid",
        "pq bid",
        "emd fee form",
        "tender fee form",
        "list of documents",
        "documents to be submitted",
    ],

    "evaluation_method": [
        "evaluation",
        "evaluation criteria",
        "technical evaluation",
        "financial evaluation",
        "commercial evaluation",
        "qcbs",
        "l1",
        "least cost",
        "quality and cost",
        "selection criteria",
        "scoring",
        "marks",
        "weightage",
    ],

    "eligibility": [
        "eligibility",
        "eligible",
        "qualification",
        "pre qualification",
        "pre-qualification",
        "minimum criteria",
        "experience",
        "annual turnover",
        "turnover",
        "bidder must",
    ],

    "disqualification_clauses": [
        "disqualification",
        "blacklisted",
        "rejected",
        "liable to rejection",
        "debarred",
    ],

    "submission_mode": [
        "online submission",
        "offline submission",
        "mode of submission",
        "submission mode",
        "physical submission",
    ],

    "technical_bid": [
        "technical bid",
        "technical proposal",
        "technical specification",
    ],

    "commercial_bid": [
        "commercial bid",
        "price bid",
        "financial bid",
        "commercial proposal",
    ],

    "scope_of_work": [
        "scope of work",
        "work description",
        "description of work",
        "project description",
    ],

    "price_bid": [
        "price bid",
        "boq",
        "bill of quantities",
        "price schedule",
    ],

    "tender_description": [
        "name of work",
        "tender title",
        "description of work",
        "project description",
    ],
}


WINDOW = 2


def split_into_paragraphs(text: str):
    paragraphs = []
    current = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            if current:
                paragraphs.append("\n".join(current))
                current = []
            continue

        current.append(line)

    if current:
        paragraphs.append("\n".join(current))

    return paragraphs


def extract_relevant_sections(text: str):

    paragraphs = split_into_paragraphs(text)

    collected = {}

    print("")
    print("Keyword Extraction")
    print("-" * 40)

    for field, keywords in KEYWORDS.items():

        snippets = []

        for i, para in enumerate(paragraphs):

            lower_para = para.lower()

            if any(keyword in lower_para for keyword in keywords):

                start = max(0, i - WINDOW)
                end = min(len(paragraphs), i + WINDOW + 1)

                snippets.append("\n\n".join(paragraphs[start:end]))

        unique = list(dict.fromkeys(snippets))

        collected[field] = "\n\n".join(unique[:3])

        print(f"{field} : {len(unique)} section(s)")

    print("-" * 40)

    relevant_context = "\n\n".join(
        value for value in collected.values() if value.strip()
    )

    print(f"Relevant Context Size : {len(relevant_context):,} characters")
    print("-" * 40)

    return collected, relevant_context
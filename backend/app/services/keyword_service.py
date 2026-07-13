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
        "pre-qualification",
        "prequalification",
        "minimum criteria",
        "bidder must",
        "should have",
        "experience",
        "turnover",
        "annual turnover",
    ],

    "disqualification_clauses": [
        "disqualification",
        "rejected",
        "liable to rejection",
        "bid shall be rejected",
        "ineligible",
        "blacklisted",
        "termination",
        "debarred",
        "shall be summarily rejected",
    ],

    "submission_mode": [
        "submission mode",
        "online submission",
        "offline submission",
        "electronic format",
        "physical submission",
        "rpad",
        "speed post",
        "registered post",
        "hand delivery",
        "mode of submission",
    ],

    "technical_bid": [
        "technical bid",
        "technical proposal",
        "technical specifications",
        "scope of supply",
        "specification",
        "technical requirement",
    ],

    "commercial_bid": [
        "commercial bid",
        "commercial proposal",
        "price bid",
        "pricing",
        "price schedule",
        "commercial terms",
        "payment terms",
    ],

    "scope_of_work": [
        "scope of work",
        "work description",
        "description of work",
        "project description",
        "scope of supply",
        "nature of work",
    ],

    "price_bid": [
        "price bid",
        "price schedule",
        "boq",
        "bill of quantities",
        "rate contract",
        "unit rate",
        "quoted price",
    ],

    "tender_description": [
        "description of material",
        "name of work",
        "scope of work",
        "work description",
        "project description",
        "brief description",
        "description of tender",
        "tender details",
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
    print(" Keyword Extraction")
    print("-" * 40)

    for field, keywords in KEYWORDS.items():
        snippets = []

        for i, para in enumerate(paragraphs):
            lower_para = para.lower()

            if any(keyword in lower_para for keyword in keywords):
                start = max(0, i - WINDOW)
                end = min(len(paragraphs), i + WINDOW + 1)

                snippet = "\n\n".join(paragraphs[start:end])
                snippets.append(snippet)

        unique = []
        seen = set()

        for s in snippets:
            if s not in seen:
                seen.add(s)
                unique.append(s)

        collected[field] = "\n\n".join(unique[:3])
        print(f" {field} : {len(unique)} section(s)")

    print("-" * 40)

    final_text = []

    for value in collected.values():
        if value.strip():
            final_text.append(value)

    relevant_context = "\n\n".join(final_text)

    print(f" Relevant Context Size : {len(relevant_context):,} characters")
    print("-" * 40)

    return collected, relevant_context

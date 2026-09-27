import pymupdf
from pathlib import Path
from typing import List

from src.models import PolicyPage


def extract_policy_text(
    pdf_path: str,
    policy_id: str,
    policy_name: str
) -> List[PolicyPage]:
    """
    Extract text from every page of a policy PDF.

    Each page retains:
    - policy ID
    - policy name
    - page number
    - extracted text
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(
            f"Policy PDF not found: {pdf_file}"
        )

    document = pymupdf.open(pdf_file)

    pages = []

    for page_index, page in enumerate(document):

        text = page.get_text("text").strip()

        policy_page = PolicyPage(
            policy_id=policy_id,
            policy_name=policy_name,
            page_number=page_index + 1,
            text=text
        )

        pages.append(policy_page)

    document.close()

    return pages
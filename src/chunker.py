import re
from typing import List

from src.models import PolicyPage, PolicyChunk


def chunk_policy_pages(
    pages: List[PolicyPage],
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[PolicyChunk]:

    chunks = []

    for page in pages:

        text = page.text.strip()

        if not text:
            continue

        # Clean excessive whitespace
        text = re.sub(r"\s+", " ", text)

        # Split into sentences
        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        current_chunk = ""
        chunk_index = 0

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            # If adding sentence exceeds chunk size,
            # save the current chunk
            if (
                len(current_chunk) + len(sentence) + 1
                > chunk_size
                and current_chunk
            ):

                chunks.append(
                    PolicyChunk(
                        chunk_id=(
                            f"{page.policy_id}_"
                            f"P{page.page_number}_"
                            f"C{chunk_index}"
                        ),
                        policy_id=page.policy_id,
                        policy_name=page.policy_name,
                        page_number=page.page_number,
                        chunk_index=chunk_index,
                        text=current_chunk.strip()
                    )
                )

                chunk_index += 1

                # Keep overlap from previous chunk
                overlap_text = current_chunk[-overlap:]

                current_chunk = (
                    overlap_text + " " + sentence
                )

            else:

                current_chunk += " " + sentence

        # Add final chunk
        if current_chunk.strip():

            chunks.append(
                PolicyChunk(
                    chunk_id=(
                        f"{page.policy_id}_"
                        f"P{page.page_number}_"
                        f"C{chunk_index}"
                    ),
                    policy_id=page.policy_id,
                    policy_name=page.policy_name,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                    text=current_chunk.strip()
                )
            )

    return chunks
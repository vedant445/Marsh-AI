import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.retriever import PolicyRetriever


retriever = PolicyRetriever()


queries = [
    "How many times can the health insurance cover be refilled?",
    "How does Super Credit increase the Sum Insured?",
    "What benefits are covered under Claim Protect?",
    "How can customers earn HealthReturns?",
    "What happens when the Sum Insured is exhausted?"
]


for query in queries:

    print("\n" + "=" * 100)
    print("QUERY")
    print("=" * 100)

    print(query)

    results = retriever.search(
        query,
        n_results=3
    )

    print("\n" + "-" * 100)
    print("RETRIEVED EVIDENCE")
    print("-" * 100)

    for index, result in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {index}")

        print(
            f"Policy: {result['policy_name']}"
        )

        print(
            f"Page: {result['page_number']}"
        )

        print(
            f"Chunk: {result['chunk_index']}"
        )

        print(
            f"Similarity: {result['similarity']}"
        )

        print(
            f"Rerank Score: {result['rerank_score']}"
        )

        print("\nEvidence:")

        print(
            result["evidence"]
        )

    print("\n")
from src.policy_config import POLICIES
from src.pdf_processor import extract_policy_text
from src.chunker import chunk_policy_pages
from src.embeddings import EmbeddingModel
from src.vector_store import PolicyVectorStore


# --------------------------------------------------
# 1. Load all policy PDFs
# --------------------------------------------------

all_chunks = []

for policy in POLICIES:

    print("\n" + "=" * 80)
    print(f"PROCESSING: {policy['policy_name']}")
    print("=" * 80)

    pages = extract_policy_text(
        pdf_path=policy["pdf_path"],
        policy_id=policy["policy_id"],
        policy_name=policy["policy_name"]
    )

    print(f"Pages extracted: {len(pages)}")

    chunks = chunk_policy_pages(
        pages,
        chunk_size=1000,
        overlap=200
    )

    print(f"Chunks created: {len(chunks)}")

    all_chunks.extend(chunks)


# --------------------------------------------------
# 2. Load embedding model
# --------------------------------------------------

print("\n" + "=" * 80)
print("LOADING EMBEDDING MODEL")
print("=" * 80)

embedding_model = EmbeddingModel()


# --------------------------------------------------
# 3. Generate embeddings
# --------------------------------------------------

texts = [
    chunk.text
    for chunk in all_chunks
]

embeddings = embedding_model.encode(texts)

print(f"\nTotal chunks: {len(all_chunks)}")
print(f"Embedding dimensions: {len(embeddings[0])}")


# --------------------------------------------------
# 4. Store everything in ChromaDB
# --------------------------------------------------

vector_store = PolicyVectorStore()

vector_store.add_chunks(
    all_chunks,
    embeddings
)

print("\nAll policy chunks stored successfully.")


# --------------------------------------------------
# 5. Test retrieval
# --------------------------------------------------

query = "How does the insurance policy refill coverage?"

query_embedding = embedding_model.encode(
    [query]
)[0]

results = vector_store.search(
    query_embedding,
    n_results=5
)


# --------------------------------------------------
# 6. Display results
# --------------------------------------------------

print("\n" + "=" * 80)
print("SEARCH QUERY")
print("=" * 80)

print(query)


print("\n" + "=" * 80)
print("RETRIEVED EVIDENCE")
print("=" * 80)


for i in range(len(results["documents"][0])):

    print("\n" + "-" * 80)

    metadata = results["metadatas"][0][i]

    print(
        f"Policy: {metadata['policy_name']}"
    )

    print(
        f"Page: {metadata['page_number']}"
    )

    print(
        f"Chunk: {metadata['chunk_index']}"
    )

    print("\nEvidence:")

    print(
        results["documents"][0][i]
    )
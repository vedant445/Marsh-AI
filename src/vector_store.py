import chromadb


class PolicyVectorStore:

    def __init__(
        self,
        collection_name: str = "marsh_policies"
    ):

        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine"
            }
        )

        # ======================================================
        # DEBUG
        # ======================================================

        print("=" * 60)
        print("Chroma Database Loaded")
        print(f"Collection Name : {self.collection.name}")
        print(f"Total Chunks    : {self.collection.count()}")
        print("=" * 60)

    def add_chunks(
        self,
        chunks,
        embeddings
    ):

        documents = [
            chunk.text
            for chunk in chunks
        ]

        ids = [
            chunk.chunk_id
            for chunk in chunks
        ]

        metadatas = [
            {
                "policy_id": chunk.policy_id,
                "policy_name": chunk.policy_name,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(f"Added {len(chunks)} chunks to ChromaDB.")

    def search(
        self,
        query_embedding,
        n_results: int = 5
    ):

        print("\nSearching ChromaDB...")
        print(f"Current Collection Count: {self.collection.count()}")

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        print(f"Retrieved {len(results['documents'][0])} documents.")

        return results
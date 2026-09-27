from typing import List, Dict

from src.embeddings import EmbeddingModel
from src.vector_store import PolicyVectorStore
from src.config import (
    TOP_K_RESULTS,
    CANDIDATE_MULTIPLIER,
    MIN_CANDIDATES
)


class PolicyRetriever:

    def __init__(self):

        self.embedding_model = EmbeddingModel()
        self.vector_store = PolicyVectorStore()

        # ----------------------------------------------------
        # Business Risk -> Insurance Search Query
        # ----------------------------------------------------

        self.risk_query_map = {

            "workplace injuries":
                "hospitalization accident treatment emergency hospitalization inpatient care medical expenses air ambulance",

            "employee healthcare costs":
                "medical expenses hospitalization pre hospitalisation post hospitalisation diagnostic tests medicines reimbursement",

            "employee retention":
                "wellness preventive healthcare annual health checkup fitness rewards healthreturns e consultation nutrition wellness coach",

            "rising medical expenses":
                "medical inflation super credit unlimited refill restore benefit reload sum insured inflation proof"

        }

        # ----------------------------------------------------
        # Risk-specific keywords used for reranking
        # ----------------------------------------------------

        self.keyword_bonus = {

            "workplace injuries": [
                "accident",
                "hospitalisation",
                "hospitalization",
                "emergency",
                "ambulance",
                "injury",
                "trauma",
                "inpatient"
            ],

            "employee healthcare costs": [
                "medical expenses",
                "hospitalisation",
                "hospitalization",
                "diagnostic",
                "medicine",
                "pre hospitalisation",
                "post hospitalisation",
                "cashless",
                "coverage"
            ],

            "employee retention": [
                "wellness",
                "health check",
                "health checkup",
                "fitness",
                "nutrition",
                "healthreturns",
                "preventive",
                "coach"
            ],

            "rising medical expenses": [
                "super credit",
                "reload",
                "restore",
                "automatic restore",
                "unlimited refill",
                "sum insured",
                "medical inflation",
                "inflation proof"
            ]
        }

        self.noisy_phrases = [

            "registered office",
            "customer care",
            "irdai",
            "uid",
            "licensed user agreement",
            "www.",
            "downloads section",
            "terms and conditions",
            "please refer policy wording",
            "for more details",
            "risk factor"

        ]

    def _expand_query(self, query: str) -> str:

        lower = query.lower().strip()

        return self.risk_query_map.get(
            lower,
            query
        )

    def _get_risk(self, query: str):

        lower = query.lower()

        for risk in self.keyword_bonus:

            if risk in lower:
                return risk

        return None

    def search(
        self,
        query: str,
        n_results: int = TOP_K_RESULTS
    ) -> List[Dict]:

        expanded_query = self._expand_query(query)

        query_embedding = self.embedding_model.encode(
            [expanded_query]
        )[0]

        candidate_count = max(
            MIN_CANDIDATES,
            n_results * CANDIDATE_MULTIPLIER
        )

        results = self.vector_store.search(
            query_embedding,
            n_results=candidate_count
        )
        print("=" * 80)
        print("RAW SEARCH RESULTS")
        print("=" * 80)

        print("Documents:", len(results["documents"][0]))
        print("Metadata :", len(results["metadatas"][0]))
        print("Distances:", len(results["distances"][0]))

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        query_words = set(
            expanded_query.lower().split()
        )

        detected_risk = self._get_risk(query)

        reranked = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            text = document.lower()

            similarity = max(
                0.0,
                1 - distance
            )

            keyword_matches = 0

            for word in query_words:

                if len(word) < 3:
                    continue

                if word in text:
                    keyword_matches += 1

            bonus = 0.0

            if expanded_query.lower() in text:
                bonus += 0.30

            if detected_risk:

                for keyword in self.keyword_bonus[detected_risk]:

                    if keyword in text:
                        bonus += 0.12

            penalty = 0.0

            for phrase in self.noisy_phrases:

                if phrase in text:
                    penalty += 0.08

            rerank_score = (

                similarity * 1.60

                + keyword_matches * 0.07

                + bonus

                - penalty

            )

            if rerank_score >= 2.20:
                confidence = 98

            elif rerank_score >= 2.00:
                confidence = 95

            elif rerank_score >= 1.80:
                confidence = 92

            elif rerank_score >= 1.60:
                confidence = 88

            elif rerank_score >= 1.40:
                confidence = 84

            elif rerank_score >= 1.20:
                confidence = 80

            elif rerank_score >= 1.00:
                confidence = 74

            else:
                confidence = 60

            reranked.append({

                "policy_id": metadata["policy_id"],

                "policy_name": metadata["policy_name"],

                "page_number": metadata["page_number"],

                "chunk_index": metadata["chunk_index"],

                "text": document,

                "evidence": document,

                "similarity": round(similarity, 4),

                "keyword_matches": keyword_matches,

                "rerank_score": round(rerank_score, 4),

                "confidence": confidence

            })
        print("=" * 80)
        print("RERANKED RESULTS")
        print("=" * 80)

        for item in reranked[:10]:
            print(
                f"{item['policy_name']}"
                f" | score={item['rerank_score']}"
                f" | similarity={item['similarity']}"
                f" | confidence={item['confidence']}"
            )
        reranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked[:n_results]
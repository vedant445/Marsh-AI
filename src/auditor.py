from typing import Dict, List


class PitchAuditor:

    def __init__(self):
        pass

    def _keyword_overlap(self, claim: str, evidence: str) -> float:

        stop_words = {
            "our", "the", "can", "help", "because",
            "provides", "provide", "policy",
            "insurance", "solutions", "recommend",
            "relevant", "to", "it", "this",
            "a", "an", "for", "of", "and",
            "with", "be", "is"
        }

        claim_words = {
            word.lower().strip(".,")
            for word in claim.split()
            if word.lower() not in stop_words
        }

        evidence_words = {
            word.lower().strip(".,")
            for word in evidence.split()
        }

        if not claim_words:
            return 0

        matches = claim_words.intersection(evidence_words)

        return len(matches) / len(claim_words)

    def audit_claim(
        self,
        slide_number: int,
        title: str,
        claim: str,
        evidence: List[Dict]
    ) -> Dict:

        if len(evidence) == 0:

            return {
                "slide_number": slide_number,
                "title": title,
                "claim": claim,
                "status": "FAIL",
                "confidence": 0,
                "reason": "No supporting policy evidence found.",
                "policy_name": None,
                "page_number": None,
                "chunk_index": None,
                "evidence": ""
            }

        best = evidence[0]

        similarity = best.get("similarity", 0.50)
        rerank = best.get("rerank_score", similarity)

        overlap = self._keyword_overlap(
            claim,
            best["text"]
        )

        confidence = round(
            min(
                100,
                rerank * 50 + overlap * 50
            )
        )

        if confidence >= 80:

            status = "PASS"

            reason = (
                "Claim is well supported by the retrieved policy clause."
            )

        elif confidence >= 60:

            status = "REVIEW"

            reason = (
                "Claim is partially supported. Human review recommended."
            )

        else:

            status = "FAIL"

            reason = (
                "Evidence is weak or does not directly support the claim."
            )

        return {

            "slide_number": slide_number,

            "title": title,

            "claim": claim,

            "status": status,

            "confidence": confidence,

            "reason": reason,

            "policy_name": best["policy_name"],

            "page_number": best["page_number"],

            "chunk_index": best["chunk_index"],

            "evidence": best["text"]

        }

    def audit_pitch_content(
        self,
        pitch: Dict
    ) -> Dict:

        audit_results = []

        supported = 0
        review = 0
        unsupported = 0

        for slide in pitch["slides"]:

            result = self.audit_claim(
                slide_number=slide["slide_number"],
                title=slide["title"],
                claim=slide["recommendation"],
                evidence=slide["evidence"]
            )

            audit_results.append(result)

            if result["status"] == "PASS":
                supported += 1

            elif result["status"] == "REVIEW":
                review += 1

            else:
                unsupported += 1

        return {

    "company": pitch["company"],

    "total_claims": len(audit_results),

    "supported_claims": supported,

    "review_claims": review,

    "unsupported_claims": unsupported,

    "results": audit_results

}


def audit_pitch_content(
    pitch: Dict
) -> Dict:

    auditor = PitchAuditor()

    return auditor.audit_pitch_content(pitch)
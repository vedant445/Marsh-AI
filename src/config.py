"""
Application-wide configuration.

Keeping constants here avoids hardcoding values across the project.
"""


# ============================================================
# Embedding Model
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ============================================================
# Vector Database
# ============================================================

COLLECTION_NAME = "insurance_policies"

TOP_K_RESULTS = 5

CANDIDATE_MULTIPLIER = 3


# ============================================================
# Retrieval / Re-ranking
# ============================================================

MIN_CANDIDATES = 10


# ============================================================
# Audit Thresholds
# ============================================================

PASS_THRESHOLD = 85

REVIEW_THRESHOLD = 70

FAIL_THRESHOLD = 0


# ============================================================
# PowerPoint
# ============================================================

MAX_RECOMMENDATION_LENGTH = 220

MAX_POLICY_CLAUSE_LENGTH = 180

MAX_EVIDENCE_LENGTH = 180

TEXT_WRAP_WIDTH = 55


# ============================================================
# Output
# ============================================================

OUTPUT_FOLDER = "output"

PITCH_FILENAME = "Marketing_Pitch.pptx"

AUDIT_FILENAME = "Audit_Report.pdf"
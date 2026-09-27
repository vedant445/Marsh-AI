import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.company_profile import generate_company_profile
from src.pitch_generator import generate_pitch
from src.auditor import audit_pitch


# ============================================================
# 1. COMPANY PROFILE
# ============================================================

profile = generate_company_profile(
    company_name="ABC Manufacturing Pvt Ltd",
    industry="Manufacturing",
    company_size="500 employees",
    key_risks=[
        "Workplace injuries",
        "Employee healthcare costs",
        "Employee retention",
        "Rising medical expenses"
    ]
)


# ============================================================
# 2. GENERATE PITCH
# ============================================================

pitch = generate_pitch(profile)


# ============================================================
# 3. AUDIT PITCH
# ============================================================

audited_pitch = audit_pitch(pitch)


# ============================================================
# 4. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 100)
print("MARSH AI PITCH ASSISTANT")
print("=" * 100)

print(f"\nCompany : {profile.company_name}")
print(f"Industry: {profile.industry}")
print(f"Size    : {profile.company_size}")


for slide in audited_pitch:

    print("\n" + "-" * 100)

    print(
        f"Slide {slide['slide_number']}: "
        f"{slide['title']}"
    )

    print("\nRecommendation:")
    print(slide["recommendation"])

    audit = slide["audit"]

    print("\nAudit Status:")
    print(audit["status"])

    print("\nAudit Reason:")
    print(audit["reason"])

    print("\nEvidence:")

    for evidence in audit["evidence"]:

        print(
            f"\n{evidence['policy_name']} | "
            f"Page {evidence['page_number']} | "
            f"Chunk {evidence['chunk_index']}"
        )

        print(evidence["evidence"])
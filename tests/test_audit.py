import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.company_profile import generate_company_profile
from src.pitch_generator import generate_pitch
from src.auditor import audit_pitch_content


def main():

    print("=" * 80)
    print("GENERATING COMPANY PROFILE")
    print("=" * 80)

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

    print("✓ Company profile generated")

    print("\nGenerating marketing pitch...")

    pitch = generate_pitch(profile)

    print("✓ Pitch generated")

    print("\nAuditing pitch...")

    report = audit_pitch_content(pitch)

    print("✓ Audit complete")

    print("\n" + "=" * 80)
    print("AUDIT REPORT")
    print("=" * 80)

    print(f"Company            : {report['company']}")
    print(f"Industry           : {report['industry']}")
    print(f"Overall Confidence : {report['overall_confidence']}%")
    print(f"Overall Status     : {report['overall_status']}")
    print(f"Total Claims       : {report['total_claims']}")
    print(f"Supported Claims   : {report['supported_claims']}")
    print(f"Review Claims      : {report['review_claims']}")
    print(f"Unsupported Claims : {report['unsupported_claims']}")

    for item in report["results"]:

        print("\n" + "-" * 80)

        print(f"Slide       : {item['slide_number']}")
        print(f"Title       : {item['title']}")
        print(f"Policy      : {item['policy_name']}")
        print(f"Page        : {item['page_number']}")
        print(f"Chunk       : {item['chunk_index']}")
        print(f"Confidence  : {item['confidence']}%")
        print(f"Status      : {item['status']}")
        print(f"Reason      : {item['reason']}")

        print("\nClaim:")
        print(item["claim"])

        print("\nEvidence:")
        print(item["evidence"][:350] + "...")


if __name__ == "__main__":
    main()
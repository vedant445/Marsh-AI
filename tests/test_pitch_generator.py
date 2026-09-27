import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.company_profile import generate_company_profile
from src.pitch_generator import PitchGenerator


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


generator = PitchGenerator()

pitch = generator.generate_pitch(profile)


print("\n" + "=" * 100)
print("GENERATED PITCH")
print("=" * 100)

print(f"\nCompany : {pitch['company']}")
print(f"Industry: {pitch['industry']}")

for i, slide in enumerate(pitch["slides"], start=1):

    print("\n" + "-" * 100)
    print(f"Slide {i}")
    print("-" * 100)

    print("Title:")
    print(slide["title"])

    print("\nRecommendation:")
    print(slide["recommendation"])

    print("\nEvidence:")

    for ev in slide["evidence"]:

        print(
            f"\n{ev['policy_name']} | "
            f"Page {ev['page_number']} | "
            f"Chunk {ev['chunk_index']}"
        )

        print(ev["evidence"][:250] + "...")
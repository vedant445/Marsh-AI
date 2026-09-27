import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.company_profile import generate_company_profile


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


print("\n" + "=" * 80)
print("COMPANY PROFILE")
print("=" * 80)

print(f"\nCompany: {profile.company_name}")
print(f"Industry: {profile.industry}")
print(f"Company Size: {profile.company_size}")

print("\nKey Risks:")

for risk in profile.key_risks:
    print(f"- {risk}")

print("\nFacts:")

for fact in profile.facts:
    print(f"- {fact}")

print("\nAssumptions:")

for assumption in profile.assumptions:
    print(f"- {assumption}")
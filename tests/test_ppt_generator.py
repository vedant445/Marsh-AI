from src.company_profile import generate_company_profile
from src.pitch_generator import generate_pitch
from src.ppt_generator import create_pitch_deck


def main():

    print("1. Starting")

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

    print("2. Profile created")

    pitch = generate_pitch(profile)

    print("3. Pitch generated")

    output = create_pitch_deck(
        pitch,
        output_path="output/ABC_Manufacturing_Pitch.pptx"
    )

    print("4. PPT generated")

    print(output)


if __name__ == "__main__":
    main()
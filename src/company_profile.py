from src.models import CompanyProfile


def generate_company_profile(company_name: str) -> CompanyProfile:

    company = company_name.lower()

    if "hdfc" in company:
        industry = "Banking & Financial Services"

    elif "tata" in company:
        industry = "Conglomerate"

    elif "infosys" in company:
        industry = "Information Technology"

    elif "wipro" in company:
        industry = "Information Technology"

    elif "maruti" in company:
        industry = "Automobile Manufacturing"

    else:
        industry = "Manufacturing"

    company_size = "500–1000 employees"

    key_risks = [
        "Workplace injuries",
        "Employee healthcare costs",
        "Employee retention",
        "Rising medical expenses"
    ]

    return CompanyProfile(
        company_name=company_name,
        industry=industry,
        company_size=company_size,
        key_risks=key_risks,
        facts=[
            f"{company_name} operates in the {industry} industry.",
            f"Estimated workforce: {company_size}."
        ],
        assumptions=[
            "Industry inferred from company name.",
            "Company size estimated."
        ]
    )
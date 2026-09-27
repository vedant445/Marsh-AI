from typing import Dict

from src.retriever import PolicyRetriever
from src.models import CompanyProfile
from src.evidence_cleaner import EvidenceCleaner

from src.company_profile import generate_company_profile
from src.auditor import audit_pitch_content


# ------------------------------------------------------------
# Business Risk -> Insurance Search Query
# ------------------------------------------------------------

RISK_QUERY_MAP = {

    "Workplace injuries":
        "hospitalization accident emergency ambulance accidental injury inpatient treatment",

    "Employee healthcare costs":
        "medical expenses hospitalization pre hospitalization post hospitalization reimbursement",

    "Employee retention":
        "wellness annual health checkup preventive care rewards fitness nutrition wellness coach",

    "Rising medical expenses":
        "medical inflation super credit unlimited refill restore sum insured"

}


# ------------------------------------------------------------
# Better recommendation templates
# ------------------------------------------------------------

RECOMMENDATION_MAP = {

    "Workplace injuries":
        "Recommend {policy} because it provides accident-related hospitalization coverage, emergency ambulance services, inpatient treatment, and medical expense protection for employees.",

    "Employee healthcare costs":
        "Recommend {policy} because it covers hospitalization expenses, diagnostic tests, pre and post hospitalization treatment, and reimbursable medical costs.",

    "Employee retention":
        "Recommend {policy} because it includes wellness benefits, annual health checkups, preventive healthcare, fitness coaching, and nutrition support that improve employee wellbeing and support employee retention initiatives.",

    "Rising medical expenses":
        "Recommend {policy} because it protects against rising healthcare costs through inflation protection, increasing Sum Insured, and unlimited refill or restore benefits."

}


class PitchGenerator:

    def __init__(self):

        self.retriever = PolicyRetriever()
        self.cleaner = EvidenceCleaner()

    def generate_pitch(
        self,
        profile: CompanyProfile
    ) -> Dict:

        slides = []

        for index, risk in enumerate(
            profile.key_risks,
            start=1
        ):

            query = RISK_QUERY_MAP.get(
                risk,
                risk
            )

            # Let the retriever decide the best evidence
            evidence = self.retriever.search(
                query,
                n_results=2
            )

            if evidence:

                best = evidence[0]

                policy_name = best["policy_name"]

                policy_clause = self.cleaner.clean(
                    best["text"]
                )

                if len(policy_clause) > 450:
                    policy_clause = policy_clause[:450] + "..."

                recommendation = RECOMMENDATION_MAP.get(
                    risk,
                    "Recommend {policy}."
                ).format(
                    policy=policy_name
                )

                slides.append({

                    "slide_number": index,

                    "title": risk,

                    "recommended_policy": policy_name,

                    "recommendation": recommendation,

                    "key_benefit": policy_clause,

                    "policy_clause": policy_clause,

                    "evidence": evidence

                })

            else:

                slides.append({

                    "slide_number": index,

                    "title": risk,

                    "recommended_policy": "No Recommendation",

                    "recommendation":
                        f"No suitable recommendation found for {risk.lower()}.",

                    "key_benefit":
                        "No supporting evidence found.",

                    "policy_clause":
                        "",

                    "evidence": []

                })

        return {

            "company": profile.company_name,

            "industry": profile.industry,

            "slides": slides

        }


def generate_pitch(
    profile: CompanyProfile
) -> Dict:

    generator = PitchGenerator()

    return generator.generate_pitch(profile)

# ============================================================
# Complete Pipeline for Streamlit UI
# ============================================================

def generate_marketing_pitch(company_name: str):

    # Generate company profile
    profile = generate_company_profile(company_name)

    # Generate pitch
    pitch = generate_pitch(profile)

    # Audit the generated pitch
    audit = audit_pitch_content(pitch)

    return pitch, audit
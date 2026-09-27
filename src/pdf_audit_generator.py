from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue
import re


# ---------------------------------------------------------
# Clean text before writing to PDF
# ---------------------------------------------------------

def clean_text(text):
    if text is None:
        return ""

    replacements = {
        "\ufb01": "fi",      # ﬁ
        "\ufb02": "fl",      # ﬂ
        "\u2018": "'",       # left single quote
        "\u2019": "'",       # right single quote
        "\u201c": '"',       # left double quote
        "\u201d": '"',       # right double quote
        "\u2013": "-",       # en dash
        "\u2014": "-",       # em dash
        "\u2022": "-",       # bullet
        "\xa0": " ",         # non-breaking space
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove unsupported characters
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    return text


# ---------------------------------------------------------
# PDF Generator
# ---------------------------------------------------------

def create_audit_pdf(audit_report, output_path):

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = darkblue

    heading = styles["Heading2"]
    body = styles["BodyText"]

    doc = SimpleDocTemplate(output_path)

    story = []

    # =====================================================
    # Title
    # =====================================================

    story.append(Paragraph("MARSH INSURANCE AI AUDIT REPORT", title_style))
    story.append(Spacer(1, 20))

    # =====================================================
    # Summary
    # =====================================================

    story.append(Paragraph("<b>Audit Summary</b>", heading))
    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"<b>Company:</b> {clean_text(audit_report['company'])}",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Claims:</b> {audit_report['total_claims']}",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Verified Claims:</b> {audit_report['supported_claims']}",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Needs Review:</b> {audit_report['review_claims']}",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Unsupported:</b> {audit_report['unsupported_claims']}",
            body,
        )
    )

    story.append(Spacer(1, 25))

    # =====================================================
    # Details
    # =====================================================

    story.append(Paragraph("<b>Claim Validation Details</b>", heading))
    story.append(Spacer(1, 12))

    for result in audit_report["results"]:

        story.append(
            Paragraph(
                f"<b>Slide {result['slide_number']} - {clean_text(result['title'])}</b>",
                heading,
            )
        )

        story.append(
            Paragraph(
                f"<b>Status:</b> {clean_text(result['status'])}",
                body,
            )
        )

        story.append(
            Paragraph(
                f"<b>Confidence:</b> {result['confidence']}%",
                body,
            )
        )

        story.append(
            Paragraph(
                f"<b>Recommendation:</b><br/>{clean_text(result['claim'])}",
                body,
            )
        )

        story.append(
            Paragraph(
                f"<b>Reason:</b><br/>{clean_text(result['reason'])}",
                body,
            )
        )

        story.append(
            Paragraph(
                f"<b>Supporting Policy:</b> {clean_text(result['policy_name'])}",
                body,
            )
        )

        story.append(
            Paragraph(
                f"<b>Page Number:</b> {result['page_number']}",
                body,
            )
        )

        story.append(
            Paragraph(
                f"<b>Evidence:</b><br/>{clean_text(result['evidence'])}",
                body,
            )
        )

        story.append(Spacer(1, 20))

    doc.build(story)
import os
import json
import streamlit as st
from src.pdf_audit_generator import create_audit_pdf

from src.company_profile import generate_company_profile
from src.pitch_generator import generate_pitch
from src.auditor import audit_pitch_content
from src.ppt_generator import create_pitch_deck

from src.config import (
    OUTPUT_FOLDER,
    PITCH_FILENAME,
    AUDIT_FILENAME
)

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Marsh AI Pitch Generator",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>

/* Main App */
.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
    max-width:1400px;
}

/* Background */
.stApp{
    background:#0F172A;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#172554;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label{
    color:white;
}

/* Title */
.title{
    font-size:42px;
    font-weight:700;
    color:white;
    margin-bottom:5px;
}

.subtitle{
    color:#CBD5E1;
    font-size:17px;
    margin-bottom:30px;
}

/* Headers */
h1,h2,h3{
    color:white;
}

/* Input Boxes */
.stTextInput input{
    border-radius:10px;
    border:1px solid #334155;
    background:#1E293B;
    color:white;
}

.stFileUploader{
    border-radius:10px;
}

/* Button */
.stButton>button{
    width:100%;
    background:#2563EB;
    color:white;
    border-radius:10px;
    font-weight:600;
    border:none;
    padding:12px;
    transition:0.3s;
}

.stButton>button:hover{
    background:#1D4ED8;
    transform:scale(1.02);
}

/* Download Buttons */
.stDownloadButton>button{
    width:100%;
    background:#16A34A;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px;
}

.stDownloadButton>button:hover{
    background:#15803D;
}

/* Expanders */
.streamlit-expanderHeader{
    font-size:18px;
    font-weight:600;
}

/* Metric Cards */
[data-testid="metric-container"]{
    background:#1E293B;
    border-radius:12px;
    padding:20px;
    border:1px solid #334155;
    box-shadow:0 2px 10px rgba(0,0,0,.25);
}

/* Tabs */
.stTabs [role="tablist"]{
    gap:15px;
}

.stTabs [role="tab"]{
    background:#1E293B;
    border-radius:8px;
    padding:12px 20px;
    color:white;
}

.stTabs [aria-selected="true"]{
    background:#2563EB;
    color:white;
}

/* Progress */
.stProgress>div>div>div{
    background:#2563EB;
}

/* Success */
.stSuccess{
    border-radius:10px;
}

/* Warning */
.stWarning{
    border-radius:10px;
}

/* Error */
.stError{
    border-radius:10px;
}

/* Info */
.stInfo{
    border-radius:10px;
}

/* Footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title("🛡 Marsh AI")

    st.markdown("---")

    st.subheader("Client Information")

    company_name = st.text_input(
        "Company Name",
        placeholder="Example: HDFC"
    )

    uploaded_files = st.file_uploader(
        "Upload Policy PDFs",
        type=["pdf"],
        accept_multiple_files=True,
    )

    generate = st.button(
        "🚀 Generate Marketing Pitch",
        use_container_width=True
    )

    st.markdown("---")

    st.write("### Features")

    st.write("✅ Company Profiling")
    st.write("✅ Policy Retrieval")
    st.write("✅ AI Recommendations")
    st.write("✅ PowerPoint Generation")
    st.write("✅ Audit Layer")

    st.markdown("---")

    st.info(
        "Generate an AI-powered insurance marketing pitch grounded in uploaded policy documents."
    )

# ============================================================
# Header
# ============================================================

st.markdown(
    "<div class='title'>Marsh Insurance AI Pitch Generator</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='subtitle'>"
    "Generate client-specific insurance recommendations, "
    "PowerPoint presentations and audit reports."
    "</div>",
    unsafe_allow_html=True,
)

# ============================================================
# Validation
# ============================================================

if generate:

    if company_name.strip() == "":
        st.error("Please enter a company name.")
        st.stop()

    if len(uploaded_files) == 0:
        st.error("Please upload at least one policy document.")
        st.stop()

    st.success("Inputs validated successfully.")

    progress = st.progress(0)

    status = st.empty()
    try:

        # =====================================================
        # Generate Company Profile
        # =====================================================

        status.info("Generating company profile...")
        progress.progress(15)

        profile = generate_company_profile(company_name)

        # =====================================================
        # Generate Marketing Pitch
        # =====================================================

        status.info("Generating AI marketing pitch...")
        progress.progress(45)

        pitch = generate_pitch(profile)

        # =====================================================
        # Create PowerPoint
        # =====================================================

        status.info("Creating PowerPoint presentation...")
        progress.progress(70)

        os.makedirs(
            OUTPUT_FOLDER,
            exist_ok=True
        )

        ppt_path = os.path.join(
            OUTPUT_FOLDER,
            PITCH_FILENAME
        )

        create_pitch_deck(
            pitch,
            ppt_path
        )

        # =====================================================
        # Audit
        # =====================================================

        status.info("Auditing AI-generated content...")
        progress.progress(90)

        audit_report = audit_pitch_content(pitch)

        audit_path = os.path.join(
            OUTPUT_FOLDER,
            "Audit_Report.pdf"
        )

        create_audit_pdf(
            audit_report,
            audit_path
        )

        st.session_state["profile"] = profile
        st.session_state["pitch"] = pitch
        st.session_state["audit_report"] = audit_report
        st.session_state["ppt_path"] = ppt_path
        st.session_state["audit_path"] = audit_path

        progress.progress(100)
        status.success("Generation Complete!")

    except Exception as e:

        st.error(f"Error: {str(e)}")

# =====================================================
# Results Tabs
# =====================================================

if "pitch" in st.session_state:

    profile = st.session_state["profile"]
    pitch = st.session_state["pitch"]
    audit_report = st.session_state["audit_report"]
    ppt_path = st.session_state["ppt_path"]
    audit_path = st.session_state["audit_path"]

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Company Profile",
        "📑 Recommended Policies",
        "📥 Downloads",
        "🛡 Audit"
    ])

    # =====================================================
    # Company Profile
    # =====================================================

    with tab1:

        st.markdown("""
        <h1 style="
            font-size:42px;
            font-weight:700;
            margin-bottom:35px;
            color:white;">
            🏢 Company Profile
        </h1>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 2])

        with col1:

            st.markdown("""
            <div style="
                color:#94A3B8;
                font-size:18px;
                font-weight:600;
                margin-bottom:8px;">
                Industry
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"""
                <div style="
                    color:white;
                    font-size:30px;
                    font-weight:700;
                    line-height:1.3;
                    margin-bottom:35px;">
                    {profile.industry}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("""
            <div style="
                color:#94A3B8;
                font-size:18px;
                font-weight:600;
                margin-bottom:8px;">
                Company Size
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"""
                <div style="
                    color:white;
                    font-size:30px;
                    font-weight:700;">
                    {profile.company_size}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown("""
            <div style="
                color:white;
                font-size:34px;
                font-weight:700;
                margin-bottom:20px;">
                Key Business Risks
            </div>
            """, unsafe_allow_html=True)

            for risk in profile.key_risks:
                st.markdown(
                    f"""
                    <div style="
                        color:#E2E8F0;
                        font-size:20px;
                        margin-bottom:16px;">
                        • {risk}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # =====================================================
    # Recommended Policies
    # =====================================================

    with tab2:

        st.header("Recommended Policies")

        for slide in pitch["slides"]:

            with st.expander(slide["title"], expanded=False):

                st.markdown(
                    f"### 🛡 {slide['recommended_policy']}"
                )

                st.markdown(
                    f"**Recommendation**\n\n{slide['recommendation']}"
                )

                st.markdown(
                    f"**Key Benefit**\n\n{slide['key_benefit']}"
                )

                st.markdown("### Supporting Evidence")

                for evidence in slide["evidence"][:2]:

                    st.info(
                        f"**{evidence['policy_name']}**\n\n"
                        f"Page {evidence['page_number']}\n\n"
                        f"{evidence['text']}"
                    )

    with tab3:

        st.header("📥 Downloads")

        col1, col2 = st.columns(2)

        with col1:

            with open(ppt_path, "rb") as file:

                st.download_button(
                label="📥 Download PowerPoint",
                data=file,
                file_name=PITCH_FILENAME,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="ppt_download"
            )

        with col2:

            with open(audit_path, "rb") as file:

                st.download_button(
                label="📥 Download Audit Report",
                data=file,
                file_name=AUDIT_FILENAME,
                mime="application/pdf",
                key="audit_download"
            )

    # =====================================================
    # Audit
    # =====================================================

    with tab4:

        st.header("🛡 Audit Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Verified Claims",
            audit_report["supported_claims"]
        )

        col2.metric(
            "Needs Review",
            audit_report["review_claims"]
        )

        col3.metric(
            "Unsupported",
            audit_report["unsupported_claims"]
        )

        st.progress(
            audit_report["supported_claims"] /
            audit_report["total_claims"]
        )

        st.caption(
            "The audit validates every AI recommendation against the uploaded policy documents."
        )

        st.markdown("---")
        st.subheader("Claim Validation Details")

        for result in audit_report["results"]:

            if result["status"] == "PASS":
                icon = "✅"
                color = "green"

            elif result["status"] == "REVIEW":
                icon = "🟡"
                color = "orange"

            else:
                icon = "❌"
                color = "red"

            with st.expander(
                f"{icon} Slide {result['slide_number']} • {result['title']}",
                expanded=False
            ):

                st.markdown(
                    f"**Recommendation**\n\n"
                    f"{result['claim']}"
                )

                c1, c2 = st.columns(2)

                with c1:
                    st.markdown(
                        f"**Status:** :{color}[{result['status']}]"
                    )

                with c2:
                    st.markdown(
                        f"**Confidence:** {result['confidence']}%"
                    )

                st.markdown(
                    f"**Reason**\n\n"
                    f"{result['reason']}"
                )

                st.markdown(
                    f"**Supporting Policy:** {result['policy_name']}"
                )

                st.markdown(
                    f"**Page Number:** {result['page_number']}"
                )

                st.markdown("**Supporting Evidence**")

                st.info(result["evidence"])
# =====================================================
# Footer
# =====================================================

st.markdown("---")

st.caption(
    "Marsh Insurance AI Pitch Generator | "
    "Powered by Retrieval-Augmented Generation (RAG), "
    "Sentence Transformers, ChromaDB and Large Language Models"
)
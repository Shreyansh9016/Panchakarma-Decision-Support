import streamlit as st
import os
from rag_pipeline import load_db, generate_answer, answer_general_query

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Panchakarma Decision Support System",
    layout="wide"
)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Panchakarma Decision Support System")

st.sidebar.markdown("""
Evidence-based system for Panchakarma therapy recommendation  
using classical Ayurveda literature.

For academic and educational use only.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("Instructions")

st.sidebar.markdown("""
1. Enter patient details  
2. Provide a clear description of symptoms  
3. Submit the form  
4. Review the recommendation and supporting evidence  
""")

if st.sidebar.button("Load Example Case"):
    st.session_state.example = True

# -------------------------
# MAIN TITLE
# -------------------------
st.title("Evidence-Based Panchakarma Decision Support System")
st.caption("Retrieval-Augmented Generation using Classical Ayurveda Sources")

# =========================================================
# LOAD PRE-BUILT DATABASE (MANDATORY FOR HF)
# =========================================================
DB_PATH = "vector_db/classical_db"

if not os.path.exists(DB_PATH):
    st.error("❌ Vector DB not found. Please upload pre-built database.")
    st.stop()

# -------------------------
# LOAD DATABASE (CACHED)
# -------------------------
@st.cache_resource(show_spinner="Loading knowledge base...")
def get_db():
    return load_db(DB_PATH)

# Safe loading
try:
    db = get_db()
except Exception as e:
    st.error(f"❌ Failed to load database: {str(e)}")
    st.stop()

# -------------------------
# EXAMPLE DATA
# -------------------------
example_symptoms = """
Chronic constipation, bloating, dry skin, fatigue, anxiety.
Symptoms worsen in cold weather.
"""

symptoms_default = example_symptoms if "example" in st.session_state else ""

# -------------------------
# MODE SELECTION TABS
# -------------------------
tab1, tab2 = st.tabs(["📋 Patient Case Analysis", "💬 General Ayurveda Queries"])

# =========================================================
# TAB 1: PATIENT CASE
# =========================================================
with tab1:
    st.subheader("Patient Information")

    with st.form("patient_form"):

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", 1, 120)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        with col2:
            prakriti = st.selectbox("Prakriti", ["Vata", "Pitta", "Kapha"])
            history = st.text_area("Medical History")

        symptoms = st.text_area(
            "Symptoms",
            value=symptoms_default,
            height=150
        )

        submit = st.form_submit_button("Submit")

    if submit:
        if not symptoms.strip():
            st.warning("Please provide a description of symptoms.")
        else:
            query = f"""
Age: {age}
Gender: {gender}
Prakriti: {prakriti}
Symptoms: {symptoms}
History: {history}
"""
            with st.spinner("Processing request..."):
                answer, sources = generate_answer(query, db)

            st.success("Analysis completed.")

            # -------------------------
            # RECOMMENDATION
            # -------------------------
            st.subheader("Recommendation")
            st.markdown(answer)

            # -------------------------
            # SUPPORTING EVIDENCE
            # -------------------------
            st.subheader("Supporting Evidence")

            with st.expander("View Source Passages"):
                for i, doc in enumerate(sources):
                    st.markdown(
                        f"**Source {i+1}: {doc.metadata.get('source','Unknown')}**"
                    )
                    st.code(doc.page_content[:600], language="markdown")
                    st.markdown("---")

# =========================================================
# TAB 2: GENERAL Q&A
# =========================================================
with tab2:
    st.header("Post-Therapy Questions / General Ayurveda Queries")

    user_query = st.text_area(
        "Ask your question (e.g., 'Can I drink cold water after Vamana?')"
    )

    if st.button("Get Answer"):
        if user_query.strip():
            with st.spinner("Generating answer from classical texts..."):
                qa_answer, qa_sources = answer_general_query(user_query, db)

            st.markdown(qa_answer)
            st.caption("✨ Answer generated from classical Ayurvedic texts")

            if qa_sources:
                with st.expander("View Retrieved Passages (Transparency)"):
                    for i, doc in enumerate(qa_sources):
                        st.markdown(
                            f"**Source {i+1}: {doc.metadata.get('source', 'Unknown')}**"
                        )
                        st.code(doc.page_content[:500] + "...", language="markdown")
                        st.markdown("---")
        else:
            st.warning("Please enter a question")

# -------------------------
# DISCLAIMER
# -------------------------
st.markdown("---")

st.caption("""
This system generates recommendations based on textual sources.
It does not replace professional medical consultation.
""")
import streamlit as st
import os
from rag_pipeline import load_db, generate_answer, answer_general_query
from build_db import build_db


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
# BUILD DATABASE IF MISSING (REQUIRED FOR STREAMLIT CLOUD)
# =========================================================

DB_PATH = "vector_db/classical_db"

if not os.path.exists(DB_PATH):
    st.info("Initializing knowledge base. This may take a few minutes...")
    build_db("data/classical", DB_PATH)


# -------------------------
# LOAD DATABASE (CACHED)
# -------------------------
@st.cache_resource
def get_db():
    return load_db(DB_PATH)

db = get_db()


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

with tab1:
    # -------------------------
    # PATIENT INPUT FORM
    # -------------------------
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

    # -------------------------
    # PROCESS INPUT & VALIDATION
    # -------------------------
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
            st.write(answer)


            # -------------------------
            # SUPPORTING EVIDENCE
            # -------------------------
            st.subheader("Supporting Evidence")

            with st.expander("View Source Passages"):

                for i, doc in enumerate(sources):
                    st.markdown(
                        f"**Source {i+1}: {doc.metadata.get('source','Unknown')}**"
                    )
                    st.write(doc.page_content[:600])
                    st.markdown("---")

with tab2:
    # -------------------------
    # Q&A SECTION
    # -------------------------
    st.header("Post-Therapy Questions / General Ayurveda Queries")

    user_query = st.text_area("Ask your question (e.g., 'Can I drink cold water after Vamana?')")

    if st.button("Get Answer"):
        if user_query.strip():
            with st.spinner("Generating answer from classical texts..."):
                qa_answer, qa_sources = answer_general_query(user_query, db)
                
            st.write(qa_answer)
            st.caption("✨ Answer generated from classical Ayurvedic texts")
            
            if qa_sources:
                with st.expander("View Retrieved Passages (Transparency)"):
                    for i, doc in enumerate(qa_sources):
                        st.markdown(f"**Source {i+1}: {doc.metadata.get('source', 'Unknown')}**")
                        st.write(doc.page_content[:500] + "...")
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
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


# -------------------------
# CONFIG
# -------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"


# -------------------------
# CHECK API KEY
# -------------------------
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("❌ GROQ_API_KEY not found in .env file")


# -------------------------
# GET EMBEDDINGS
# -------------------------
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


# -------------------------
# LOAD VECTOR DATABASE
# -------------------------
def load_db(path):

    embeddings = get_embeddings()

    db = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


# -------------------------
# GENERATE ANSWER
# -------------------------
def generate_answer(query, db):

    retriever = db.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(query)

    # -------- Handle no results --------
    if not docs:
        return "No relevant information found in knowledge base.", []

    context = "\n\n".join(d.page_content for d in docs)

    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=0.2
    )

    prompt = f"""
You are an expert Ayurveda physician specializing in Panchakarma.

Use ONLY the provided context.
Do NOT use outside knowledge.
Do NOT invent treatments.

If the information is insufficient, say:
"Insufficient evidence from sources."

Context:
{context}

Patient Case:
{query}

Provide your answer in clear sections:

1. Recommended Panchakarma therapy
2. Clinical rationale
3. Contraindications
4. Supporting evidence from context
5. Confidence level (High / Medium / Low)
"""

    response = llm.invoke(prompt)
    return response.content, docs

# -------------------------
# ANSWER GENERAL QUERY
# -------------------------
def answer_general_query(query, db):
    # Step 1: Retrieve top-k relevant documents
    # Using k=5 for enhanced retrieval and anti-hallucination support
    docs = db.similarity_search(query, k=5)

    if not docs:
        return "I don't know based on the available Ayurvedic texts.", []

    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=0.1
    )

    # Step 2: STRICT grounded prompt
    prompt = f"""
You are an expert Ayurveda assistant specialized in Panchakarma.

Answer the user's question ONLY using the provided context.
Do NOT use external knowledge.
Do NOT guess or hallucinate.

If the answer is not present in the context, say:
"I don't know based on the available Ayurvedic texts."

Context:
{context}

Question:
{query}

Instructions:
- Give a clear, practical answer.
- If applicable, mention precautions.
- Keep it concise and medically responsible.
- Do NOT fabricate details.

Answer:
"""

    response = llm.invoke(prompt)

    return response.content, docs
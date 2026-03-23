from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os


# -------------------------
# CONFIG
# -------------------------
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def build_db(data_path, save_path):

    documents = []

    print(f"\n📂 Loading PDFs from: {data_path}")

    for file in os.listdir(data_path):

        if file.lower().endswith(".pdf"):

            file_path = os.path.join(data_path, file)

            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load()

                # Add source metadata
                for d in docs:
                    d.metadata["source"] = file

                documents.extend(docs)

                print(f"✅ Loaded: {file}")

            except Exception as e:
                print(f"❌ Error loading {file}: {e}")

    print(f"\n📄 Total pages loaded: {len(documents)}")

    # -------------------------
    # SPLIT DOCUMENTS
    # -------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    split_docs = splitter.split_documents(documents)

    print(f"✂️ Total chunks created: {len(split_docs)}")

    # -------------------------
    # EMBEDDINGS
    # -------------------------
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # -------------------------
    # CREATE FAISS DB
    # -------------------------
    db = FAISS.from_documents(split_docs, embeddings)

    os.makedirs(save_path, exist_ok=True)

    db.save_local(save_path)

    print(f"\n💾 Vector DB saved to: {save_path}")


# -------------------------
# RUN SCRIPT
# -------------------------
if __name__ == "__main__":

    build_db("data/classical", "vector_db/classical_db")
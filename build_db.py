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
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_db(data_path, save_path):

    # -------------------------
    # VALIDATE INPUT PATH
    # -------------------------
    if not os.path.exists(data_path):
        raise ValueError(f"❌ Data path does not exist: {data_path}")

    documents = []

    print(f"\n📂 Loading PDFs from: {data_path}")

    # -------------------------
    # LOAD PDF FILES
    # -------------------------
    pdf_files = [f for f in os.listdir(data_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        raise ValueError("❌ No PDF files found in the specified directory.")

    for file in pdf_files:

        file_path = os.path.join(data_path, file)

        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            if not docs:
                print(f"⚠️ Skipped empty PDF: {file}")
                continue

            # Add metadata
            for d in docs:
                d.metadata["source"] = file

            documents.extend(docs)

            print(f"✅ Loaded: {file} ({len(docs)} pages)")

        except Exception as e:
            print(f"❌ Error loading {file}: {e}")

    if not documents:
        raise ValueError("❌ No documents loaded. Cannot build database.")

    print(f"\n📄 Total pages loaded: {len(documents)}")

    # -------------------------
    # SPLIT DOCUMENTS
    # -------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    split_docs = splitter.split_documents(documents)

    if not split_docs:
        raise ValueError("❌ No chunks created. Check document content.")

    print(f"✂️ Total chunks created: {len(split_docs)}")

    # -------------------------
    # EMBEDDINGS
    # -------------------------
    print("\n🔎 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # -------------------------
    # CREATE FAISS DB
    # -------------------------
    print("⚙️ Building FAISS index...")
    db = FAISS.from_documents(split_docs, embeddings)

    os.makedirs(save_path, exist_ok=True)

    db.save_local(save_path)

    print(f"\n💾 Vector DB saved to: {save_path}")
    print("✅ Database build complete!")


# -------------------------
# RUN SCRIPT
# -------------------------
if __name__ == "__main__":
    build_db("data/classical", "vector_db/classical_db")
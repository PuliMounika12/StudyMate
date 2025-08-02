from pdf_reader import extract_text_from_pdf
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load QA model (small instruct model)
qa_pipeline = pipeline("text-generation", model="sshleifer/tiny-gpt2", max_new_tokens=100)

def load_pdf_to_vectorstore(file_path):
    raw_text = extract_text_from_pdf(file_path)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(raw_text)
    
    vectorstore = FAISS.from_texts(texts, embedding_model)
    return vectorstore, texts

def answer_question(vectorstore, texts, question):
    docs = vectorstore.similarity_search(question, k=3)

    if not docs:
        return "❌ Sorry, I couldn't find anything related to your question in the document."

    context = "\n\n".join([doc.page_content for doc in docs])
    
    # 🔴 Limit context length to avoid crashing the model
    context = context[:1000]  # Only take the first 1000 characters

    prompt = f"""Answer the question using the context below:\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"""

    try:
        result = qa_pipeline(prompt)[0]["generated_text"]
        return result[len(prompt):].strip()
    except Exception as e:
        return f"⚠️ Error generating response: {e}"

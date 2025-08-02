import streamlit as st
from qa_engine import load_pdf_to_vectorstore, answer_question

st.title("📚 StudyMate (Open Source Edition)")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    st.success("PDF uploaded! Creating search index...")
    vectorstore, texts = load_pdf_to_vectorstore("temp.pdf")
    st.success("Ready! Ask a question about the PDF below:")

    query = st.text_input("Ask your question")

    if query:
        with st.spinner("Thinking..."):
            answer = answer_question(vectorstore, texts, query)
        st.markdown("### 🤖 Answer:")
        st.write(answer)

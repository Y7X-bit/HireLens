import PyPDF2
import streamlit as st
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Helper Functions ---

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def extract_matched_skills(resume_text: str, job_text: str) -> List[str]:
    """Return list of matched keywords between resume and job description."""
    job_keywords = set(job_text.lower().split())
    resume_keywords = set(resume_text.lower().split())
    matched = job_keywords.intersection(resume_keywords)
    return sorted(list(matched))

def score_resume(resume_text: str, job_text: str) -> float:
    """Return similarity score between job and resume."""
    documents = [job_text, resume_text]
    tfidf = TfidfVectorizer().fit_transform(documents)
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

# --- Streamlit App ---

st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.title("🤖 AI Resume Screener")
st.markdown("Upload a job description and multiple resumes to rank them by relevance.")

# Upload job description
job_file = st.file_uploader("📄 Upload Job Description (TXT)", type=["txt"])

# Upload resumes
resume_files = st.file_uploader("📁 Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if st.button("🚀 Start Screening") and job_file and resume_files:
    with st.spinner("Processing resumes..."):
        job_text = job_file.read().decode("utf-8")
        results: List[Tuple[str, float, List[str]]] = []

        for resume_file in resume_files:
            resume_text = extract_text_from_pdf(resume_file)
            score = score_resume(resume_text, job_text)
            matched_skills = extract_matched_skills(resume_text, job_text)
            results.append((resume_file.name, score, matched_skills))

        results.sort(key=lambda x: x[1], reverse=True)

    st.success("✅ Screening Complete!")

    for i, (filename, score, matched_skills) in enumerate(results, 1):
        st.markdown(f"### {i}. `{filename}` — Score: **{score:.2f}**")
        st.markdown(f"Matched Skills: `{', '.join(matched_skills[:15]) or 'None'}`")
        st.markdown("---")

elif not job_file or not resume_files:
    st.info("⬆️ Upload both a job description and at least one resume to begin.")

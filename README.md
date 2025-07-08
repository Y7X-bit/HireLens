# 🔍 AI Resume Screener

A smart resume screening app powered by Python and Streamlit.  
Upload a **job description** and multiple **PDF resumes**, and get a ranked list based on **skill matching** and **similarity scoring** — all offline, no API needed.

---

### 🚀 Features

✅ Beautiful Streamlit UI  
✅ Upload one `.txt` job description + multiple `.pdf` resumes  
✅ Resume text extracted using `PyPDF2`  
✅ TF-IDF scoring + cosine similarity  
✅ Shows matched keywords from the JD  
✅ 100% offline — no OpenAI key, no internet dependency  

---

### 🖼 Preview

<img src="https://github.com/Y7X-bit/resume-screener-app/assets/preview.png" alt="App Screenshot" width="700"/>

---

### 📂 How To Run

```bash
pip install -r requirements.txt
streamlit run resume_screener_app.py
```

Open your browser to `http://localhost:8501` and you're good to go! 👨‍💼✨

---

### 📦 Folder Structure

```
resume-screener-app/
├── resume_screener_app.py     # Streamlit main app
├── job_description.txt        # Sample JD
├── requirements.txt           # Dependencies
├── .gitignore
└── README.md
```

---

### 🛠 Tech Used

- Python 🐍  
- Streamlit ⚡  
- scikit-learn 🤖  
- PyPDF2 📄

---

### 💗 Powered By

Built with 💻, ☕ and love by **Yugank Singh (Y7X)**  
🔎 Powered by Y7X 💗


import customtkinter as ctk
import os
import PyPDF2
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class HireLensApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("HireLens")
        self.geometry("800x700")
        self.configure(bg="#000000")

        self.jd_path = ""
        self.resume_folder = ""

        self.init_ui()

    def init_ui(self):
        font_title = ctk.CTkFont(size=24, weight="bold")
        font_text = ctk.CTkFont(size=15)

        ctk.CTkLabel(self, text="👓 HireLens", font=font_title, text_color="red", bg_color="#000000").pack(pady=12)
        ctk.CTkLabel(self, text="🖤 Drag & Drop your Job Description and Resume Folder", font=font_text, text_color="white", bg_color="#000000").pack(pady=4)

        self.drop_jd = ctk.CTkTextbox(self, width=540, height=45, font=font_text, corner_radius=12, fg_color="#000000", text_color="white", border_width=2, border_color="red")
        self.drop_jd.pack(pady=10)
        self.drop_jd.insert("1.0", "⬇️ Drop job_description.txt here")
        self.drop_jd.drop_target_register(DND_FILES)
        self.drop_jd.dnd_bind("<<Drop>>", self.handle_jd_drop)

        self.drop_resumes = ctk.CTkTextbox(self, width=540, height=45, font=font_text, corner_radius=12, fg_color="#000000", text_color="white", border_width=2, border_color="red")
        self.drop_resumes.pack(pady=10)
        self.drop_resumes.insert("1.0", "📁 Drop folder with PDF resumes here")
        self.drop_resumes.drop_target_register(DND_FILES)
        self.drop_resumes.dnd_bind("<<Drop>>", self.handle_resume_drop)

        ctk.CTkButton(self, text="🚀 Screen Resumes", command=self.screen_resumes, fg_color="#000000", hover_color="#111111", text_color="white", corner_radius=20, border_width=2, border_color="red").pack(pady=18)

        self.output_textbox = ctk.CTkTextbox(self, width=740, height=290, state="disabled", corner_radius=14, fg_color="#000000", text_color="white", border_width=2, border_color="red")
        self.output_textbox.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13), text_color="white", bg_color="#000000")
        self.status_label.pack(pady=6)

        # 🔎 Powered by Y7X 💗 branding at the bottom
        ctk.CTkLabel(self, text="🔎 Powered by Y7X 💗", font=ctk.CTkFont(size=13, weight="bold"), text_color="white", bg_color="#000000").pack(pady=6)

    def handle_jd_drop(self, event):
        path = event.data.strip("{}")
        if os.path.isfile(path) and path.endswith(".txt"):
            self.jd_path = path
            self.drop_jd.configure(state="normal")
            self.drop_jd.delete("1.0", "end")
            self.drop_jd.insert("1.0", f"✅ Loaded: {os.path.basename(path)}")
            self.drop_jd.configure(state="disabled")
        else:
            messagebox.showerror("❌ Error", "Please drop a valid .txt file.")

    def handle_resume_drop(self, event):
        path = event.data.strip("{}")
        if os.path.isdir(path):
            self.resume_folder = path
            self.drop_resumes.configure(state="normal")
            self.drop_resumes.delete("1.0", "end")
            self.drop_resumes.insert("1.0", f"✅ Folder: {os.path.basename(path)}")
            self.drop_resumes.configure(state="disabled")
        else:
            messagebox.showerror("❌ Error", "Please drop a valid folder.")

    def extract_text_from_pdf(self, path):
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    if page.extract_text():
                        text += page.extract_text()
                return text
        except Exception:
            return ""

    def extract_matched_keywords(self, resume_text, job_text):
        job_keywords = set(job_text.lower().split())
        resume_keywords = set(resume_text.lower().split())
        return sorted(list(job_keywords.intersection(resume_keywords)))

    def score_resume(self, resume_text, job_text):
        documents = [job_text, resume_text]
        tfidf = TfidfVectorizer().fit_transform(documents)
        return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    def screen_resumes(self):
        if not os.path.exists(self.jd_path) or not os.path.exists(self.resume_folder):
            messagebox.showerror("❌ Error", "Missing job description or resume folder.")
            return

        with open(self.jd_path, "r") as f:
            job_text = f.read()

        results = []
        for file in os.listdir(self.resume_folder):
            if file.endswith(".pdf"):
                full_path = os.path.join(self.resume_folder, file)
                resume_text = self.extract_text_from_pdf(full_path)
                score = self.score_resume(resume_text, job_text)
                matched = self.extract_matched_keywords(resume_text, job_text)
                results.append((file, score, ", ".join(matched[:10])))

        results.sort(key=lambda x: x[1], reverse=True)

        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("0.0", "end")

        for i, (fname, score, matched) in enumerate(results, 1):
            self.output_textbox.insert("end", f"{i}. {fname} — Score: {score:.2f}\nMatched: {matched}\n\n")

        self.output_textbox.configure(state="disabled")

        with open("ranking_output.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Resume", "Score", "Matched Keywords"])
            writer.writerows(results)

        self.status_label.configure(text="✅ Screening complete. Results saved as CSV!")

if __name__ == "__main__":
    app = HireLensApp()
    app.mainloop()
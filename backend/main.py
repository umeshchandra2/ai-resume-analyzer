from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-resume-analyzer-six-kappa.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Backend Running"}


@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        pdf_bytes = await file.read()

        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))

        resume_text = ""

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text.lower()

        jd_text = job_description.lower()

        jd_words = set(jd_text.split())
        resume_words = set(resume_text.split())

        matched_skills = list(jd_words.intersection(resume_words))
        missing_skills = list(jd_words.difference(resume_words))

        ats_score = 0
        if len(jd_words) > 0:
            ats_score = round(
                (len(matched_skills) / len(jd_words)) * 100
            )

        if ats_score >= 80:
            recommendation = "Excellent Match"
        elif ats_score >= 60:
            recommendation = "Good Match"
        elif ats_score >= 40:
            recommendation = "Average Match"
        else:
            recommendation = "Needs Improvement"

        suggestions = []

        if ats_score < 80:
            suggestions.append(
                "Add more keywords from the job description."
            )

        if len(missing_skills) > 0:
            suggestions.append(
                "Include missing technical skills where applicable."
            )

        suggestions.append(
            "Quantify achievements with numbers and metrics."
        )

        return {
            "ats_score": ats_score,
            "recommendation": recommendation,
            "matched_skills": matched_skills[:20],
            "missing_skills": missing_skills[:20],
            "suggestions": suggestions,
            "resume_strength": [
                "Resume uploaded successfully",
                "PDF parsed successfully",
                "Keyword comparison completed"
            ]
        }

    except Exception as e:
        return {
            "ats_score": 0,
            "recommendation": "Error",
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": [str(e)],
            "resume_strength": []
        }
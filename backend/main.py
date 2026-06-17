from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    pdf_content = await file.read()
    pdf = PdfReader(io.BytesIO(pdf_content))

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    resume_text = text.lower()
    jd_text = job_description.lower()

    skills = [
        "python", "java", "sql", "mysql", "react", "javascript",
        "html", "css", "machine learning", "git", "github",
        "fastapi", "aws", "azure", "docker", "power bi",
        "postgresql", "mongodb", "node.js", "express.js",
        "rest api", "flask", "django"
    ]

    resume_skills = []
    job_skills = []

    for skill in skills:
        if skill in resume_text:
            resume_skills.append(skill)

        if skill in jd_text:
            job_skills.append(skill)

    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(job_skills) == 0:
        ats_score = 0
    else:
        ats_score = int((len(matched_skills) / len(job_skills)) * 100)

    if ats_score >= 80:
        recommendation = "Excellent Match"
    elif ats_score >= 60:
        recommendation = "Good Match"
    elif ats_score >= 40:
        recommendation = "Average Match"
    else:
        recommendation = "Needs Improvement"

    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            f"Consider adding {skill} projects or experience to your resume."
        )

    resume_strength = []

    if len(resume_skills) >= 10:
        resume_strength.append("Strong technical skill coverage")

    if "python" in resume_skills:
        resume_strength.append("Python experience detected")

    if "sql" in resume_skills:
        resume_strength.append("Database skills detected")

    if "machine learning" in resume_skills:
        resume_strength.append("Machine Learning background detected")

    if "react" in resume_skills:
        resume_strength.append("Frontend development experience detected")

    return {
        "filename": file.filename,
        "resume_skills": resume_skills,
        "job_skills_required": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "recommendation": recommendation,
        "suggestions": suggestions,
        "resume_strength": resume_strength
    }
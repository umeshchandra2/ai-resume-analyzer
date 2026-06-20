import os
import io
import json
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

genai.configure(api_key=os.getenv("GEMINI_API_KEY_AI_RESUME"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

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
                resume_text += text + "\n"

        prompt = f"""
You are an ATS Resume Analyzer.

Analyze the resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY valid JSON in this exact format:
{{
  "ats_score": 0,
  "recommendation": "",
  "matched_skills": [],
  "missing_skills": [],
  "suggestions": [],
  "resume_strength": []
}}

Rules:
- ats_score must be a number from 0 to 100.
- matched_skills should include only real technical or business skills.
- missing_skills should include only important missing skills from the job description.
- suggestions should be clear resume improvement suggestions.
- resume_strength should mention strong points from the resume.
- Do not include common words like for, and, with, this, of.
"""

        gemini_response = model.generate_content(prompt)
        response_text = gemini_response.text.strip()

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        result = json.loads(response_text)
        return result

    except Exception as e:
        return {
            "ats_score": 0,
            "recommendation": "Error",
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": [f"Error analyzing resume: {str(e)}"],
            "resume_strength": []
        }
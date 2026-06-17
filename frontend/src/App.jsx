import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!file) {
      alert("Please upload a resume");
      return;
    }

    if (!jobDescription.trim()) {
      alert("Please paste a job description");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);
      formData.append("job_description", jobDescription);

      const response = await fetch(
        "https://ai-resume-analyzer-hwps.onrender.com/analyze-resume",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log("API Response:", data);

      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Error analyzing resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AI Resume Analyzer</h1>
      <p className="subtitle">
        Compare your resume with a job description
      </p>

      <div className="card">
        <label>Upload Resume PDF</label>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <label>Paste Job Description</label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste job description here..."
        />

        <button onClick={analyzeResume} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </div>

      {result && (
        <div className="results">
          <h2>Results</h2>

          <div className="score-box">
            <h3>ATS Score</h3>
            <p>{result.ats_score || 0}%</p>
            <span>{result.recommendation || "No recommendation"}</span>
          </div>

          <div className="skills-grid">
            <div className="skill-card">
              <h3>Matched Skills</h3>
              {result.matched_skills?.length > 0 ? (
                result.matched_skills.map((skill, index) => (
                  <p className="matched" key={index}>
                    ✓ {skill}
                  </p>
                ))
              ) : (
                <p>No matched skills found</p>
              )}
            </div>

            <div className="skill-card">
              <h3>Missing Skills</h3>
              {result.missing_skills?.length > 0 ? (
                result.missing_skills.map((skill, index) => (
                  <p className="missing" key={index}>
                    ✗ {skill}
                  </p>
                ))
              ) : (
                <p>No missing skills found</p>
              )}
            </div>

            <div className="skill-card">
              <h3>Suggestions</h3>
              {result.suggestions?.length > 0 ? (
                result.suggestions.map((item, index) => (
                  <p key={index}>💡 {item}</p>
                ))
              ) : (
                <p>No suggestions available</p>
              )}
            </div>

            <div className="skill-card">
              <h3>Resume Strengths</h3>
              {result.resume_strength?.length > 0 ? (
                result.resume_strength.map((item, index) => (
                  <p key={index}>✅ {item}</p>
                ))
              ) : (
                <p>No strengths available</p>
              )}
            </div>
          </div>


        </div>
      )}
    </div>
  );
}

export default App;
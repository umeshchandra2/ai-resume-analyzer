import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);

  const analyzeResume = async () => {
    if (!file) {
      alert("Please upload a resume");
      return;
    }

    if (!jobDescription.trim()) {
      alert("Please paste a job description");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    const response = await fetch("https://ai-resume-analyzer-hwps.onrender.com/analyze-resume", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="container">
      <h1>AI Resume Analyzer</h1>
      <p className="subtitle">Compare your resume with a job description</p>

      <div className="card">
        <label>Upload Resume PDF</label>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />

        <label>Paste Job Description</label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste job description here..."
        />

        <button onClick={analyzeResume}>Analyze Resume</button>
      </div>

      {result && (
        <div className="results">
          <h2>Results</h2>

          <div className="score-box">
            <h3>ATS Score</h3>
            <p>{result.ats_score}%</p>
            <span>{result.recommendation}</span>
          </div>

          <div className="skills-grid">
            <div className="skill-card">
              <h3>Matched Skills</h3>
              {result.matched_skills.map((skill) => (
                <p className="matched" key={skill}>
                  ✓ {skill}
                </p>
              ))}
            </div>

            <div className="skill-card">
              <h3>Missing Skills</h3>
              {result.missing_skills.map((skill) => (
                <p className="missing" key={skill}>
                  ✗ {skill}
                </p>
              ))}
            </div>

            <div className="skill-card">
              <h3>Suggestions</h3>
              {result.suggestions.map((item, index) => (
                <p key={index}>💡 {item}</p>
              ))}
            </div>

            <div className="skill-card">
              <h3>Resume Strengths</h3>
              {result.resume_strength.map((item, index) => (
                <p key={index}>✅ {item}</p>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
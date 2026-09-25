import { useState } from "react";
import "./App.css";

function ScoreCircle({ score }) {
  const value = Number(score || 0);

  return (
    <div
      className="score-circle"
      style={{
        "--score": `${Math.min(Math.max(value, 0), 100) * 3.6}deg`,
      }}
    >
      <span>{value.toFixed(2)}%</span>
    </div>
  );
}

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleResumeChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Please upload a PDF resume.");
      return;
    }

    setResume(file);
    setError("");
  };

  const analyzeResume = async () => {
    if (!resume) {
      setError("Please upload your resume PDF.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter the job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Analysis failed.");
      }

      const data = await response.json();

      setResult(data);

      setTimeout(() => {
        document
          .getElementById("results")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
      }, 100);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to the backend. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatSkill = (skill) => {
    if (!skill) return "";

    return skill
      .split(" ")
      .map(
        (word) =>
          word.charAt(0).toUpperCase() + word.slice(1)
      )
      .join(" ");
  };

  const overallScore = Number(
    result?.overall_match_score || 0
  );

  const qualityScore = Number(
    result?.resume_quality?.quality_score || 0
  );

  return (
    <div className="app">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="header">

        <div className="brand">

          <div className="brand-logo">
            AI
          </div>

          <div>
            <h2>ResumeAI</h2>

            <p>
              Resume Intelligence Platform
            </p>
          </div>

        </div>

        <div className="status-pill">
          <span className="status-dot"></span>
          AI Engine Ready
        </div>

      </header>


      {/* =====================================================
          HERO + INPUT
      ===================================================== */}

      <main>

        <section className="hero">

          <span className="section-label">
            AI RESUME ANALYZER
          </span>

          <h1 className="hero-title">
            Match your resume
            <br />
            with any job.
          </h1>

          <p className="hero-description">
            Upload your resume and job description to get an
            AI-powered compatibility analysis, ATS insights,
            missing skills and improvement recommendations.
          </p>


          {/* INPUT CARDS */}

          <div className="input-grid">


            {/* =================================================
                RESUME UPLOAD
            ================================================= */}

            <div className="input-card">

              <div className="card-header">

                <div className="card-icon upload-icon">
                  ↑
                </div>

                <div>
                  <h3>
                    Upload Resume
                  </h3>

                  <p>
                    PDF format only
                  </p>
                </div>

              </div>


              <label className="upload-zone">

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleResumeChange}
                  style={{ display: "none" }}
                />

                <div className="upload-icon-large">
                  ↑
                </div>

                {resume ? (
                  <>
                    <h4 title={resume.name}>
                      {resume.name}
                    </h4>

                    <p>
                      {(resume.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </>
                ) : (
                  <>
                    <h4>
                      Click to upload your resume
                    </h4>

                    <p>
                      PDF files only
                    </p>
                  </>
                )}

              </label>

            </div>


            {/* =================================================
                JOB DESCRIPTION
            ================================================= */}

            <div className="input-card">

              <div className="card-header">

                <div className="card-icon jd-icon">
                  JD
                </div>

                <div>
                  <h3>
                    Job Description
                  </h3>

                  <p>
                    Paste the target job description
                  </p>
                </div>

              </div>


              <textarea
                className="job-textarea"
                placeholder="Paste the job description here..."
                value={jobDescription}
                onChange={(event) =>
                  setJobDescription(event.target.value)
                }
              />

            </div>

          </div>


          {/* ERROR */}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}


          {/* ANALYZE BUTTON */}

          <button
            className="analyze-button"
            onClick={analyzeResume}
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>
                Analyze Resume →
              </>
            )}

          </button>

        </section>


        {/* =====================================================
            RESULTS
        ===================================================== */}

        {result && (

          <section
            className="results-section"
            id="results"
          >

            {/* RESULTS HEADING */}

            <div className="results-heading">

              <span className="section-label">
                ANALYSIS COMPLETE
              </span>

              <h2>
                Resume Analysis Results
              </h2>

              <p>
                Here is the compatibility analysis between your
                resume and the selected job description.
              </p>

            </div>


            {/* =================================================
                OVERALL MATCH
            ================================================= */}

            <div className="overall-card">

              <div className="overall-info">

                <span className="section-label">
                  OVERALL MATCH
                </span>

                <h2>
                  Resume Compatibility
                </h2>

                <p>
                  Overall compatibility between your resume
                  and the selected job description.
                </p>

              </div>


              <div
                className="overall-score"
                style={{
                  "--overall-score": `${Math.min(
                    Math.max(overallScore, 0),
                    100
                  ) * 3.6}deg`,
                }}
              >

                <span>
                  {overallScore.toFixed(2)}%
                </span>

              </div>

            </div>


            {/* =================================================
                SCORE BREAKDOWN
            ================================================= */}

            <div className="section-heading">

              <span className="section-label">
                SCORE BREAKDOWN
              </span>

              <h2>
                Detailed Scores
              </h2>

            </div>


            <div className="score-grid">


              {/* KEYWORD */}

              <div className="score-card">

                <ScoreCircle
                  score={result.keyword_match_score}
                />

                <h3>
                  Keyword Match
                </h3>

                <p>
                  Skills directly matching the job
                  requirements.
                </p>

              </div>


              {/* SEMANTIC */}

              <div className="score-card">

                <ScoreCircle
                  score={result.semantic_match_score}
                />

                <h3>
                  Semantic Match
                </h3>

                <p>
                  AI-based similarity between your
                  resume and the job.
                </p>

              </div>


              {/* ATS */}

              <div className="score-card">

                <ScoreCircle
                  score={result.ats_score}
                />

                <h3>
                  ATS Score
                </h3>

                <p>
                  Important job keywords detected
                  in your resume.
                </p>

              </div>


              {/* QUALITY */}

              <div className="score-card">

                <ScoreCircle
                  score={qualityScore}
                />

                <h3>
                  Resume Quality
                </h3>

                <p>
                  Basic ATS-friendly resume quality
                  analysis.
                </p>

              </div>

            </div>


            {/* =================================================
                JOB ANALYSIS
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                JOB ANALYSIS
              </span>

              <h2>
                Job Description Analysis
              </h2>


              <div className="job-analysis-card">


                <div className="job-info-row">

                  <span>
                    Job Title
                  </span>

                  <strong>
                    {result.job_analysis?.job_title ||
                      "Not detected"}
                  </strong>

                </div>


                <div className="job-info-row">

                  <span>
                    Experience
                  </span>

                  <strong>
                    {result.job_analysis?.experience?.join(
                      ", "
                    ) || "Not specified"}
                  </strong>

                </div>


                <div className="job-info-row">

                  <span>
                    Education
                  </span>

                  <strong>
                    {result.job_analysis?.education?.join(
                      ", "
                    ) || "Not specified"}
                  </strong>

                </div>

              </div>


              {/* REQUIRED SKILLS */}

              <h3 className="sub-heading">
                Required Skills
              </h3>

              <div className="tag-container">

                {result.job_analysis?.required_skills
                  ?.length > 0 ? (

                  result.job_analysis.required_skills.map(
                    (skill) => (
                      <span
                        className="skill-tag"
                        key={skill}
                      >
                        {formatSkill(skill)}
                      </span>
                    )
                  )

                ) : (
                  <p className="empty-text">
                    No required skills detected.
                  </p>
                )}

              </div>


              {/* PREFERRED SKILLS */}

              {result.job_analysis?.preferred_skills
                ?.length > 0 && (

                <>
                  <h3 className="sub-heading">
                    Preferred Skills
                  </h3>

                  <div className="tag-container">

                    {result.job_analysis.preferred_skills.map(
                      (skill) => (
                        <span
                          className="preferred-tag"
                          key={skill}
                        >
                          {formatSkill(skill)}
                        </span>
                      )
                    )}

                  </div>
                </>
              )}


              {/* RESPONSIBILITIES */}

              {result.job_analysis?.responsibilities
                ?.length > 0 && (

                <>
                  <h3 className="sub-heading">
                    Key Responsibilities
                  </h3>

                  <div className="responsibility-list">

                    {result.job_analysis.responsibilities.map(
                      (item, index) => (

                        <div
                          className="responsibility-item"
                          key={index}
                        >

                          <span>
                            {index + 1}
                          </span>

                          <p>
                            {item}
                          </p>

                        </div>

                      )
                    )}

                  </div>
                </>
              )}

            </section>


            {/* =================================================
                RESUME SKILLS
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                RESUME SKILLS
              </span>

              <h2>
                Skills Detected in Your Resume
              </h2>

              <div className="tag-container">

                {result.resume_skills?.length > 0 ? (

                  result.resume_skills.map(
                    (skill) => (
                      <span
                        className="skill-tag"
                        key={skill}
                      >
                        {formatSkill(skill)}
                      </span>
                    )
                  )

                ) : (
                  <p className="empty-text">
                    No technical skills detected.
                  </p>
                )}

              </div>

            </section>


            {/* =================================================
                MATCHED SKILLS
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                MATCHED SKILLS
              </span>

              <h2>
                Skills You Have
              </h2>

              <div className="tag-container">

                {result.matched_skills?.length > 0 ? (

                  result.matched_skills.map(
                    (skill) => (
                      <span
                        className="matched-tag"
                        key={skill}
                      >
                        ✓ {formatSkill(skill)}
                      </span>
                    )
                  )

                ) : (
                  <p className="empty-text">
                    No matching skills found.
                  </p>
                )}

              </div>

            </section>


            {/* =================================================
                MISSING SKILLS
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                MISSING SKILLS
              </span>

              <h2>
                Skills to Improve
              </h2>

              <div className="tag-container">

                {result.missing_skills?.length > 0 ? (

                  result.missing_skills.map(
                    (skill) => (
                      <span
                        className="missing-tag"
                        key={skill}
                      >
                        + {formatSkill(skill)}
                      </span>
                    )
                  )

                ) : (
                  <p className="empty-text">
                    No major missing skills.
                  </p>
                )}

              </div>

            </section>


            {/* =================================================
                RESUME QUALITY
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                RESUME QUALITY
              </span>

              <h2>
                Resume Quality Analysis
              </h2>


              <div className="quality-card">

                <div className="quality-score">
                  {qualityScore}%
                </div>

                <div className="quality-label">
                  Quality Score
                </div>

                <p>
                  {result.resume_quality?.word_count || 0}
                  {" "}
                  words detected in your resume.
                </p>

              </div>


              {result.resume_quality?.feedback?.length > 0 && (

                <div className="feedback-list">

                  {result.resume_quality.feedback.map(
                    (feedback, index) => (

                      <div
                        className="feedback-item"
                        key={index}
                      >

                        <span>
                          •
                        </span>

                        <p>
                          {feedback}
                        </p>

                      </div>

                    )
                  )}

                </div>

              )}

            </section>


            {/* =================================================
                SKILL GAP
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                SKILL GAP
              </span>

              <h2>
                Skill Gap Suggestions
              </h2>


              <div className="suggestion-list">

                {result.skill_gap_suggestions?.length > 0 ? (

                  result.skill_gap_suggestions.map(
                    (suggestion, index) => (

                      <div
                        className="suggestion-item"
                        key={index}
                      >

                        <span>
                          {index + 1}
                        </span>

                        <p>
                          {suggestion}
                        </p>

                      </div>

                    )
                  )

                ) : (
                  <p className="empty-text">
                    No skill gap suggestions available.
                  </p>
                )}

              </div>

            </section>


            {/* =================================================
                AI RECOMMENDATIONS
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                AI RECOMMENDATIONS
              </span>

              <h2>
                Resume Improvement Recommendations
              </h2>


              <div className="suggestion-list">

                {result.resume_recommendations?.length > 0 ? (

                  result.resume_recommendations.map(
                    (recommendation, index) => (

                      <div
                        className="suggestion-item"
                        key={index}
                      >

                        <span>
                          {index + 1}
                        </span>

                        <p>
                          {recommendation}
                        </p>

                      </div>

                    )
                  )

                ) : (
                  <p className="empty-text">
                    No additional recommendations.
                  </p>
                )}

              </div>

            </section>


            {/* =================================================
                ATS ANALYSIS
            ================================================= */}

            <section className="result-section">

              <span className="section-label">
                ATS ANALYSIS
              </span>

              <h2>
                ATS Keyword Analysis
              </h2>


              <div className="ats-grid">


                <div className="ats-card">

                  <div className="ats-number">
                    {result.ats_analysis?.ats_score || 0}%
                  </div>

                  <p>
                    ATS Score
                  </p>

                </div>


                <div className="ats-card">

                  <div className="ats-number">
                    {result.ats_analysis?.required_keywords
                      ?.length || 0}
                  </div>

                  <p>
                    Required Keywords
                  </p>

                </div>

              </div>


              {/* MATCHED KEYWORDS */}

              <h3 className="sub-heading">
                Matched Keywords
              </h3>

              <div className="tag-container">

                {result.ats_analysis?.matched_keywords
                  ?.length > 0 ? (

                  result.ats_analysis.matched_keywords.map(
                    (keyword) => (
                      <span
                        className="matched-tag"
                        key={keyword}
                      >
                        ✓ {formatSkill(keyword)}
                      </span>
                    )
                  )

                ) : (
                  <p className="empty-text">
                    No matched keywords.
                  </p>
                )}

              </div>


              {/* MISSING KEYWORDS */}

              <h3 className="sub-heading">
                Missing Keywords
              </h3>

              <div className="tag-container">

                {result.ats_analysis?.missing_keywords
                  ?.length > 0 ? (

                  result.ats_analysis.missing_keywords.map(
                    (keyword) => (
                      <span
                        className="missing-tag"
                        key={keyword}
                      >
                        + {formatSkill(keyword)}
                      </span>
                    )
                  )

                ) : (
                  <p className="empty-text">
                    No missing keywords.
                  </p>
                )}

              </div>

            </section>

          </section>
        )}

      </main>


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="footer">
        AI Resume Analyzer • Resume & Job Compatibility Platform
      </footer>

    </div>
  );
}

export default App;
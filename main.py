from app.resume_parser import extract_text_from_pdf
from app.skill_extractor import extract_skills, analyze_job_description
from app.matcher import calculate_match
from app.semantic_matcher import calculate_semantic_match
from app.skill_gap import generate_skill_gap


# File paths
resume_path = "data/resume.pdf"
job_path = "data/job_description.txt"


# 1. Extract text from resume PDF
resume_text = extract_text_from_pdf(resume_path)


# 2. Read job description
with open(job_path, "r", encoding="utf-8") as file:
    job_description = file.read()


# 3. Extract skills from resume and job description
resume_skills = extract_skills(resume_text)
required_skills = analyze_job_description(job_description)


# 4. Calculate keyword-based ATS match
matched_skills, missing_skills, keyword_score = calculate_match(
    resume_skills,
    required_skills
)


# 5. Calculate semantic AI match
semantic_score = calculate_semantic_match(
    resume_text,
    job_description
)


# 6. Calculate overall match score
overall_score = (keyword_score * 0.5) + (semantic_score * 0.5)


# 7. Generate skill-gap suggestions
skill_gap_suggestions = generate_skill_gap(missing_skills)


# 8. Display results
print("=" * 50)
print("       AI RESUME ANALYZER")
print("=" * 50)


print()
print("RESUME SKILLS")
print("-" * 30)

for skill in resume_skills:
    print("✓", skill)


print()
print("JOB REQUIRED SKILLS")
print("-" * 30)

for skill in required_skills:
    print("•", skill)


print()
print("ATS MATCH ANALYSIS")
print("-" * 30)

print("Keyword Match Score:", round(keyword_score, 2), "%")
print("Semantic Match Score:", round(semantic_score, 2), "%")
print("Overall Match Score:", round(overall_score, 2), "%")


print()
print("MATCHED SKILLS")
print("-" * 30)

if matched_skills:
    for skill in sorted(matched_skills):
        print("✓", skill)
else:
    print("No matching skills found.")


print()
print("MISSING SKILLS")
print("-" * 30)

if missing_skills:
    for skill in sorted(missing_skills):
        print("✗", skill)
else:
    print("No missing skills found.")


print()
print("SKILL GAP ANALYSIS")
print("-" * 30)

for suggestion in skill_gap_suggestions:
    print("→", suggestion)


print()
print("=" * 50)
print("       ANALYSIS COMPLETED")
print("=" * 50)
import re


def extract_important_keywords(job_description):
    """
    Extract important technical keywords from a job description.
    """

    keywords = [
        "java",
        "python",
        "javascript",
        "react",
        "angular",
        "spring boot",
        "fastapi",
        "mysql",
        "postgresql",
        "mongodb",
        "docker",
        "kubernetes",
        "git",
        "github",
        "rest api",
        "machine learning",
        "nlp",
        "llm",
        "generative ai",
        "rag",
        "aws",
        "azure",
        "microservices",
        "sql",
    ]

    job_text = job_description.lower()

    found_keywords = []

    for keyword in keywords:

        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

        if re.search(pattern, job_text):
            found_keywords.append(keyword)

    return sorted(found_keywords)


def analyze_ats_keywords(resume_text, job_description):

    resume_text = resume_text.lower()

    required_keywords = extract_important_keywords(
        job_description
    )

    matched_keywords = []
    missing_keywords = []

    for keyword in required_keywords:

        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

        if re.search(pattern, resume_text):
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    if len(required_keywords) == 0:
        ats_score = 0
    else:
        ats_score = (
            len(matched_keywords)
            / len(required_keywords)
        ) * 100

    return {
        "ats_score": round(float(ats_score), 2),
        "required_keywords": required_keywords,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords
    }
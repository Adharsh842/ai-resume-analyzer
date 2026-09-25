import re


TECHNICAL_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "spring boot",
    "spring",
    "fastapi",
    "flask",
    "django",
    "node.js",
    "nodejs",
    "express",
    "html",
    "css",
    "tailwind",
    "bootstrap",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "sql",
    "docker",
    "kubernetes",
    "git",
    "github",
    "gitlab",
    "rest api",
    "restful api",
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "llm",
    "generative ai",
    "rag",
    "prompt engineering",
    "aws",
    "azure",
    "gcp",
    "redis",
    "kafka",
    "microservices",
    "junit",
    "maven",
    "gradle"
}


# Common variations of the same skill
SKILL_ALIASES = {
    "js": "javascript",
    "javascript": "javascript",

    "ts": "typescript",
    "typescript": "typescript",

    "react.js": "react",
    "reactjs": "react",
    "react": "react",

    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "mongo": "mongodb",
    "mongodb": "mongodb",

    "rest": "rest api",
    "rest api": "rest api",
    "restful api": "restful api",

    "ml": "machine learning",
    "machine learning": "machine learning",

    "ai": "generative ai",
    "generative ai": "generative ai",

    "natural language processing": "natural language processing",
    "nlp": "nlp",

    "rag": "rag",

    "aws": "aws",
    "amazon web services": "aws"
}


def normalize_text(text):
    """
    Convert text into a normalized format
    for reliable skill matching.
    """

    text = text.lower()

    # Replace special characters with spaces
    text = re.sub(r"[^a-z0-9+#.\-/ ]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):

    text = normalize_text(text)

    found_skills = set()

    for skill in TECHNICAL_SKILLS:

        # Escape skill so characters like + and . are handled safely
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.add(skill)

    # Check aliases
    for alias, actual_skill in SKILL_ALIASES.items():

        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.add(actual_skill)

    return sorted(found_skills)


def analyze_job_description(job_description):

    return extract_skills(job_description)
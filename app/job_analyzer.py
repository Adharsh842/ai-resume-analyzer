import re


# ==========================================
# COMMON JOB TITLES
# ==========================================

JOB_TITLES = [
    "software development engineer",
    "associate software engineer",
    "software developer",
    "software engineer",
    "backend developer",
    "backend engineer",
    "frontend developer",
    "frontend engineer",
    "full stack developer",
    "full stack engineer",
    "java developer",
    "python developer",
    "react developer",
    "web developer",
    "application developer",
    "devops engineer",
    "data analyst",
    "data scientist",
    "machine learning engineer"
]


# ==========================================
# EDUCATION KEYWORDS
# ==========================================

EDUCATION_KEYWORDS = [
    "b.tech",
    "b.e",
    "bachelor",
    "bachelors",
    "b.sc",
    "bca",
    "m.tech",
    "mca",
    "master",
    "degree",
    "computer science",
    "information technology"
]


# ==========================================
# EXPERIENCE PATTERNS
# ==========================================

EXPERIENCE_PATTERNS = [
    r"\b\d+\s*-\s*\d+\s*years?\b",
    r"\b\d+\+?\s*years?\b",
    r"\bfresher\b",
    r"\bentry[- ]level\b",
    r"\bexperienced\b"
]


# ==========================================
# TECHNICAL KEYWORDS
# ==========================================

TECHNICAL_KEYWORDS = [
    "java",
    "python",
    "javascript",
    "typescript",

    "react",
    "angular",
    "vue",

    "html",
    "css",
    "tailwind",
    "bootstrap",

    "spring boot",

    "fastapi",
    "flask",
    "django",

    "node.js",
    "nodejs",
    "express",

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

    "microservices",

    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "llm",
    "generative ai",
    "rag",

    "aws",
    "azure",
    "gcp",

    "redis",
    "kafka",

    "junit",
    "maven",
    "gradle"
]


# ==========================================
# TEXT NORMALIZATION
# ==========================================

def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# JOB TITLE
# ==========================================

def extract_job_title(job_description):

    text = normalize_text(
        job_description
    )

    found_titles = []

    for title in JOB_TITLES:

        pattern = (
            r"(?<!\w)"
            + re.escape(title)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            found_titles.append(
                title.title()
            )

    if found_titles:

        return found_titles[0]

    return "Not detected"


# ==========================================
# TECHNICAL SKILLS
# ==========================================

def extract_job_skills(job_description):

    text = normalize_text(
        job_description
    )

    found_skills = []

    for skill in TECHNICAL_KEYWORDS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            found_skills.append(
                skill
            )

    return sorted(
        set(found_skills)
    )


# ==========================================
# EXPERIENCE
# ==========================================

def extract_experience(job_description):

    text = normalize_text(
        job_description
    )

    found_experience = []

    # First check ranges such as 0-2 years
    range_matches = re.findall(
        r"\b\d+\s*-\s*\d+\s*years?\b",
        text
    )

    if range_matches:

        found_experience.extend(
            range_matches
        )

    else:

        # Check individual experience values
        individual_matches = re.findall(
            r"\b\d+\+?\s*years?\b",
            text
        )

        found_experience.extend(
            individual_matches
        )

    # Check fresher / entry level
    for pattern in [
        r"\bfresher\b",
        r"\bentry[- ]level\b",
        r"\bexperienced\b"
    ]:

        matches = re.findall(
            pattern,
            text
        )

        found_experience.extend(
            matches
        )

    if found_experience:

        return sorted(
            set(found_experience)
        )

    return ["Not specified"]


# ==========================================
# EDUCATION
# ==========================================

def extract_education(job_description):

    text = normalize_text(
        job_description
    )

    found_education = []

    for keyword in EDUCATION_KEYWORDS:

        pattern = (
            r"(?<!\w)"
            + re.escape(keyword)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            found_education.append(
                keyword.upper()
            )

    if found_education:

        return sorted(
            set(found_education)
        )

    return ["Not specified"]


# ==========================================
# RESPONSIBILITIES
# ==========================================

def extract_responsibilities(job_description):

    lines = job_description.splitlines()

    responsibilities = []

    responsibility_words = [
        "develop",
        "developed",
        "design",
        "designed",
        "build",
        "built",
        "implement",
        "implemented",
        "maintain",
        "maintaining",
        "create",
        "created",
        "test",
        "testing",
        "deploy",
        "deployment",
        "integrate",
        "integration",
        "collaborate",
        "manage",
        "analyze"
    ]

    ignore_phrases = [
        "we are looking",
        "we're looking",
        "job description",
        "requirements:",
        "required skills:",
        "preferred:",
        "preferred skills:",
        "preferred qualifications:"
    ]

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Ignore headings and introductory sentences
        should_ignore = False

        for phrase in ignore_phrases:

            if lower_line.startswith(phrase):

                should_ignore = True
                break

        if should_ignore:
            continue

        # Check responsibility keywords
        for word in responsibility_words:

            pattern = (
                r"\b"
                + re.escape(word)
                + r"\b"
            )

            if re.search(
                pattern,
                lower_line
            ):

                responsibilities.append(
                    clean_line
                )

                break

    return responsibilities[:10]


# ==========================================
# PREFERRED SKILLS
# ==========================================

def extract_preferred_skills(job_description):

    lines = job_description.splitlines()

    preferred_lines = []

    in_preferred_section = False

    preferred_markers = [
        "preferred:",
        "preferred skills:",
        "preferred qualifications:",
        "nice to have:",
        "good to have:"
    ]

    section_end_markers = [
        "responsibilities:",
        "requirements:",
        "required skills:",
        "qualifications:"
    ]

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Start preferred section
        if any(
            marker in lower_line
            for marker in preferred_markers
        ):

            in_preferred_section = True

            # Capture text after the heading
            for marker in preferred_markers:

                if marker in lower_line:

                    after_marker = lower_line.split(
                        marker,
                        1
                    )[1]

                    if after_marker.strip():

                        preferred_lines.append(
                            after_marker
                        )

                    break

            continue

        # Stop when another section begins
        if in_preferred_section:

            if any(
                marker in lower_line
                for marker in section_end_markers
            ):

                in_preferred_section = False
                continue

            preferred_lines.append(
                lower_line
            )

    preferred_text = " ".join(
        preferred_lines
    )

    if not preferred_text:

        return []

    found_skills = []

    for skill in TECHNICAL_KEYWORDS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            preferred_text
        ):

            found_skills.append(
                skill
            )

    return sorted(
        set(found_skills)
    )


# ==========================================
# MAIN JOB ANALYZER
# ==========================================

def analyze_job_description_details(
    job_description
):

    job_title = extract_job_title(
        job_description
    )

    skills = extract_job_skills(
        job_description
    )

    experience = extract_experience(
        job_description
    )

    education = extract_education(
        job_description
    )

    responsibilities = extract_responsibilities(
        job_description
    )

    preferred_skills = extract_preferred_skills(
        job_description
    )

    # Skills not classified as preferred
    # are treated as required skills.
    required_skills = [
        skill
        for skill in skills
        if skill not in preferred_skills
    ]

    return {

        "job_title": job_title,

        "required_skills": required_skills,

        "preferred_skills": preferred_skills,

        "experience": experience,

        "education": education,

        "responsibilities": responsibilities
    }
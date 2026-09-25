import re


def calculate_resume_quality(resume_text):

    text = resume_text.lower()

    score = 0
    feedback = []

    # --------------------------------
    # 1. Contact Information
    # --------------------------------

    has_email = bool(
        re.search(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            resume_text
        )
    )

    has_phone = bool(
        re.search(
            r"\b\d{10}\b",
            resume_text
        )
    )

    if has_email:
        score += 10
    else:
        feedback.append(
            "Add a professional email address."
        )

    if has_phone:
        score += 10
    else:
        feedback.append(
            "Add a valid phone number."
        )


    # --------------------------------
    # 2. Skills Section
    # --------------------------------

    if re.search(
        r"\bskills\b|\btechnical skills\b",
        text
    ):
        score += 10
    else:
        feedback.append(
            "Add a dedicated Skills section."
        )


    # --------------------------------
    # 3. Education Section
    # --------------------------------

    if re.search(
        r"\beducation\b|\bdegree\b|\bb.tech\b|\bbachelor\b",
        text
    ):
        score += 10
    else:
        feedback.append(
            "Add an Education section."
        )


    # --------------------------------
    # 4. Projects Section
    # --------------------------------

    if re.search(
        r"\bprojects\b|\bproject\b",
        text
    ):
        score += 10
    else:
        feedback.append(
            "Add relevant technical projects."
        )


    # --------------------------------
    # 5. Experience / Internship
    # --------------------------------

    if re.search(
        r"\bexperience\b|\binternship\b|\bintern\b",
        text
    ):
        score += 10
    else:
        feedback.append(
            "Add internship or relevant experience if available."
        )


    # --------------------------------
    # 6. Action Words
    # --------------------------------

    action_words = [
        "developed",
        "implemented",
        "designed",
        "created",
        "built",
        "developed",
        "integrated",
        "optimized",
        "managed",
        "analyzed"
    ]

    action_word_found = False

    for word in action_words:
        if re.search(
            r"\b" + re.escape(word) + r"\b",
            text
        ):
            action_word_found = True
            break

    if action_word_found:
        score += 10
    else:
        feedback.append(
            "Use strong action words such as Developed, Implemented, Designed and Built."
        )


    # --------------------------------
    # 7. Resume Length
    # --------------------------------

    word_count = len(
        resume_text.split()
    )

    if 250 <= word_count <= 1000:
        score += 10
    elif word_count < 250:
        feedback.append(
            "Resume content appears too short. Add relevant details."
        )
    else:
        feedback.append(
            "Resume may contain too much content. Keep it concise and relevant."
        )


    # --------------------------------
    # 8. Technical Keywords
    # --------------------------------

    technical_keywords = [
        "java",
        "python",
        "javascript",
        "react",
        "spring boot",
        "sql",
        "mysql",
        "postgresql",
        "git",
        "docker",
        "fastapi",
        "rest api"
    ]

    technical_count = 0

    for keyword in technical_keywords:
        if keyword in text:
            technical_count += 1

    if technical_count >= 3:
        score += 10
    else:
        feedback.append(
            "Add more relevant technical skills and technologies."
        )


    # --------------------------------
    # Final Result
    # --------------------------------

    if not feedback:
        feedback.append(
            "Resume contains the main sections and basic ATS-friendly elements."
        )

    return {
        "quality_score": score,
        "word_count": word_count,
        "feedback": feedback
    }
def generate_resume_recommendations(
    resume_text,
    job_description,
    resume_skills,
    required_skills,
    missing_skills
):

    recommendations = []

    resume_text_lower = resume_text.lower()

    # 1. Missing skills
    if missing_skills:

        for skill in sorted(missing_skills):

            recommendations.append(
                "Consider adding " + skill +
                " to your resume if you have relevant experience."
            )

    # 2. Project experience
    if "project" not in resume_text_lower:

        recommendations.append(
            "Add a Projects section with relevant technical projects."
        )

    # 3. Experience
    if (
        "experience" not in resume_text_lower
        and "internship" not in resume_text_lower
    ):

        recommendations.append(
            "Add internship, training or relevant practical experience if available."
        )

    # 4. Action words
    action_words = [
        "developed",
        "implemented",
        "designed",
        "built",
        "created",
        "integrated",
        "optimized"
    ]

    has_action_word = False

    for word in action_words:

        if word in resume_text_lower:
            has_action_word = True
            break

    if not has_action_word:

        recommendations.append(
            "Use strong action words such as Developed, Implemented, Designed and Built."
        )

    # 5. Job-specific keywords
    if required_skills:

        matched_count = len(
            set(resume_skills).intersection(
                set(required_skills)
            )
        )

        if matched_count < len(required_skills):

            recommendations.append(
                "Tailor your resume to the job description by naturally including relevant skills you actually possess."
            )

    # 6. Resume length
    word_count = len(resume_text.split())

    if word_count < 250:

        recommendations.append(
            "Your resume appears short. Add relevant project, internship and technical details."
        )

    elif word_count > 1000:

        recommendations.append(
            "Your resume may be too long. Remove unnecessary information and keep the content concise."
        )

    # 7. Technical skills
    if len(resume_skills) < 5:

        recommendations.append(
            "Add more relevant technical skills that you genuinely know."
        )

    # 8. Default recommendation
    if not recommendations:

        recommendations.append(
            "Your resume is reasonably aligned with the job description. Continue tailoring project descriptions to the specific role."
        )

    return recommendations
def calculate_match(resume_skills, required_skills):

    resume_set = set(resume_skills)
    required_set = set(required_skills)

    matched_skills = resume_set.intersection(required_set)
    missing_skills = required_set.difference(resume_set)

    if len(required_set) == 0:
        score = 0
    else:
        score = (len(matched_skills) / len(required_set)) * 100

    return matched_skills, missing_skills, score
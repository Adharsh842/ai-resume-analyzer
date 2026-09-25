def generate_skill_gap(missing_skills):

    if not missing_skills:
        return ["No major skill gaps found."]

    suggestions = []

    skill_suggestions = {

        "docker":
            "Learn Docker basics and practice containerizing a Spring Boot application.",

        "aws":
            "Learn AWS fundamentals such as EC2, S3, IAM and basic cloud deployment.",

        "spring boot":
            "Improve Spring Boot knowledge by building REST APIs with Spring Data JPA.",

        "mysql":
            "Practice SQL queries, joins, indexes, constraints and database design.",

        "postgresql":
            "Practice PostgreSQL queries, relationships, indexes and database integration.",

        "mongodb":
            "Learn MongoDB CRUD operations, collections and integrating MongoDB with applications.",

        "react":
            "Practice React components, hooks, routing and REST API integration.",

        "javascript":
            "Strengthen JavaScript fundamentals including ES6, promises, async/await and DOM concepts.",

        "python":
            "Learn Python fundamentals and build small automation or data-processing projects.",

        "fastapi":
            "Learn FastAPI routing, request validation, Pydantic models and REST API development.",

        "machine learning":
            "Learn supervised learning, model training, feature engineering and model evaluation.",

        "natural language processing":
            "Learn NLP concepts such as tokenization, embeddings, text classification and transformers.",

        "nlp":
            "Learn NLP concepts such as tokenization, embeddings and text classification.",

        "llm":
            "Learn LLM fundamentals, prompt engineering, embeddings and retrieval-augmented generation.",

        "generative ai":
            "Learn Generative AI concepts and build applications using LLM APIs.",

        "rag":
            "Learn RAG architecture, document embeddings, vector databases and retrieval pipelines.",

        "prompt engineering":
            "Practice prompt engineering techniques for improving LLM responses.",

        "rest api":
            "Practice designing REST APIs using HTTP methods, status codes and JSON responses.",

        "git":
            "Practice Git commands, branching, merging and collaborative development workflows."
    }


    for skill in sorted(missing_skills):

        suggestion = skill_suggestions.get(
            skill,
            "Improve your knowledge of " + skill + " through practical projects."
        )

        suggestions.append(
            "Missing " + skill + ": " + suggestion
        )


    return suggestions
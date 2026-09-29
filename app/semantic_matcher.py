from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def calculate_semantic_match(resume_text, job_description):
    model = get_model()

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    score = float(similarity * 100)

    return score
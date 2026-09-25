from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

import tempfile
import os


# ==========================================
# IMPORT PROJECT MODULES
# ==========================================

from app.resume_parser import extract_text_from_pdf

from app.skill_extractor import (
    extract_skills,
    analyze_job_description
)

from app.matcher import calculate_match

from app.semantic_matcher import (
    calculate_semantic_match
)

from app.skill_gap import (
    generate_skill_gap
)

from app.ats_analyzer import (
    analyze_ats_keywords
)

from app.resume_quality import (
    calculate_resume_quality
)

from app.resume_recommender import (
    generate_resume_recommendations
)

from app.job_analyzer import (
    analyze_job_description_details
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="AI Resume Analyzer",
    description="AI-powered Resume Analyzer and Job Matcher API",
    version="1.0.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AI Resume Analyzer API is running"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ==========================================
# ANALYZE RESUME
# ==========================================

@app.post("/analyze")
async def analyze_resume(

    resume: UploadFile = File(...),

    job_description: str = Form(...)

):

    # ======================================
    # SAVE UPLOADED RESUME TEMPORARILY
    # ======================================

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        contents = await resume.read()

        temp_file.write(contents)

        temp_resume_path = temp_file.name


    try:

        # ==================================
        # EXTRACT RESUME TEXT
        # ==================================

        resume_text = extract_text_from_pdf(
            temp_resume_path
        )


        # ==================================
        # RESUME QUALITY ANALYSIS
        # ==================================

        resume_quality = calculate_resume_quality(
            resume_text
        )


        # ==================================
        # EXTRACT RESUME SKILLS
        # ==================================

        resume_skills = extract_skills(
            resume_text
        )


        # ==================================
        # EXTRACT REQUIRED JOB SKILLS
        # ==================================

        required_skills = analyze_job_description(
            job_description
        )


        # ==================================
        # JOB DESCRIPTION ANALYZER
        # ==================================

        job_analysis = analyze_job_description_details(
            job_description
        )


        # ==================================
        # KEYWORD MATCHING
        # ==================================

        (
            matched_skills,
            missing_skills,
            keyword_score
        ) = calculate_match(

            resume_skills,

            required_skills
        )


        # ==================================
        # SEMANTIC AI MATCHING
        # ==================================

        semantic_score = calculate_semantic_match(

            resume_text,

            job_description
        )


        # ==================================
        # ATS KEYWORD ANALYSIS
        # ==================================

        ats_analysis = analyze_ats_keywords(

            resume_text,

            job_description
        )


        ats_score = ats_analysis[
            "ats_score"
        ]


        # ==================================
        # OVERALL SCORE
        # ==================================

        overall_score = (

            keyword_score * 0.4

            + semantic_score * 0.4

            + ats_score * 0.2

        )


        # ==================================
        # SKILL GAP ANALYSIS
        # ==================================

        skill_gap_suggestions = generate_skill_gap(

            missing_skills
        )


        # ==================================
        # AI RESUME RECOMMENDATIONS
        # ==================================

        resume_recommendations = (
            generate_resume_recommendations(

                resume_text,

                job_description,

                resume_skills,

                required_skills,

                missing_skills

            )
        )


        # ==================================
        # FINAL RESPONSE
        # ==================================

        return {

            # --------------------------------
            # FILE INFORMATION
            # --------------------------------

            "filename": resume.filename,


            # --------------------------------
            # MATCH SCORES
            # --------------------------------

            "keyword_match_score": round(
                keyword_score,
                2
            ),

            "semantic_match_score": round(
                semantic_score,
                2
            ),

            "ats_score": round(
                ats_score,
                2
            ),

            "overall_match_score": round(
                overall_score,
                2
            ),


            # --------------------------------
            # RESUME QUALITY
            # --------------------------------

            "resume_quality": resume_quality,


            # --------------------------------
            # RESUME SKILLS
            # --------------------------------

            "resume_skills": resume_skills,


            # --------------------------------
            # REQUIRED SKILLS
            # --------------------------------

            "required_skills": required_skills,


            # --------------------------------
            # MATCHED SKILLS
            # --------------------------------

            "matched_skills": sorted(
                matched_skills
            ),


            # --------------------------------
            # MISSING SKILLS
            # --------------------------------

            "missing_skills": sorted(
                missing_skills
            ),


            # --------------------------------
            # SKILL GAP
            # --------------------------------

            "skill_gap_suggestions": (
                skill_gap_suggestions
            ),


            # --------------------------------
            # RESUME RECOMMENDATIONS
            # --------------------------------

            "resume_recommendations": (
                resume_recommendations
            ),


            # --------------------------------
            # ATS ANALYSIS
            # --------------------------------

            "ats_analysis": ats_analysis,


            # --------------------------------
            # JOB DESCRIPTION ANALYSIS
            # --------------------------------

            "job_analysis": job_analysis

        }


    finally:

        # ==================================
        # DELETE TEMPORARY FILE
        # ==================================

        if os.path.exists(
            temp_resume_path
        ):

            os.remove(
                temp_resume_path
            )
import os
import tempfile

import streamlit as st
import pandas as pd
import plotly.express as px

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIG
# ============================================================

from config import (
    EMBEDDING_MODEL
)


# ============================================================
# EXTRACTOR
# ============================================================

from extractor import (
    extract_pdf_text,
    extract_required_skills,
    extract_preferred_skills,
    extract_skills
)


# ============================================================
# MATCHER
# ============================================================

from matcher import (
    calculate_skill_scores,
    calculate_critical_skill_score,
    calculate_supporting_skill_score,
    calculate_semantic_similarity
)


# ============================================================
# SCORER
# ============================================================

from scorer import (
    calculate_experience_score,
    calculate_education_score,
    calculate_final_score,
    get_decision
)


# ============================================================
# LLM EXPLAINER
# ============================================================

from llm_explainer import (
    generate_llm_explanation
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "screening_results" not in st.session_state:

    st.session_state.screening_results = []


if "selected_candidate" not in st.session_state:

    st.session_state.selected_candidate = None


if "screened" not in st.session_state:

    st.session_state.screened = False


if "stored_jd" not in st.session_state:

    st.session_state.stored_jd = ""


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_model():

    return SentenceTransformer(
        EMBEDDING_MODEL
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "⚙️ Settings"
    )

    st.write(
        "Configure your resume screening process."
    )

    top_n = st.slider(
        "Number of candidates to display",
        min_value=3,
        max_value=20,
        value=5
    )

    st.divider()

    st.subheader(
        "📊 Scoring Weights"
    )

    st.write(
        "**Critical Skills:** 45%"
    )

    st.write(
        "**Supporting Skills:** 15%"
    )

    st.write(
        "**Semantic Similarity:** 15%"
    )

    st.write(
        "**Experience:** 15%"
    )

    st.write(
        "**Education:** 10%"
    )


# ============================================================
# TITLE
# ============================================================

st.title(
    "🤖 AI Resume Screening System"
)

st.markdown(
    "### Intelligent ATS Resume Ranking & Candidate Analysis"
)


# ============================================================
# FUNCTION:
# GENERATE LLM ANALYSIS
# ============================================================

def generate_candidate_ai_analysis(
    result,
    jd
):

    # --------------------------------------------------------
    # Already generated
    # --------------------------------------------------------

    existing = result.get(
        "llm_explanation"
    )

    if existing:

        return existing


    # --------------------------------------------------------
    # Resume text
    # --------------------------------------------------------

    resume_text = result.get(
        "resume_text",
        ""
    )


    if not resume_text:

        return {

            "summary":
                "Resume text is unavailable for AI analysis.",

            "strengths": [],

            "gaps": [],

            "recommendation":
                "Manual review recommended."
        }


    # --------------------------------------------------------
    # Generate LLM explanation
    # --------------------------------------------------------

    try:

        explanation = generate_llm_explanation(

            jd,

            result,

            resume_text
        )


        if not isinstance(
            explanation,
            dict
        ):

            explanation = {

                "summary":
                    str(explanation),

                "strengths": [],

                "gaps": [],

                "recommendation":
                    "Manual review recommended."
            }


        result[
            "llm_explanation"
        ] = explanation


        return explanation


    except Exception as error:

        return {

            "summary":
                "AI analysis could not be generated.",

            "strengths": [],

            "gaps": [

                f"LLM error: {error}"
            ],

            "recommendation":
                "Please review the candidate manually."
        }


# ============================================================
# FUNCTION:
# DISPLAY RANKING PAGE
# ============================================================

def show_candidate_ranking(
    results,
    top_n
):

    st.header(
        "🏆 Candidate Ranking"
    )

    st.caption(
        "Candidates are ranked by the final ATS score. "
        "Click a candidate to view complete analysis."
    )


    # ========================================================
    # CANDIDATE CARDS
    # ========================================================

    for rank, result in enumerate(
        results[:top_n],
        start=1
    ):

        st.divider()


        col1, col2, col3, col4 = st.columns(
            [0.7, 4.0, 1.5, 1.8]
        )


        # ----------------------------------------------------
        # Rank
        # ----------------------------------------------------

        with col1:

            if rank == 1:

                st.markdown(
                    "## 🥇"
                )

            elif rank == 2:

                st.markdown(
                    "## 🥈"
                )

            elif rank == 3:

                st.markdown(
                    "## 🥉"
                )

            else:

                st.markdown(
                    f"## #{rank}"
                )


        # ----------------------------------------------------
        # Candidate name
        # ----------------------------------------------------

        with col2:

            st.markdown(
                f"### {result['candidate']}"
            )

            st.write(
                f"**{result['decision']}**"
            )


        # ----------------------------------------------------
        # Score
        # ----------------------------------------------------

        with col3:

            st.metric(
                "ATS Score",
                f"{result['final_score']:.2f}%"
            )


        # ----------------------------------------------------
        # Details button
        # ----------------------------------------------------

        with col4:

            if st.button(
                "🔍 View Details",
                key=f"details_{rank}_{result['candidate']}",
                use_container_width=True
            ):

                st.session_state.selected_candidate = (
                    result["candidate"]
                )

                st.rerun()


# ============================================================
# FUNCTION:
# DISPLAY CANDIDATE DETAILS
# ============================================================

def show_candidate_details(
    result,
    jd
):

    # ========================================================
    # BACK BUTTON
    # ========================================================

    if st.button(
        "← Back to Candidates",
        type="secondary"
    ):

        st.session_state.selected_candidate = None

        st.rerun()


    st.divider()


    # ========================================================
    # CANDIDATE HEADER
    # ========================================================

    st.header(
        f"Rank {result['rank']}: "
        f"{result['candidate']}"
    )


    score_col1, score_col2 = st.columns(2)


    with score_col1:

        st.metric(
            "Final ATS Score",
            f"{result['final_score']:.2f}%"
        )


    with score_col2:

        st.metric(
            "Decision",
            result["decision"]
        )


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    st.subheader(
        "📊 Score Breakdown"
    )


    breakdown_df = pd.DataFrame({

        "Category": [

            "Critical Skills",

            "Supporting Skills",

            "Semantic",

            "Experience",

            "Education"
        ],

        "Score": [

            result[
                "critical_score"
            ],

            result[
                "supporting_score"
            ],

            result[
                "semantic_score"
            ],

            result[
                "experience_score"
            ],

            result[
                "education_score"
            ]
        ]
    })


    fig = px.bar(

        breakdown_df,

        x="Category",

        y="Score",

        text="Score",

        title="Candidate Score Breakdown"
    )


    fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside"
    )


    fig.update_yaxes(
        range=[
            0,
            100
        ]
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # SCORE CONTRIBUTION
    # ========================================================

    st.subheader(
        "🎯 Score Contribution"
    )


    contribution_df = pd.DataFrame({

        "Category": [

            "Critical Skills",

            "Supporting Skills",

            "Semantic",

            "Experience",

            "Education"
        ],

        "Contribution": [

            result[
                "critical_score"
            ] * 0.45,

            result[
                "supporting_score"
            ] * 0.15,

            result[
                "semantic_score"
            ] * 0.15,

            result[
                "experience_score"
            ] * 0.15,

            result[
                "education_score"
            ] * 0.10
        ]
    })


    fig2 = px.pie(

        contribution_df,

        names="Category",

        values="Contribution",

        title="Contribution to Final ATS Score"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # ========================================================
    # AI HIRING ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "🤖 AI Hiring Analysis"
    )


    # --------------------------------------------------------
    # Generate only for selected candidate
    # --------------------------------------------------------

    if not result.get(
        "llm_explanation"
    ):

        with st.spinner(
            "🤖 AI is analyzing this candidate..."
        ):

            explanation = (
                generate_candidate_ai_analysis(
                    result,
                    jd
                )
            )

    else:

        explanation = result[
            "llm_explanation"
        ]


    # ========================================================
    # SUMMARY
    # ========================================================

    st.subheader(
        "📝 Summary"
    )


    st.info(
        explanation.get(
            "summary",
            "No summary available."
        )
    )


    # ========================================================
    # STRENGTHS
    # ========================================================

    st.subheader(
        "✅ Strengths"
    )


    strengths = explanation.get(
        "strengths",
        []
    )


    if strengths:

        for strength in strengths:

            st.success(
                f"✓ {strength}"
            )

    else:

        st.write(
            "No strengths identified."
        )


    # ========================================================
    # GAPS
    # ========================================================

    st.subheader(
        "❌ Gaps"
    )


    gaps = explanation.get(
        "gaps",
        []
    )


    if gaps:

        for gap in gaps:

            st.error(
                f"• {gap}"
            )

    else:

        st.success(
            "No major gaps identified."
        )


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    st.subheader(
        "💡 Recommendation"
    )


    st.warning(
        explanation.get(
            "recommendation",
            "No recommendation available."
        )
    )


    # ========================================================
    # CRITICAL SKILLS
    # ========================================================

    st.divider()

    st.subheader(
        "🔥 Critical Skills"
    )


    critical_col1, critical_col2 = st.columns(2)


    with critical_col1:

        st.write(
            "**Matched Critical Skills**"
        )


        if result[
            "critical_matched"
        ]:

            for skill in result[
                "critical_matched"
            ]:

                st.success(
                    skill
                )

        else:

            st.info(
                "No critical skills matched."
            )


    with critical_col2:

        st.write(
            "**Missing Critical Skills**"
        )


        if result[
            "critical_missing"
        ]:

            for skill in result[
                "critical_missing"
            ]:

                st.error(
                    skill
                )

        else:

            st.success(
                "No critical skills missing."
            )


    # ========================================================
    # SUPPORTING SKILLS
    # ========================================================

    st.subheader(
        "🧩 Supporting Skills"
    )


    supporting_col1, supporting_col2 = st.columns(2)


    with supporting_col1:

        st.write(
            "**Matched Supporting Skills**"
        )


        if result[
            "supporting_required_matched"
        ]:

            for skill in result[
                "supporting_required_matched"
            ]:

                st.success(
                    skill
                )

        else:

            st.info(
                "No supporting skills matched."
            )


    with supporting_col2:

        st.write(
            "**Missing Supporting Skills**"
        )


        if result[
            "supporting_required_missing"
        ]:

            for skill in result[
                "supporting_required_missing"
            ]:

                st.warning(
                    skill
                )

        else:

            st.success(
                "No supporting skills missing."
            )


    # ========================================================
    # REQUIRED SKILLS
    # ========================================================

    st.subheader(
        "📌 Required Skills"
    )


    req_col1, req_col2 = st.columns(2)


    with req_col1:

        st.write(
            "**Matched**"
        )


        if result[
            "required_matched"
        ]:

            for skill in result[
                "required_matched"
            ]:

                st.success(
                    skill
                )

        else:

            st.info(
                "None"
            )


    with req_col2:

        st.write(
            "**Missing**"
        )


        if result[
            "required_missing"
        ]:

            for skill in result[
                "required_missing"
            ]:

                st.error(
                    skill
                )

        else:

            st.success(
                "None"
            )


    # ========================================================
    # PREFERRED SKILLS
    # ========================================================

    st.subheader(
        "⭐ Preferred Skills"
    )


    pref_col1, pref_col2 = st.columns(2)


    with pref_col1:

        st.write(
            "**Matched**"
        )


        if result[
            "preferred_matched"
        ]:

            for skill in result[
                "preferred_matched"
            ]:

                st.success(
                    skill
                )

        else:

            st.info(
                "None"
            )


    with pref_col2:

        st.write(
            "**Missing**"
        )


        if result[
            "preferred_missing"
        ]:

            for skill in result[
                "preferred_missing"
            ]:

                st.warning(
                    skill
                )

        else:

            st.success(
                "None"
            )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    st.subheader(
        "💼 Experience"
    )


    experience_col1, experience_col2 = st.columns(2)


    with experience_col1:

        st.metric(

            "Experience Score",

            f"{result['experience_score']:.2f}%"
        )


    with experience_col2:

        years = result[
            "experience_years"
        ]


        if years <= 0:

            experience_display = (
                "No experience"
            )

        elif years < 1:

            months = round(
                years * 12
            )

            experience_display = (
                f"{months} months"
            )

        else:

            experience_display = (
                f"{years:.2f} years"
            )


        st.metric(

            "Detected Experience",

            experience_display
        )


    # ========================================================
    # EDUCATION
    # ========================================================

    st.subheader(
        "🎓 Education"
    )


    if result[
        "education"
    ]:

        st.write(

            ", ".join(
                result[
                    "education"
                ]
            )
        )

    else:

        st.info(
            "Education not detected."
        )


    # ========================================================
    # RESUME TEXT
    # ========================================================

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text(
            result.get(
                "resume_text",
                "Resume text unavailable."
            )
        )


# ============================================================
# INPUT PAGE
# ============================================================

# ------------------------------------------------------------
# If candidate is NOT selected, show upload/screening page
# ------------------------------------------------------------

if (
    st.session_state.selected_candidate
    is None
):

    # ========================================================
    # JOB DESCRIPTION
    # ========================================================

    st.header(
        "📄 Job Description"
    )


    jd_input = st.text_area(

        "Paste Job Description",

        height=250,

        placeholder=
            "Paste the job description here..."
    )


    # ========================================================
    # RESUME UPLOAD
    # ========================================================

    st.header(
        "📁 Upload Resumes"
    )


    uploaded_files = st.file_uploader(

        "Upload candidate resumes",

        type=["pdf"],

        accept_multiple_files=True
    )


    # ========================================================
    # SCREEN BUTTON
    # ========================================================

    screen_button = st.button(

        "🚀 Screen Resumes",

        type="primary",

        use_container_width=True
    )


    # ========================================================
    # SCREENING
    # ========================================================

    if screen_button:

        # ====================================================
        # VALIDATION
        # ====================================================

        if not jd_input.strip():

            st.error(
                "Please enter a Job Description."
            )

            st.stop()


        if not uploaded_files:

            st.error(
                "Please upload at least one resume."
            )

            st.stop()


        # ====================================================
        # SAVE JD
        # ====================================================

        st.session_state.stored_jd = (
            jd_input
        )


        # ====================================================
        # LOAD MODEL
        # ====================================================

        with st.spinner(
            "Loading AI embedding model..."
        ):

            model = load_model()


        # ====================================================
        # EXTRACT JD REQUIREMENTS
        # ====================================================

        required_skills = (
            extract_required_skills(
                jd_input
            )
        )


        preferred_skills = (
            extract_preferred_skills(
                jd_input
            )
        )


        # ====================================================
        # DISPLAY REQUIREMENTS
        # ====================================================

        st.subheader(
            "🎯 Job Requirements"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                "**Required Skills**"
            )


            if required_skills:

                st.info(
                    ", ".join(
                        required_skills
                    )
                )

            else:

                st.write(
                    "None detected"
                )


        with col2:

            st.write(
                "**Preferred Skills**"
            )


            if preferred_skills:

                st.info(
                    ", ".join(
                        preferred_skills
                    )
                )

            else:

                st.write(
                    "None detected"
                )


        # ====================================================
        # PROCESSING
        # ====================================================

        results = []

        progress = st.progress(
            0
        )

        status_text = st.empty()


        # ====================================================
        # PROCESS EACH RESUME
        # ====================================================

        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            status_text.write(
                f"Processing: **{uploaded_file.name}**"
            )


            temp_path = None


            try:

                # ------------------------------------------------
                # Temporary PDF
                # ------------------------------------------------

                with tempfile.NamedTemporaryFile(

                    delete=False,

                    suffix=".pdf"

                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    temp_path = (
                        temp_file.name
                    )


                # ------------------------------------------------
                # Extract text
                # ------------------------------------------------

                resume_text = (
                    extract_pdf_text(
                        temp_path
                    )
                )


                if not resume_text.strip():

                    st.warning(
                        f"Could not extract text from "
                        f"{uploaded_file.name}"
                    )

                    continue


                # ------------------------------------------------
                # Skills
                # ------------------------------------------------

                resume_skills = (
                    extract_skills(
                        resume_text
                    )
                )


                # =================================================
                # BASIC SKILL SCORE
                # =================================================

                skill_result = (
                    calculate_skill_scores(

                        required_skills,

                        preferred_skills,

                        resume_skills
                    )
                )


                # =================================================
                # CRITICAL SKILLS
                # =================================================

                critical_result = (
                    calculate_critical_skill_score(

                        required_skills,

                        resume_skills
                    )
                )


                # =================================================
                # SUPPORTING SKILLS
                # =================================================

                supporting_result = (
                    calculate_supporting_skill_score(

                        required_skills,

                        preferred_skills,

                        resume_skills,

                        critical_result
                    )
                )


                # =================================================
                # SEMANTIC SIMILARITY
                # =================================================

                semantic_score = (
                    calculate_semantic_similarity(

                        model,

                        jd_input,

                        resume_text
                    )
                )


                # =================================================
                # EXPERIENCE
                # =================================================

                (
                    experience_score,
                    experience_years
                ) = calculate_experience_score(

                    resume_text,

                    jd_input
                )


                # =================================================
                # EDUCATION
                # =================================================

                (
                    education_score,
                    education
                ) = calculate_education_score(

                    resume_text,

                    jd_input
                )


                # =================================================
                # FINAL SCORE
                # =================================================

                final_score = (
                    calculate_final_score(

                        critical_skill_score=
                            critical_result[
                                "critical_score"
                            ],

                        supporting_skill_score=
                            supporting_result[
                                "supporting_score"
                            ],

                        semantic_score=
                            semantic_score,

                        education_score=
                            education_score,

                        experience_score=
                            experience_score
                    )
                )


                # =================================================
                # DECISION
                # =================================================

                decision = get_decision(
                    final_score
                )


                # =================================================
                # SAVE RESULT
                # =================================================

                results.append({

                    # ---------------------------------------------
                    # Candidate
                    # ---------------------------------------------

                    "candidate":
                        uploaded_file.name,


                    # ---------------------------------------------
                    # Resume text
                    # ---------------------------------------------

                    "resume_text":
                        resume_text,


                    # ---------------------------------------------
                    # Final
                    # ---------------------------------------------

                    "final_score":
                        float(
                            final_score
                        ),

                    "decision":
                        decision,


                    # ---------------------------------------------
                    # Critical
                    # ---------------------------------------------

                    "critical_score":
                        float(
                            round(
                                critical_result[
                                    "critical_score"
                                ],
                                2
                            )
                        ),

                    "critical_required":
                        critical_result[
                            "critical_required"
                        ],

                    "critical_matched":
                        critical_result[
                            "critical_matched"
                        ],

                    "critical_missing":
                        critical_result[
                            "critical_missing"
                        ],


                    # ---------------------------------------------
                    # Supporting
                    # ---------------------------------------------

                    "supporting_score":
                        float(
                            round(
                                supporting_result[
                                    "supporting_score"
                                ],
                                2
                            )
                        ),

                    "supporting_required":
                        supporting_result[
                            "supporting_required"
                        ],

                    "supporting_required_matched":
                        supporting_result[
                            "supporting_required_matched"
                        ],

                    "supporting_required_missing":
                        supporting_result[
                            "supporting_required_missing"
                        ],


                    # ---------------------------------------------
                    # Basic skill
                    # ---------------------------------------------

                    "skill_score":
                        float(
                            round(
                                skill_result[
                                    "skill_score"
                                ],
                                2
                            )
                        ),

                    "required_score":
                        float(
                            round(
                                skill_result[
                                    "required_score"
                                ],
                                2
                            )
                        ),

                    "preferred_score":
                        float(
                            round(
                                skill_result[
                                    "preferred_score"
                                ],
                                2
                            )
                        ),


                    # ---------------------------------------------
                    # Semantic
                    # ---------------------------------------------

                    "semantic_score":
                        float(
                            round(
                                semantic_score,
                                2
                            )
                        ),


                    # ---------------------------------------------
                    # Experience
                    # ---------------------------------------------

                    "experience_score":
                        float(
                            round(
                                experience_score,
                                2
                            )
                        ),

                    "experience_years":
                        float(
                            experience_years
                        ),


                    # ---------------------------------------------
                    # Education
                    # ---------------------------------------------

                    "education_score":
                        float(
                            round(
                                education_score,
                                2
                            )
                        ),

                    "education":
                        education,


                    # ---------------------------------------------
                    # Required
                    # ---------------------------------------------

                    "required_matched":
                        skill_result[
                            "required_matched"
                        ],

                    "required_missing":
                        skill_result[
                            "required_missing"
                        ],


                    # ---------------------------------------------
                    # Preferred
                    # ---------------------------------------------

                    "preferred_matched":
                        skill_result[
                            "preferred_matched"
                        ],

                    "preferred_missing":
                        skill_result[
                            "preferred_missing"
                        ],

                    # ---------------------------------------------
                    # LLM initially empty
                    # ---------------------------------------------

                    "llm_explanation":
                        None
                })


            except Exception as error:

                st.error(
                    f"Error processing "
                    f"{uploaded_file.name}: "
                    f"{error}"
                )


            finally:

                if (
                    temp_path
                    and
                    os.path.exists(
                        temp_path
                    )
                ):

                    os.unlink(
                        temp_path
                    )


            progress.progress(

                (index + 1)

                /

                len(uploaded_files)
            )


        status_text.empty()


        # ====================================================
        # CHECK RESULTS
        # ====================================================

        if not results:

            st.error(
                "No valid resumes could be processed."
            )

            st.stop()


        # ====================================================
        # SORT
        # ====================================================

        results.sort(

            key=lambda x:
                x["final_score"],

            reverse=True
        )


        # ====================================================
        # ADD RANK
        # ====================================================

        for rank, result in enumerate(

            results,

            start=1
        ):

            result[
                "rank"
            ] = rank


        # ====================================================
        # SAVE TO SESSION STATE
        # ====================================================

        st.session_state.screening_results = (
            results
        )

        st.session_state.screened = True


        # ====================================================
        # SUCCESS
        # ====================================================

        st.success(
            "✅ Resume screening completed successfully."
        )


        # ====================================================
        # RERUN TO SHOW RANKING
        # ====================================================

        st.rerun()


# ============================================================
# SHOW RESULTS AFTER SCREENING
# ============================================================

if (
    st.session_state.screened
    and
    st.session_state.screening_results
):

    results = (
        st.session_state.screening_results
    )


    # ========================================================
    # DETAIL PAGE
    # ========================================================

    if (
        st.session_state.selected_candidate
        is not None
    ):

        selected_candidate = (
            st.session_state.selected_candidate
        )


        selected_result = None


        for result in results:

            if (
                result["candidate"]
                ==
                selected_candidate
            ):

                selected_result = result

                break


        if selected_result is None:

            st.session_state.selected_candidate = None

            st.rerun()


        show_candidate_details(

            selected_result,

            st.session_state.stored_jd
        )


    # ========================================================
    # RANKING PAGE
    # ========================================================

    else:

        # ====================================================
        # DASHBOARD
        # ====================================================

        st.divider()

        st.header(
            "📊 Screening Dashboard"
        )


        strong = sum(

            r["decision"]
            == "Strong Match"

            for r in results
        )


        good = sum(

            r["decision"]
            == "Good Match"

            for r in results
        )


        moderate = sum(

            r["decision"]
            == "Moderate Match"

            for r in results
        )


        weak = sum(

            r["decision"]
            == "Weak Match"

            for r in results
        )


        c1, c2, c3, c4, c5 = st.columns(5)


        c1.metric(
            "👥 Candidates",
            len(results)
        )


        c2.metric(
            "🟢 Strong",
            strong
        )


        c3.metric(
            "🔵 Good",
            good
        )


        c4.metric(
            "🟡 Moderate",
            moderate
        )


        c5.metric(
            "🔴 Weak",
            weak
        )


        # ====================================================
        # RANKING
        # ====================================================

        show_candidate_ranking(

            results,

            top_n
        )


        # ====================================================
        # SCORE COMPARISON
        # ====================================================

        st.divider()

        st.header(
            "📈 Candidate Score Comparison"
        )


        chart_data = []


        for result in results[:top_n]:

            chart_data.append({

                "Candidate":
                    result[
                        "candidate"
                    ],

                "Score":
                    result[
                        "final_score"
                    ]
            })


        chart_df = pd.DataFrame(
            chart_data
        )


        fig = px.bar(

            chart_df,

            x="Candidate",

            y="Score",

            text="Score",

            title=
                "Top Candidate ATS Scores"
        )


        fig.update_traces(

            texttemplate=
                "%{text:.1f}%",

            textposition=
                "outside"
        )


        fig.update_layout(

            yaxis_title=
                "ATS Score (%)",

            xaxis_title=
                "Candidate",

            yaxis_range=[
                0,
                100
            ]
        )


        st.plotly_chart(

            fig,

            use_container_width=True
        )


        # ====================================================
        # DOWNLOAD CSV
        # ====================================================

        st.divider()


        st.subheader(
            "⬇️ Export Results"
        )


        # Don't expose full resume text or LLM object
        # unnecessarily in CSV.

        export_data = []


        for result in results:

            export_data.append({

                "Rank":
                    result[
                        "rank"
                    ],

                "Candidate":
                    result[
                        "candidate"
                    ],

                "Final Score":
                    result[
                        "final_score"
                    ],

                "Decision":
                    result[
                        "decision"
                    ],

                "Critical Skills":
                    result[
                        "critical_score"
                    ],

                "Supporting Skills":
                    result[
                        "supporting_score"
                    ],

                "Semantic":
                    result[
                        "semantic_score"
                    ],

                "Experience":
                    result[
                        "experience_score"
                    ],

                "Education":
                    result[
                        "education_score"
                    ],

                "Experience Years":
                    result[
                        "experience_years"
                    ]
            })


        output_df = pd.DataFrame(
            export_data
        )


        csv_data = (

            output_df

            .to_csv(
                index=False
            )

            .encode(
                "utf-8"
            )
        )


        st.download_button(

            "⬇️ Download Ranked Results CSV",

            data=csv_data,

            file_name=
                "ranked_candidates.csv",

            mime=
                "text/csv",

            use_container_width=True
        )
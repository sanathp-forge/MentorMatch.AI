"""
MentorMatch AI - Hackathon Prototype
"Find the right mentor. Build the right future."
AI-powered mentorship for every student's career journey.

Winning positioning:
"MentorMatch AI doesn't simply find a mentor. It understands where a student is,
where they want to go, what is stopping them, and who can help them get there."
"""

import os
import sys
import time
import textwrap
import pandas as pd
import streamlit as st
from datetime import datetime

# Version: 2026.10.08-v4-readiness-contrast-final
# Local imports
from utils.database import (
    init_db, load_table_as_df, save_dataframe_to_table,
    insert_session, insert_feedback, insert_mentor_request,
    get_notifications, add_notification
)
from utils.data_generator import generate_all_datasets
from ai.matcher import match_mentors_for_student
from ai.skill_gap import analyze_skill_gap
from ai.roadmap import generate_career_roadmap
from ai.llm import ask_career_coach, detect_active_llm_service
from ai.rag import generate_rag_response, retrieve_rag_context, answer_website_guide_query
from ai.embeddings import get_backend_info
from utils.helpers import (
    inject_custom_css, render_metric_card, render_hero_celebration_banner,
    render_pipeline_banner, render_html, render_brand_logo,
    create_skill_radar_chart, create_skill_gap_bar_chart,
    create_department_distribution_chart, create_career_goal_donut_chart,
    create_campus_skill_heatmap, verify_student_id_demo
)

# Page configuration
st.set_page_config(
    page_title="MentorMatch AI | AI Mentorship Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme State Initialization (Dark / Light Glass)
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

# Inject modern Glassmorphism & College themed CSS
inject_custom_css(theme=st.session_state.theme_mode)

# High-Performance In-Memory Data Initialization & Caching
@st.cache_data(show_spinner=False)
def load_and_initialize_system():
    init_db()
    students_df = load_table_as_df("students")
    mentors_df = load_table_as_df("mentors")
    sessions_df = load_table_as_df("sessions")
    feedback_df = load_table_as_df("feedback")
    skills_df = load_table_as_df("skills")

    if students_df.empty or mentors_df.empty or len(mentors_df) < 50:
        s, m, ses, f, sk = generate_all_datasets()
        save_dataframe_to_table(s, "students")
        save_dataframe_to_table(m, "mentors")
        save_dataframe_to_table(ses, "sessions")
        save_dataframe_to_table(f, "feedback")
        save_dataframe_to_table(sk, "skills")
        add_notification("STU001", "Request Accepted", "Aarav Mehta (Google) accepted your mentorship inquiry.", "Success")
        add_notification("STU001", "Session Reminder", "Upcoming session: 'Production ML Deployment' on Oct 12.", "Reminder")
        add_notification("STU001", "Skill Gap Alert", "AI engine identified Docker & AWS as priority bottlenecks.", "AI")
        return s, m, ses, f, sk

    return students_df, mentors_df, sessions_df, feedback_df, skills_df

# Cached AI Matcher for Sub-second Performance
@st.cache_data(show_spinner=False)
def get_cached_mentor_matches(student_dict_tuple: tuple, mentors_tuple: tuple, top_k: int = 3):
    s_dict = dict(student_dict_tuple)
    m_df = pd.DataFrame(list(mentors_tuple))
    return match_mentors_for_student(s_dict, m_df, top_k=top_k)

# Cached Skill Gap Analysis
@st.cache_data(show_spinner=False)
def get_cached_skill_gap(skills_str: str, target_role: str, exp_level: str):
    skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]
    return analyze_skill_gap(skills_list, target_role, exp_level)

# Load data once
students_df, mentors_df, sessions_df, feedback_df, skills_df = load_and_initialize_system()

# Session State Initialization
if "current_student_id" not in st.session_state:
    st.session_state.current_student_id = "STU001"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello Sanath! I am **MentorMate AI** with Campus RAG. I have reviewed your profile (5th Sem CSE, targeting AI Engineer) against our campus curriculum and mentor network. How can I guide your career today?"}
    ]

if "guide_chat_history" not in st.session_state:
    st.session_state.guide_chat_history = [
        {
            "role": "assistant",
            "content": "👋 **Hello! I'm your MentorMatch Website Guide.**\n\nAsk me anything about navigating this platform, finding mentors, career roadmaps, or booking sessions! You can also click any of the quick tour shortcuts below."
        }
    ]

if "match_results" not in st.session_state:
    st.session_state.match_results = None

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "🏠 Dashboard"

# Active Student Resolver
def get_current_student():
    s_rows = students_df[students_df["student_id"] == st.session_state.current_student_id]
    if not s_rows.empty:
        return s_rows.iloc[0].to_dict()
    return students_df.iloc[0].to_dict()

current_student = get_current_student()

# ==============================================================================
# SIDEBAR NAVIGATION & THEME CONTROLS
# ==============================================================================
with st.sidebar:
    render_brand_logo(theme=st.session_state.theme_mode)

    # 1-Click Hackathon Demo Mode
    if st.button("🎬 Launch 3-Min Hackathon Demo", type="primary", use_container_width=True):
        st.session_state.current_student_id = "STU001"
        st.session_state.nav_page = "🏠 Dashboard"
        st.toast("🚀 Demo Mode Primed: Student Sanath Sharma loaded with benchmark AI Engineering signals!", icon="✅")
        st.rerun()

    # Theme Toggle & Student Login Row
    t_col1, t_col2 = st.columns([1, 1])
    with t_col1:
        selected_theme = st.selectbox(
            "Theme",
            options=["🌙 Dark", "☀️ Light"],
            index=0 if st.session_state.theme_mode == "dark" else 1,
            label_visibility="collapsed"
        )
        new_theme = "dark" if selected_theme == "🌙 Dark" else "light"
        if new_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = new_theme
            st.rerun()
    with t_col2:
        if st.button("👤 Switch", use_container_width=True, help="Switch active student persona"):
            st.session_state.nav_page = "👤 User & Login"
            st.rerun()

    # Active Persona Glass Card
    with st.container(border=True):
        st.caption("ACTIVE STUDENT PERSONA")
        st.markdown(f"**{current_student['name']}**")
        st.caption(f"{current_student['department']} • Sem {current_student['semester']}")
        p_c1, p_c2 = st.columns(2)
        with p_c1:
            st.markdown(f"`CGPA {current_student['cgpa']}`")
        with p_c2:
            st.markdown(f"`{current_student['target_role']}`")

    # Main Navigation
    nav_options = [
        "🏠 Dashboard",
        "🎯 Find My Mentor",
        "🧠 AI Career Coach (RAG)",
        "🗺️ My Roadmap",
        "🔍 Skill Gap Analyzer",
        "👥 Mentors",
        "📊 Analytics",
        "📅 Sessions",
        "💡 AI Insights",
        "👤 User & Login",
        "📷 Campus Verification"
    ]

    selected_nav = st.radio(
        "Navigation",
        options=nav_options,
        index=nav_options.index(st.session_state.nav_page) if st.session_state.nav_page in nav_options else 0,
        label_visibility="collapsed"
    )
    if selected_nav != st.session_state.nav_page:
        st.session_state.nav_page = selected_nav
        st.rerun()

    st.markdown("<hr style='margin: 0.85rem 0; opacity: 0.2;' />", unsafe_allow_html=True)

    # System Architecture Telemetry
    llm_prov, llm_model = detect_active_llm_service()
    with st.container(border=True):
        st.caption("AI INTELLIGENCE STACK")
        st.markdown(f"• **LLM Coach**: {llm_prov}")
        st.markdown(f"• **RAG Retrieval**: Grounded Campus KB")
        st.markdown(f"• **Matching**: 7-Signal Vector Engine")

    # Notifications
    notifs = get_notifications(st.session_state.current_student_id)
    if notifs:
        with st.expander(f"🔔 Notifications ({len(notifs)})"):
            for n in notifs[:3]:
                st.markdown(f"**{n['title']}**: {n['message']}")


# ==============================================================================
# PAGE 1: 🏠 DASHBOARD
# ==============================================================================
if st.session_state.nav_page == "🏠 Dashboard":
    # College-Themed Animated Celebration Banner
    render_hero_celebration_banner(current_student['name'], current_student['career_readiness_score'])

    # Pipeline Flow Visualizer
    render_pipeline_banner()

    # Student Personalized Greeting & Readiness Callout
    col_greet, col_cta = st.columns([3, 1])
    with col_greet:
        st.subheader(f"Good afternoon, {current_student['name'].split()[0]} 👋")
        st.write(
            f"Your AI career readiness index is currently at **{current_student['career_readiness_score']}%**. "
            f"You have **1 scheduled session** upcoming this week with Aarav Mehta."
        )
    with col_cta:
        if st.button("🎯 Find My Mentor →", type="primary", use_container_width=True):
            st.session_state.nav_page = "🎯 Find My Mentor"
            st.rerun()

    # Squarespace Fluid Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Career Readiness", f"{current_student['career_readiness_score']}%", "+14% this semester", index="01")
    with m2:
        render_metric_card("Skill Benchmark", "74%", f"Target: {current_student['target_role']}", index="02")
    with m3:
        render_metric_card("Roadmap Status", "Phase 2", "42% completed", index="03")
    with m4:
        render_metric_card("Profile Strength", f"{current_student['resume_score']}%", "Verified for matching", index="04")

    st.write("")

    # 2-Column Core View: Skill Radar + AI Career Insight
    c_left, c_right = st.columns([1, 1])

    with c_left:
        with st.container(border=True):
            st.markdown('<span class="sqsp-eyebrow">01 / COMPETENCY MATRIX</span>', unsafe_allow_html=True)
            st.markdown("### Student Competency Radar")
            st.caption("Multi-axial evaluation across technical and communication competencies")
            radar_categories = ["Python", "AI/ML", "Cloud / AWS", "DSA", "Communication", "System Design"]
            radar_values = [85, 75, 40, 70, 78, 45]
            is_dark_active = (st.session_state.theme_mode == "dark")
            radar_fig = create_skill_radar_chart(radar_categories, radar_values, is_dark=is_dark_active)
            st.plotly_chart(radar_fig, use_container_width=True)

    with c_right:
        with st.container(border=True):
            st.markdown('<span class="sqsp-eyebrow">02 / AI STRATEGIC TRAJECTORY</span>', unsafe_allow_html=True)
            st.markdown("### Career Insight & Action Plan")
            st.info(f"**Strategic Trajectory:** Based on your profile telemetry, your highest-ROI path is **AI + Full Stack Engineering**.")
            
            st.markdown("##### Strengths Identified")
            st.markdown("Python • React • Machine Learning • FastAPI Microservices")

            st.markdown("##### High-Priority Gaps")
            st.markdown("Docker Containerization • Cloud Deployment (AWS) • MLOps • System Design")

            st.markdown("##### Recommended Next Action")
            st.markdown(
                "> **Connect with an AI/Cloud mentor** and complete a production-grade containerized AI deployment on AWS EC2."
            )

    # Quick Feature Links Row
    st.write("")
    st.markdown("#### Quick Actions & Workflows")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("🤖 Match with Best Mentor", use_container_width=True):
            st.session_state.nav_page = "🎯 Find My Mentor"
            st.rerun()
    with q2:
        if st.button("🗺️ View Personalized Roadmap", use_container_width=True):
            st.session_state.nav_page = "🗺️ My Roadmap"
            st.rerun()
    with q3:
        if st.button("🔍 Run Skill Gap Diagnostic", use_container_width=True):
            st.session_state.nav_page = "🔍 Skill Gap Analyzer"
            st.rerun()
    with q4:
        if st.button("🧠 Ask MentorMate AI (RAG)", use_container_width=True):
            st.session_state.nav_page = "🧠 AI Career Coach (RAG)"
            st.rerun()


# ==============================================================================
# PAGE 2: 🎯 FIND MY MENTOR (THE MOST IMPORTANT PAGE)
# ==============================================================================
elif st.session_state.nav_page == "🎯 Find My Mentor":
    st.title("🎯 Find My Mentor")
    st.caption("Powered by the **AI Mentorship Intelligence Engine**: Synthesizing 7 multidimensional signals into explainable recommendations.")

    # Form Container
    with st.expander("📝 Customize Matching Parameters & Signals", expanded=True):
        with st.form("mentor_match_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                f_goal = st.text_input("Career Goal", value=current_student.get("career_goal", "AI + Full Stack Engineer"))
                f_role = st.selectbox(
                    "Target Role",
                    options=["AI Engineer", "Data Scientist", "Full Stack Developer", "Cloud Engineer", "Cybersecurity Analyst", "Product Manager", "Software Engineer"],
                    index=0
                )
                f_exp = st.selectbox("Experience Level", options=["Beginner", "Intermediate", "Advanced"], index=1)
            with c2:
                f_curr_skills = st.text_area("Current Skills", value=current_student.get("skills", "Python, React, Node.js, Machine Learning, MongoDB, FastAPI"), height=68)
                f_want_learn = st.text_area("Skills You Want To Learn", value="Docker, AWS, MLOps, System Design, Kubernetes", height=68)
            with c3:
                f_avail = st.selectbox("Availability", options=["Weekends & Evenings", "High (3-4 hrs/week)", "Moderate (2 hrs/week)", "Evenings Only"], index=0)
                f_style = st.selectbox("Preferred Mentoring Style", options=["Hands-on Projects & Architecture Reviews", "Conceptual / Theory First", "Pair Programming", "Step-by-step Guidance"], index=0)
                f_comm = st.selectbox("Communication Preference", options=["Async & Weekly Sync", "Weekly Video Calls", "Chat & Code Reviews"], index=0)

            btn_match = st.form_submit_button("🤖 Find My Best Mentor", type="primary", use_container_width=True)

    # Sub-second Cached Matching
    if btn_match or st.session_state.match_results is None:
        student_query = {
            "career_goal": f_goal if 'f_goal' in locals() else current_student.get("career_goal"),
            "target_role": f_role if 'f_role' in locals() else current_student.get("target_role"),
            "skills": f_curr_skills if 'f_curr_skills' in locals() else current_student.get("skills"),
            "skills_to_learn": f_want_learn if 'f_want_learn' in locals() else "Docker, AWS, MLOps, System Design",
            "experience_level": f_exp if 'f_exp' in locals() else current_student.get("experience_level"),
            "preferred_learning_style": f_style if 'f_style' in locals() else current_student.get("preferred_learning_style"),
            "communication_preference": f_comm if 'f_comm' in locals() else current_student.get("communication_preference"),
            "availability": f_avail if 'f_avail' in locals() else current_student.get("availability")
        }
        st.session_state.match_results = get_cached_mentor_matches(
            tuple(sorted(student_query.items())),
            tuple(mentors_df.to_dict(orient="records")),
            top_k=3
        )

    st.subheader("🎯 Top Mentor Matches")
    matches = st.session_state.match_results or []
    
    for i, mentor in enumerate(matches, 1):
        score = mentor["match_score"]
        is_top = (i == 1)

        with st.container(border=True):
            col_avatar, col_info, col_score = st.columns([1, 4, 2])
            with col_avatar:
                st.markdown(f"""
                <div style="border: 1px solid rgba(128,128,128,0.25); border-radius: 14px; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800;">
                    {mentor['name'][0]}
                </div>
                <div style="font-size: 0.75rem; font-weight: 700; opacity: 0.8; margin-top: 0.35rem;">★ {mentor['rating']} / 5.0</div>
                """, unsafe_allow_html=True)
            with col_info:
                top_badge = "<span class='sqsp-tag' style='font-weight: 700;'>● #1 MATCH</span>" if is_top else ""
                st.markdown(f"### {mentor['name']} {top_badge}", unsafe_allow_html=True)
                st.markdown(f"<span class='sqsp-tag'>{mentor['company'].upper()}</span> <span style='font-weight: 600;'>{mentor['role']}</span>", unsafe_allow_html=True)
                st.caption(f"{mentor['experience_years']} yrs experience • {mentor['industry']} • {mentor['availability']}")
                st.write(f"**Skills**: `{mentor['skills']}`")
                st.caption(f"*{mentor['bio']}*")
            with col_score:
                st.markdown(f"""
                <div style="text-align: right; margin-bottom: 0.5rem;">
                    <span class="sqsp-eyebrow">COMPATIBILITY</span>
                    <div style="font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1;">{score}%</div>
                    <span style="font-size: 0.74rem; opacity: 0.7;">7-Signal Composite</span>
                </div>
                """, unsafe_allow_html=True)

            # Explainable AI (XAI) Breakdown Expander
            with st.expander(f"🔍 Explainable Compatibility Analysis ({score}% Breakdown)", expanded=is_top):
                col_why, col_bars = st.columns([1, 1])
                with col_why:
                    st.markdown('<span class="sqsp-eyebrow">01 / SIGNAL ANALYSIS</span>', unsafe_allow_html=True)
                    st.markdown("##### AI Alignment Drivers")
                    for b in mentor["why_bullets"]:
                        st.markdown(f"✓ **{b}**")
                    st.info(f"**Compatibility Summary:** {mentor['ai_summary']}")
                with col_bars:
                    st.markdown('<span class="sqsp-eyebrow">02 / SIGNAL WEIGHTS</span>', unsafe_allow_html=True)
                    st.markdown("##### Dimension Breakdown")
                    for signal_name, val in mentor["breakdown"].items():
                        st.write(f"**{signal_name}** ({val}%)")
                        st.progress(val / 100.0)

                st.markdown("---")
                st.markdown("##### ✉️ Automated Outreach Draft")
                user_msg = st.text_area(
                    "Personalized Mentorship Message (Editable)",
                    value=mentor["auto_request_draft"],
                    key=f"draft_{mentor['mentor_id']}",
                    height=80
                )
                if st.button(f"Request 1:1 Mentorship with {mentor['name'].split()[0]} →", key=f"btn_send_{mentor['mentor_id']}", type="primary"):
                    insert_mentor_request({
                        "student_id": current_student["student_id"],
                        "mentor_id": mentor["mentor_id"],
                        "status": "Pending",
                        "message": user_msg,
                        "target_role": current_student["target_role"]
                    })
                    add_notification(
                        current_student["student_id"],
                        "Request Sent",
                        f"Mentorship request submitted to {mentor['name']} ({mentor['company']}).",
                        "Success"
                    )
                    st.success(f"Mentorship Request Submitted to {mentor['name']} ✓")


# ==============================================================================
# PAGE 3: 🧠 AI CAREER COACH (RAG GROUNDED)
# ==============================================================================
elif st.session_state.nav_page == "🧠 AI Career Coach (RAG)":
    st.markdown('<span class="sqsp-eyebrow">RETRIEVAL-AUGMENTED GENERATION • CAMPUS KNOWLEDGE BASE</span>', unsafe_allow_html=True)
    st.markdown("## MentorMate AI Coach")
    st.caption("24/7 conversational career intelligence grounded in verified university curricula and mentor profiles.")

    # Status Bar
    llm_prov, llm_model = detect_active_llm_service()
    with st.container(border=True):
        st.markdown(f"● **Grounded Campus RAG Active** • 8 Institutional Documents Indexed • Engine: **{llm_prov}**")

    # Quick Inquiries
    st.caption("RECOMMENDED INQUIRIES:")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    suggested_clicked = None
    with q_col1:
        if st.button("How to become an AI Engineer? →", use_container_width=True):
            suggested_clicked = "How do I become an AI Engineer?"
    with q_col2:
        if st.button("What skills am I missing? →", use_container_width=True):
            suggested_clicked = "What skills am I missing?"
    with q_col3:
        if st.button("Which mentor should I choose? →", use_container_width=True):
            suggested_clicked = "Which mentor should I choose?"
    with q_col4:
        if st.button("What project should I build? →", use_container_width=True):
            suggested_clicked = "What project should I build?"

    # Chat Messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user"><span class="sqsp-eyebrow" style="margin-bottom: 0.25rem;">YOU</span>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai"><span class="sqsp-eyebrow" style="margin-bottom: 0.25rem;">MENTORMATE AI // GROUNDED RAG</span>{msg["content"]}</div>', unsafe_allow_html=True)

    # User Input
    user_prompt = st.chat_input("Ask anything about your roadmap, skill gaps, mentors, or internships...")
    active_prompt = suggested_clicked or user_prompt

    if active_prompt:
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})
        with st.spinner("MentorMate RAG Engine retrieving campus knowledge and synthesizing advice..."):
            ans, engine_used = ask_career_coach(active_prompt, current_student)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
        st.rerun()


# ==============================================================================
# PAGE 4: 🗺️ MY ROADMAP
# ==============================================================================
elif st.session_state.nav_page == "🗺️ My Roadmap":
    st.markdown('<span class="sqsp-eyebrow">CAREER MILESTONE ARCHITECTURE</span>', unsafe_allow_html=True)
    st.markdown("## Progressive Career Roadmap")
    st.caption(f"A structured 4-phase trajectory engineered for **{current_student['target_role']}** market readiness.")

    roadmap = generate_career_roadmap(current_student["target_role"], current_student["skills"].split(","))

    for idx, phase in enumerate(roadmap, 1):
        pct = phase["completion_pct"]
        is_done = (pct == 100)
        badge_text = "● COMPLETED" if is_done else (f"● IN PROGRESS ({pct}%)" if pct > 0 else "● UPCOMING")

        with st.container(border=True):
            r_top1, r_top2 = st.columns([3, 1])
            with r_top1:
                st.markdown(f'<span class="sqsp-eyebrow">PHASE 0{idx} // {phase["duration_weeks"]} WEEKS</span>', unsafe_allow_html=True)
                st.markdown(f"### {phase['phase_name']}")
                st.caption(f"Status: {badge_text}")
            with r_top2:
                st.markdown(f"""
                <div style="text-align: right;">
                    <span class="sqsp-eyebrow">COMPLETION</span>
                    <div style="font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800;">{pct}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.progress(pct / 100.0)
            st.write(f"**Target Skills**: `{', '.join(phase['skills'])}`")
            
            col_res, col_topic, col_proj = st.columns(3)
            with col_res:
                st.markdown("**📚 Resources**")
                st.caption(phase['recommended_resources'])
            with col_topic:
                st.markdown("**💬 Mentor Discussion**")
                st.caption(phase['mentor_discussion_topic'])
            with col_proj:
                st.markdown("**🛠️ Capstone Showcase**")
                st.caption(f"**{phase['capstone_project']}**")


# ==============================================================================
# PAGE 5: 🔍 SKILL GAP ANALYZER
# ==============================================================================
elif st.session_state.nav_page == "🔍 Skill Gap Analyzer":
    st.title("🔍 AI Skill Gap Analysis")
    st.caption("Comparative benchmarking of existing proficiencies against target industry standards.")

    gap_analysis = get_cached_skill_gap(
        current_student["skills"],
        current_student["target_role"],
        current_student["experience_level"]
    )

    st.warning(f"⚡ **AI Critical Bottleneck**: {gap_analysis['ai_recommendation']}")

    col_chart, col_table = st.columns([1, 1])
    with col_chart:
        st.subheader("📊 Proficiency Benchmark Visualizer")
        is_dark_active = (st.session_state.theme_mode == "dark")
        bar_fig = create_skill_gap_bar_chart(gap_analysis["gap_table"], is_dark=is_dark_active)
        st.plotly_chart(bar_fig, use_container_width=True)

    with col_table:
        st.subheader("📋 Detailed Skill Differential")
        df_gap = pd.DataFrame(gap_analysis["gap_table"])
        df_gap.columns = ["Skill", "Current", "Target", "Net Gap", "Status"]
        st.dataframe(df_gap, use_container_width=True, hide_index=True)


# ==============================================================================
# PAGE 6: 👥 MENTORS DIRECTORY
# ==============================================================================
elif st.session_state.nav_page == "👥 Mentors":
    st.title("👥 University Mentor Directory")
    st.caption("Explore 60+ verified alumni, industry leaders, professors, and teaching fellows.")

    c_srch, c_ind = st.columns([2, 1])
    with c_srch:
        search_query = st.text_input("🔍 Search mentors by name, role, skill or company", value="")
    with c_ind:
        industries = ["All Industries"] + sorted(mentors_df["industry"].unique().tolist())
        sel_industry = st.selectbox("Industry", options=industries)

    filtered_mentors = mentors_df.copy()
    if search_query:
        q_l = search_query.lower()
        filtered_mentors = filtered_mentors[
            filtered_mentors["name"].str.lower().str.contains(q_l) |
            filtered_mentors["role"].str.lower().str.contains(q_l) |
            filtered_mentors["skills"].str.lower().str.contains(q_l) |
            filtered_mentors["company"].str.lower().str.contains(q_l)
        ]
    if sel_industry != "All Industries":
        filtered_mentors = filtered_mentors[filtered_mentors["industry"] == sel_industry]

    st.write(f"Showing **{len(filtered_mentors)}** mentors")

    cols = st.columns(2)
    for idx, (_, m) in enumerate(filtered_mentors.head(12).iterrows()):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### {m['name']} ⭐ {m['rating']}")
                st.markdown(f"**{m['role']}** @ **{m['company']}**")
                st.caption(f"{m['experience_years']} yrs experience • {m['industry']}")
                st.write(f"`{m['skills']}`")
                st.caption(f"{str(m['bio'])[:120]}...")


# ==============================================================================
# PAGE 7: 📊 UNIVERSITY ANALYTICS
# ==============================================================================
elif st.session_state.nav_page == "📊 Analytics":
    st.markdown('<span class="sqsp-eyebrow">CAMPUS-WIDE TELEMETRY & TALENT DEMAND</span>', unsafe_allow_html=True)
    st.markdown("## University Mentorship Intelligence")
    st.caption("Institutional metrics, department talent distributions, and skill demand patterns across campus.")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_metric_card("Total Students", f"{len(students_df)}+", "Active in network", index="01")
    with k2:
        render_metric_card("Active Mentors", f"{len(mentors_df)}+", "Alumni & Industry", index="02")
    with k3:
        render_metric_card("Mentorship Sessions", f"{len(sessions_df)}+", "Completed & Scheduled", index="03")
    with k4:
        render_metric_card("Avg Compatibility", "87%", "Satisfaction: 92%", index="04")

    st.write("")
    is_dark_active = (st.session_state.theme_mode == "dark")
    c_g1, c_g2 = st.columns([1, 1])
    with c_g1:
        st.markdown('<span class="sqsp-eyebrow">01 / ENROLLMENT BY DEPARTMENT</span>', unsafe_allow_html=True)
        st.markdown("### Department Distribution")
        dept_fig = create_department_distribution_chart(students_df, is_dark=is_dark_active)
        st.plotly_chart(dept_fig, use_container_width=True)
    with c_g2:
        st.markdown('<span class="sqsp-eyebrow">02 / CAREER OBJECTIVES</span>', unsafe_allow_html=True)
        st.markdown("### Target Career Roles")
        donut_fig = create_career_goal_donut_chart(students_df, is_dark=is_dark_active)
        st.plotly_chart(donut_fig, use_container_width=True)

    st.markdown('<span class="sqsp-eyebrow">03 / SKILL HEATMAP MATRIX</span>', unsafe_allow_html=True)
    st.markdown("### Campus Skill Demand Heatmap")
    heatmap_fig = create_campus_skill_heatmap(students_df, is_dark=is_dark_active)
    st.plotly_chart(heatmap_fig, use_container_width=True)


# ==============================================================================
# PAGE 8: 💡 AI INSIGHTS
# ==============================================================================
elif st.session_state.nav_page == "💡 AI Insights":
    st.markdown('<span class="sqsp-eyebrow">INSTITUTIONAL INTELLIGENCE PATTERNS</span>', unsafe_allow_html=True)
    st.markdown("## AI-Powered Campus Insights")
    st.caption("Algorithmic patterns synthesized from 320+ students, 540+ sessions, and feedback telemetry.")

    insights = [
        ("01", "AI/ML represents the fastest-growing mentorship demand this term", "Over 44% of new student registrations identify AI Engineer or Data Scientist as their primary career objective.", "Onboard 15 additional industry cloud & MLOps mentors."),
        ("02", "38% of students targeting AI lack cloud deployment proficiency", "Cross-sectional analysis reveals solid Python fundamentals but critical deficits in Docker and AWS.", "Host mandatory 'Cloud Deployment for AI' workshops."),
        ("03", "Students with 3+ sessions demonstrated +24% higher skill mastery", "Post-session longitudinal confidence metrics indicate strong statistical correlation with placement success.", "Implement a 3-session milestone graduation badge."),
        ("04", "Computer Science students show high technical confidence but lower behavioral readiness", "Mock interview metrics average only 52% communication readiness among 5th/6th semester candidates.", "Mandate behavioral mock interviews with alumni leaders.")
    ]

    for num, title, body, action in insights:
        with st.container(border=True):
            st.markdown(f'<span class="sqsp-eyebrow">INSIGHT {num} // TREND ANALYSIS</span>', unsafe_allow_html=True)
            st.markdown(f"#### {title}")
            st.write(body)
            st.info(f"**Actionable Institutional Policy:** {action}")


# ==============================================================================
# PAGE 9: 📅 SESSIONS & FEEDBACK
# ==============================================================================
elif st.session_state.nav_page == "📅 Sessions":
    st.title("📅 Mentorship Sessions & Feedback")
    st.caption("Manage scheduled sessions, track milestones, and trigger automated AI follow-ups.")

    tab_sched, tab_book, tab_feed = st.tabs(["Upcoming & Past Sessions", "Schedule New Session", "Post-Session Feedback"])

    with tab_sched:
        my_sessions = sessions_df[sessions_df["student_id"] == current_student["student_id"]]
        if my_sessions.empty:
            st.info("No recorded sessions for this student. Use the Schedule tab to book one!")
        else:
            for _, s_row in my_sessions.iterrows():
                m_info = mentors_df[mentors_df["mentor_id"] == s_row["mentor_id"]]
                m_name = m_info.iloc[0]["name"] if not m_info.empty else "Mentor"
                with st.container(border=True):
                    st.markdown(f"#### {s_row['topic']} • `{s_row['status']}`")
                    st.write(f"With **{m_name}** • Date: {s_row['date']} • Duration: {s_row['duration']} min")

    with tab_book:
        with st.form("book_session_form"):
            b_mentor = st.selectbox("Select Mentor", options=mentors_df["name"].tolist())
            b_date = st.date_input("Date", value=datetime.today())
            b_topic = st.selectbox("Topic", options=["AI Career Roadmap Assessment", "Production ML Pipeline on AWS", "System Design: Microservices", "Mock Technical Coding Interview"])
            if st.form_submit_button("Confirm Booking", type="primary"):
                chosen_m_id = mentors_df[mentors_df["name"] == b_mentor].iloc[0]["mentor_id"]
                new_s_id = f"SES{len(sessions_df)+1:03d}"
                insert_session({
                    "session_id": new_s_id,
                    "student_id": current_student["student_id"],
                    "mentor_id": chosen_m_id,
                    "date": str(b_date),
                    "topic": b_topic,
                    "duration": 45,
                    "status": "Scheduled"
                })
                st.success(f"Session booked successfully with {b_mentor} for {b_date} ✓")

    with tab_feed:
        with st.form("feedback_form"):
            fb_mentor = st.selectbox("Completed Session with", options=mentors_df["name"].tolist()[:5])
            fb_rating = st.slider("Session Rating", min_value=1.0, max_value=5.0, value=5.0, step=0.5)
            fb_learn = st.text_area("Primary Takeaway", value="Learned the importance of containerizing FastAPI endpoints with Docker before AWS EC2 deployment.")
            c_bef, c_aft = st.columns(2)
            with c_bef:
                c_before = st.slider("Confidence Before (0-100)", 0, 100, 50)
            with c_aft:
                c_after = st.slider("Confidence After (0-100)", 0, 100, 85)

            if st.form_submit_button("Submit Feedback & Generate AI Follow-Up", type="primary"):
                chosen_m_id = mentors_df[mentors_df["name"] == fb_mentor].iloc[0]["mentor_id"]
                insert_feedback({
                    "student_id": current_student["student_id"],
                    "mentor_id": chosen_m_id,
                    "rating": fb_rating,
                    "feedback": fb_learn,
                    "skills_improved": "Docker, FastAPI",
                    "confidence_before": c_before,
                    "confidence_after": c_after
                })
                st.success("Feedback recorded! AI Follow-Up Action Plan Generated:")
                st.info("✓ Complete Docker basics • ✓ Package FastAPI endpoint • ✓ Read AWS guide • ✓ Schedule follow-up in 14 days.")


# ==============================================================================
# PAGE 10: 👤 USER REGISTRATION & LOGIN
# ==============================================================================
elif st.session_state.nav_page == "👤 User & Login":
    st.title("👤 Student Profile & Account Center")
    st.caption("Switch between registered campus students or register a brand new student profile.")

    tab_switch, tab_new = st.tabs(["Switch / Login Existing Student", "Register New Student"])

    with tab_switch:
        with st.container(border=True):
            st.subheader("Login as Registered Student")
            student_options = students_df[["student_id", "name", "target_role"]].apply(
                lambda r: f"{r['student_id']} - {r['name']} ({r['target_role']})", axis=1
            ).tolist()
            
            sel_student_str = st.selectbox("Select Student Profile", options=student_options, index=0)
            if st.button("Log In as Selected Student", type="primary"):
                sel_id = sel_student_str.split(" - ")[0]
                st.session_state.current_student_id = sel_id
                st.session_state.match_results = None
                st.toast(f"Logged in as {sel_student_str.split(' - ')[1]}! Dashboard updated.", icon="✅")
                st.rerun()

    with tab_new:
        with st.container(border=True):
            st.subheader("Register New Student Profile")
            with st.form("new_student_form"):
                n_col1, n_col2 = st.columns(2)
                with n_col1:
                    new_name = st.text_input("Full Name", value="")
                    new_dept = st.selectbox("Department", options=["Computer Science Engineering", "Information Technology", "AI & Data Science", "Electronics & Comm"])
                    new_sem = st.slider("Semester", 1, 8, 5)
                    new_cgpa = st.number_input("CGPA", min_value=5.0, max_value=10.0, value=8.2, step=0.1)
                with n_col2:
                    new_target = st.selectbox("Target Role", options=["AI Engineer", "Data Scientist", "Full Stack Developer", "Cloud Engineer", "Cybersecurity Analyst", "Product Manager"])
                    new_skills = st.text_input("Skills (comma separated)", value="Python, SQL, React")
                    new_interests = st.text_input("Interests", value="Generative AI, Web Development")
                    new_exp = st.selectbox("Experience Level", options=["Beginner", "Intermediate", "Advanced"])
                
                new_bio = st.text_area("Short Bio", value="Engineering student aiming to bridge classroom theory with industry mentorship.")

                if st.form_submit_button("Register & Log In Immediately", type="primary"):
                    if not new_name.strip():
                        st.error("Please enter a valid student name.")
                    else:
                        new_stu_id = f"STU{len(students_df) + 1:03d}"
                        new_student_record = {
                            "student_id": new_stu_id,
                            "name": new_name,
                            "age": 21,
                            "gender": "Other",
                            "department": new_dept,
                            "semester": new_sem,
                            "cgpa": new_cgpa,
                            "skills": new_skills,
                            "interests": new_interests,
                            "career_goal": f"{new_target} Specialist",
                            "target_role": new_target,
                            "experience_level": new_exp,
                            "projects": f"{new_skills.split(',')[0]} Showcase Project",
                            "preferred_learning_style": "Hands-on Projects",
                            "communication_preference": "Async & Weekly Sync",
                            "availability": "High (3-4 hrs/week)",
                            "career_readiness_score": 65,
                            "resume_score": 75,
                            "confidence_score": 70,
                            "location": "Campus North",
                            "bio": new_bio
                        }
                        # Save to database
                        students_df_updated = pd.concat([students_df, pd.DataFrame([new_student_record])], ignore_index=True)
                        save_dataframe_to_table(students_df_updated, "students")
                        st.session_state.current_student_id = new_stu_id
                        st.session_state.match_results = None
                        st.cache_data.clear()
                        st.success(f"Profile registered successfully! Logged in as {new_name} ({new_stu_id}) ✓")
                        time.sleep(1)
                        st.rerun()


# ==============================================================================
# PAGE 11: 📷 CAMPUS VERIFICATION DEMO
# ==============================================================================
elif st.session_state.nav_page == "📷 Campus Verification":
    st.title("📷 Campus ID & Face Verification")
    st.caption("Demonstrates biometric verification of student identity before alumni mentorship.")

    col_up, col_res = st.columns([1, 1])
    with col_up:
        uploaded_id = st.file_uploader("Upload Student ID Photo", type=["jpg", "jpeg", "png"])
        run_verify = st.button("Run Verification Check", type="primary")

    with col_res:
        if run_verify or uploaded_id is not None:
            raw_bytes = uploaded_id.read() if uploaded_id else None
            v_res = verify_student_id_demo(raw_bytes)
            st.success(f"✓ {v_res['message']}")
            st.info(f"**Confidence**: {v_res['confidence']}% • **Method**: {v_res['method']}")

# Global Footer
st.markdown("""
<div style="text-align: center; opacity: 0.6; font-size: 0.8rem; margin: 3rem 0 1rem 0; padding-top: 1rem;">
    MentorMatch AI • "Find the right mentor. Build the right future." • Campus Mentorship Intelligence
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# FLOATING BOTTOM-RIGHT WEBSITE GUIDE CHATBOT
# ==============================================================================
with st.container():
    st.markdown('<div id="corner-guide-bot-anchor"></div>', unsafe_allow_html=True)
    with st.popover("🤖", help="MentorGuide AI • Interactive Website Assistant"):
        st.markdown('<span class="sqsp-eyebrow">INTERACTIVE PLATFORM ASSISTANT</span>', unsafe_allow_html=True)
        st.markdown("### 🤖 MentorGuide AI")
        st.caption("Ask anything about navigating the platform, finding mentors, or exploring features.")

        # Quick Navigation Jump Pills
        st.markdown("**Quick Shortcuts:**")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            if st.button("🎯 Mentors", key="g_nav_m", use_container_width=True):
                st.session_state.nav_page = "🎯 Find My Mentor"
                st.rerun()
        with sc2:
            if st.button("🗺️ Roadmap", key="g_nav_r", use_container_width=True):
                st.session_state.nav_page = "🗺️ My Roadmap"
                st.rerun()
        with sc3:
            if st.button("🔍 Gaps", key="g_nav_g", use_container_width=True):
                st.session_state.nav_page = "🔍 Skill Gap Analyzer"
                st.rerun()

        sc4, sc5 = st.columns(2)
        with sc4:
            if st.button("📅 Book Session", key="g_nav_s", use_container_width=True):
                st.session_state.nav_page = "📅 Sessions"
                st.rerun()
        with sc5:
            if st.button("👤 Switch User", key="g_nav_u", use_container_width=True):
                st.session_state.nav_page = "👤 User & Login"
                st.rerun()

        st.markdown("<hr style='margin: 0.65rem 0; opacity: 0.2;' />", unsafe_allow_html=True)

        # Chat conversation messages
        for idx, g_msg in enumerate(st.session_state.guide_chat_history[-4:]):
            if g_msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-bubble-user" style="padding: 0.6rem 0.85rem; font-size: 0.86rem; margin-bottom: 0.5rem;">'
                    f'<span class="sqsp-eyebrow" style="margin-bottom: 0.15rem; font-size: 0.65rem;">YOU</span>'
                    f'{g_msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-bubble-ai" style="padding: 0.75rem 0.95rem; font-size: 0.86rem; margin-bottom: 0.5rem;">'
                    f'<span class="sqsp-eyebrow" style="margin-bottom: 0.15rem; font-size: 0.65rem;">GUIDE BOT</span>'
                    f'{g_msg["content"]}</div>',
                    unsafe_allow_html=True
                )
                if g_msg.get("target_page") and g_msg.get("button_label"):
                    if st.button(g_msg["button_label"], key=f"guide_jump_{idx}", type="primary", use_container_width=True):
                        st.session_state.nav_page = g_msg["target_page"]
                        st.rerun()

        # Input form
        with st.form("guide_chat_form", clear_on_submit=True):
            guide_input = st.text_input("Ask how to use the website:", placeholder="e.g. How do I match with Aarav Mehta?", label_visibility="collapsed")
            f_col1, f_col2 = st.columns([2, 1])
            with f_col1:
                submitted = st.form_submit_button("Ask Guide →", type="primary", use_container_width=True)
            with f_col2:
                tour_submitted = st.form_submit_button("Tour 🧭", use_container_width=True)

            if tour_submitted:
                guide_input = "Give me a quick tour of what this website can do"
                submitted = True

            if submitted and guide_input:
                st.session_state.guide_chat_history.append({"role": "user", "content": guide_input})
                res = answer_website_guide_query(guide_input, current_student)
                st.session_state.guide_chat_history.append({
                    "role": "assistant",
                    "content": res["answer"],
                    "target_page": res.get("target_page"),
                    "button_label": res.get("button_label")
                })
                st.rerun()

        if len(st.session_state.guide_chat_history) > 1:
            if st.button("Reset Guide Chat", key="btn_reset_guide", use_container_width=True):
                st.session_state.guide_chat_history = [
                    {
                        "role": "assistant",
                        "content": "👋 **Hello! I'm your MentorMatch Website Guide.**\n\nAsk me anything about navigating this platform, finding mentors, career roadmaps, or booking sessions! You can also click any of the quick tour shortcuts below."
                    }
                ]
                st.rerun()


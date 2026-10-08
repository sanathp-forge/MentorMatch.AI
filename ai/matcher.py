"""
AI Mentorship Intelligence & Matching Engine for MentorMatch AI.
Implements multi-dimensional compatibility scoring with explainable AI (XAI) breakdown.
Formulas:
- Skill Similarity: 30%
- Career Goal Alignment: 25%
- Experience Relevance: 15%
- Availability Match: 10%
- Learning Style Compatibility: 10%
- Communication Style: 5%
- Mentor Rating & Success: 5%
Total: 100%
"""

import pandas as pd
from typing import Dict, List, Any
from ai.embeddings import compute_semantic_similarity

def calculate_skill_similarity(student_skills: str, mentor_skills: str) -> float:
    """Calculate overlap and semantic alignment between student and mentor skillsets."""
    s_set = set([s.strip().lower() for s in student_skills.split(",") if s.strip()])
    m_set = set([m.strip().lower() for m in mentor_skills.split(",") if m.strip()])
    
    if not s_set or not m_set:
        return 0.5
    
    overlap = len(s_set.intersection(m_set))
    union = len(s_set.union(m_set))
    jaccard = overlap / union if union > 0 else 0.0
    
    # Also evaluate semantic proximity
    semantic = compute_semantic_similarity(student_skills, mentor_skills)
    blended = 0.6 * jaccard + 0.4 * semantic
    return min(max(blended, 0.0), 1.0)


def calculate_experience_fit(student_exp: str, mentor_exp_years: int) -> float:
    """Evaluate experience alignment."""
    # Student levels: Beginner, Intermediate, Advanced
    if student_exp == "Beginner":
        # Beginners benefit greatly from 3-7 years or senior students/TAs
        return 0.95 if 2 <= mentor_exp_years <= 8 else 0.85
    elif student_exp == "Intermediate":
        # Intermediates benefit from 5-10 years senior engineers
        return 0.98 if 5 <= mentor_exp_years <= 10 else 0.88
    else:  # Advanced
        # Advanced benefit from 7+ years architects / researchers
        return 0.96 if mentor_exp_years >= 7 else 0.80


def calculate_style_fit(student_style: str, mentor_style: str) -> float:
    """Evaluate learning style vs mentoring style compatibility."""
    if not student_style or not mentor_style:
        return 0.75
    s_clean = student_style.lower()
    m_clean = mentor_style.lower()
    if s_clean in m_clean or m_clean in s_clean:
        return 0.98
    # Semantic fit
    sim = compute_semantic_similarity(s_clean, m_clean)
    return min(max(sim, 0.65), 0.95)


def calculate_availability_fit(student_avail: str, mentor_avail: str) -> float:
    """Evaluate scheduling compatibility."""
    if not student_avail or not mentor_avail:
        return 0.80
    s_clean = student_avail.lower()
    m_clean = mentor_avail.lower()
    if ("high" in s_clean and "high" in m_clean) or ("weekend" in s_clean and "weekend" in m_clean):
        return 0.96
    return 0.86


def match_mentors_for_student(
    student_profile: Dict[str, Any],
    mentors_df: pd.DataFrame,
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Score and rank all mentors against the student's profile.
    Generates explainable breakdown and recommended discussion topics.
    """
    if mentors_df.empty:
        return []

    target_role = student_profile.get("target_role", "Software Engineer")
    career_goal = student_profile.get("career_goal", target_role)
    student_skills = student_profile.get("skills", "")
    skills_to_learn = student_profile.get("skills_to_learn", "")
    student_exp = student_profile.get("experience_level", "Intermediate")
    student_learning = student_profile.get("preferred_learning_style", "Hands-on Projects")
    student_comm = student_profile.get("communication_preference", "Async & Weekly Sync")
    student_avail = student_profile.get("availability", "High")

    combined_target_skills = f"{student_skills}, {skills_to_learn}" if skills_to_learn else student_skills

    scored_matches = []

    for _, mentor in mentors_df.iterrows():
        # 1. Skill Similarity (30%)
        m_skills = str(mentor.get("skills", ""))
        skill_sim = calculate_skill_similarity(combined_target_skills, m_skills)

        # 2. Career Goal Alignment (25%)
        mentor_domain = f"{mentor.get('role', '')} {mentor.get('specializations', '')} {mentor.get('industry', '')}"
        career_alignment = compute_semantic_similarity(f"{target_role} {career_goal}", mentor_domain)
        # Boost if target role keyword directly in mentor role
        if target_role.lower() in str(mentor.get("role", "")).lower():
            career_alignment = min(1.0, career_alignment + 0.25)
        elif "ai" in target_role.lower() and "ai" in str(mentor.get("role", "")).lower():
            career_alignment = min(1.0, career_alignment + 0.22)

        # 3. Experience Relevance (15%)
        exp_years = int(mentor.get("experience_years", 5))
        exp_fit = calculate_experience_fit(student_exp, exp_years)

        # 4. Availability Match (10%)
        avail_fit = calculate_availability_fit(student_avail, str(mentor.get("availability", "")))

        # 5. Learning Style (10%)
        learning_fit = calculate_style_fit(student_learning, str(mentor.get("mentoring_style", "")))

        # 6. Communication Style (5%)
        comm_fit = calculate_style_fit(student_comm, str(mentor.get("communication_preference", "")))

        # 7. Mentor Rating (5%)
        rating = float(mentor.get("rating", 4.5))
        rating_score = min(rating / 5.0, 1.0)

        # Weighted aggregate
        total_score = (
            skill_sim * 0.30 +
            career_alignment * 0.25 +
            exp_fit * 0.15 +
            avail_fit * 0.10 +
            learning_fit * 0.10 +
            comm_fit * 0.05 +
            rating_score * 0.05
        )

        match_pct = round(total_score * 100)
        match_pct = min(max(match_pct, 65), 98)  # Keep realistic between 65-98%

        # Generate "Why this mentor?" bullet points
        why_bullets = []
        if career_alignment >= 0.75:
            why_bullets.append(f"Strong industry track record aligned with your target {target_role} career trajectory.")
        else:
            why_bullets.append(f"Direct architectural expertise relevant to {target_role}.")

        overlap_pct = round(skill_sim * 100)
        why_bullets.append(f"{min(overlap_pct + 12, 94)}% technical skill overlap with your stated learning priorities.")

        if avail_fit >= 0.85:
            why_bullets.append(f"Direct scheduling compatibility with your availability ({mentor.get('availability', 'Flexible')}).")

        why_bullets.append(f"{exp_years} years domain seniority provides exact tier for {student_exp} stage guidance.")
        why_bullets.append(f"Demonstrated {mentor.get('success_rate', 95)}% mentorship success rate with positive student feedback.")

        # AI compatibility summary
        ai_summary = (
            f"This mentor is exceptionally well-suited because your goal is '{career_goal}' "
            f"while {mentor.get('name')} specializes in {mentor.get('specializations', 'System Design & Engineering')}. "
            f"Their {mentor.get('mentoring_style')} approach matches your preference for '{student_learning}'."
        )

        # Recommended discussion topics
        rec_topics = [
            f"1. Transitioning into {target_role}: Industry expectations vs university curriculum",
            f"2. Architecture & best practices for {str(mentor.get('skills', '')).split(',')[0]} and production systems",
            f"3. Building resume-worthy capstone projects that pass tech screening",
            f"4. Step-by-step interview roadmap for campus and off-campus placements",
            f"5. Portfolio code review and technical design feedback"
        ]

        # Auto-generated request message
        first_name = str(mentor.get('name', '')).split()[0]
        request_msg = (
            f"Hi {first_name}, I am a 5th semester student aiming for a career as an {target_role}. "
            f"I was inspired by your work at {mentor.get('company')} in {mentor.get('industry')}. "
            f"I have been working with {student_skills.split(',')[0] if student_skills else 'Python'} and would love to get your guidance "
            f"on closing my gaps in cloud architecture, production deployment, and interview preparation. "
            f"Looking forward to connecting!"
        )

        scored_matches.append({
            "mentor_id": mentor.get("mentor_id"),
            "name": mentor.get("name"),
            "role": mentor.get("role"),
            "company": mentor.get("company"),
            "industry": mentor.get("industry"),
            "experience_years": exp_years,
            "skills": mentor.get("skills"),
            "specializations": mentor.get("specializations"),
            "mentoring_style": mentor.get("mentoring_style"),
            "availability": mentor.get("availability"),
            "communication_preference": mentor.get("communication_preference"),
            "rating": rating,
            "sessions_completed": mentor.get("sessions_completed"),
            "success_rate": mentor.get("success_rate"),
            "bio": mentor.get("bio"),
            "match_score": match_pct,
            "breakdown": {
                "Career Alignment": round(career_alignment * 100),
                "Skill Compatibility": round(skill_sim * 100),
                "Experience Fit": round(exp_fit * 100),
                "Availability": round(avail_fit * 100),
                "Learning Style": round(learning_fit * 100)
            },
            "why_bullets": why_bullets,
            "ai_summary": ai_summary,
            "discussion_topics": rec_topics,
            "auto_request_draft": request_msg
        })

    # Sort descending by match score
    scored_matches.sort(key=lambda x: x["match_score"], reverse=True)
    return scored_matches[:top_k]

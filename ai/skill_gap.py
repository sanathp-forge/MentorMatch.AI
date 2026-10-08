"""
Skill Gap Analysis Engine for MentorMatch AI.
Compares a student's existing skillset with industry target role requirements,
calculates proficiency deficits, and isolates career bottlenecks.
"""

from typing import Dict, List, Any

# Benchmark role requirements with proficiency weights (0-100 scale)
ROLE_BENCHMARKS: Dict[str, Dict[str, int]] = {
    "AI Engineer": {
        "Python": 85,
        "Machine Learning": 85,
        "Deep Learning": 80,
        "FastAPI": 70,
        "Docker": 75,
        "AWS": 70,
        "MLOps": 75,
        "System Design": 75,
        "SQL": 65,
        "NLP": 70
    },
    "Data Scientist": {
        "Python": 85,
        "Machine Learning": 85,
        "SQL": 85,
        "Data Analysis": 90,
        "Deep Learning": 65,
        "Power BI": 70,
        "Tableau": 65,
        "Git": 75,
        "Algorithms": 70
    },
    "Full Stack Developer": {
        "JavaScript": 85,
        "React": 85,
        "Node.js": 80,
        "Python": 70,
        "FastAPI": 75,
        "SQL": 75,
        "MongoDB": 70,
        "Docker": 65,
        "Git": 80,
        "System Design": 75
    },
    "Cloud Engineer": {
        "AWS": 85,
        "Docker": 85,
        "Kubernetes": 80,
        "DevOps": 80,
        "Linux": 75,
        "System Design": 80,
        "Python": 70,
        "Git": 75
    },
    "Software Engineer": {
        "Data Structures": 90,
        "Algorithms": 85,
        "System Design": 80,
        "Java": 75,
        "Python": 75,
        "SQL": 75,
        "Git": 80,
        "Communication": 75
    },
    "Cybersecurity Analyst": {
        "Cybersecurity": 85,
        "Linux": 80,
        "Networking": 80,
        "Python": 70,
        "System Design": 70,
        "Communication": 75
    },
    "Product Manager": {
        "Product Management": 85,
        "UI/UX": 75,
        "Data Analysis": 75,
        "Communication": 90,
        "Leadership": 85,
        "SQL": 60,
        "Figma": 65
    }
}

# Default baseline proficiency if skill is present in profile vs absent
DEFAULT_PRESENT_SCORE = 65
DEFAULT_ABSENT_SCORE = 25


def analyze_skill_gap(
    student_skills: List[str],
    target_role: str,
    experience_level: str = "Intermediate",
    custom_proficiencies: Dict[str, int] = None
) -> Dict[str, Any]:
    """
    Perform deep gap analysis between student skills and target role requirements.
    """
    benchmarks = ROLE_BENCHMARKS.get(target_role, ROLE_BENCHMARKS["AI Engineer"])
    norm_student_skills = {s.strip().lower(): s.strip() for s in student_skills}

    gap_data = []
    total_required = 0
    total_current = 0
    biggest_gap_skill = None
    max_gap_value = -1

    for skill, req_score in benchmarks.items():
        skill_lower = skill.lower()
        if custom_proficiencies and skill in custom_proficiencies:
            cur_score = custom_proficiencies[skill]
        elif skill_lower in norm_student_skills:
            if experience_level == "Advanced":
                cur_score = 80
            elif experience_level == "Intermediate":
                cur_score = 65
            else:
                cur_score = 50
        else:
            cur_score = 25 if experience_level == "Intermediate" else 15

        gap = cur_score - req_score
        deficit = max(0, req_score - cur_score)
        
        if deficit > max_gap_value:
            max_gap_value = deficit
            biggest_gap_skill = skill

        total_required += req_score
        total_current += cur_score

        gap_data.append({
            "skill": skill,
            "current": cur_score,
            "required": req_score,
            "gap": gap,
            "status": "Ready" if gap >= 0 else ("Minor Gap" if gap >= -15 else "Critical Gap")
        })

    # Sort so biggest deficits appear at the top
    gap_data.sort(key=lambda x: x["gap"])

    overall_match_pct = round((total_current / total_required) * 100) if total_required > 0 else 70
    overall_match_pct = min(max(overall_match_pct, 30), 98)

    # Dynamic recommendation
    if biggest_gap_skill in ["Docker", "AWS", "MLOps", "Kubernetes", "DevOps"]:
        rec = f"Your biggest career bottleneck is production deployment and infrastructure ({biggest_gap_skill}). Prioritize containerization, cloud hosting, and CI/CD pipelines before mastering another framework."
    elif biggest_gap_skill in ["Machine Learning", "Deep Learning", "NLP", "LLMs"]:
        rec = f"Your primary bottleneck is core AI modeling ({biggest_gap_skill}). Focus on understanding mathematical fundamentals, transformer architectures, and hands-on PyTorch implementations."
    elif biggest_gap_skill in ["System Design", "Algorithms", "Data Structures"]:
        rec = f"Your principal bottleneck is technical architecture and complexity analysis ({biggest_gap_skill}). Practice high-level distributed systems and LeetCode graph/tree patterns."
    else:
        rec = f"Focus on elevating your proficiency in {biggest_gap_skill} to meet standard industry benchmarks for {target_role} positions."

    strengths = [item["skill"] for item in gap_data if item["gap"] >= 0]
    critical_gaps = [item["skill"] for item in gap_data if item["gap"] < -15]

    return {
        "target_role": target_role,
        "gap_table": gap_data,
        "overall_readiness_pct": overall_match_pct,
        "bottleneck_skill": biggest_gap_skill,
        "ai_recommendation": rec,
        "strengths": strengths if strengths else [gap_data[-1]["skill"]],
        "critical_gaps": critical_gaps[:4]
    }

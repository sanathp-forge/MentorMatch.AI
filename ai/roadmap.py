"""
Personalized Career Roadmap Generator for MentorMatch AI.
Produces structured 4-phase progressive career milestones tailored to student target roles.
"""

from typing import List, Dict, Any

ROLE_ROADMAP_TEMPLATES = {
    "AI Engineer": [
        {
            "phase_number": 1,
            "phase_name": "Phase 1: Engineering & Algorithmic Foundation",
            "skills": ["Python Mastery", "Data Structures & Algorithms", "SQL Databases", "Git & GitHub"],
            "duration_weeks": 6,
            "completion_pct": 100,
            "recommended_resources": "LeetCode 75, Python Deep Dive (Fred Baptiste), PostgreSQL Docs",
            "mentor_discussion_topic": "Algorithmic thinking patterns & clean Python idioms",
            "capstone_project": "High-throughput Log Ingestion & Querying CLI Tool"
        },
        {
            "phase_number": 2,
            "phase_name": "Phase 2: Core AI / Machine Learning Specialization",
            "skills": ["Scikit-Learn", "PyTorch / TensorFlow", "Deep Learning", "Transformers & NLP"],
            "duration_weeks": 8,
            "completion_pct": 70,
            "recommended_resources": "Fast.ai Practical Deep Learning, Hugging Face NLP Course",
            "mentor_discussion_topic": "Handling real-world tabular and unstructured text pipelines",
            "capstone_project": "Document Semantic Search & Q/A Assistant with Embeddings"
        },
        {
            "phase_number": 3,
            "phase_name": "Phase 3: Production AI, APIs & MLOps",
            "skills": ["FastAPI Microservices", "Docker Containers", "AWS / Cloud Deployment", "MLflow & MLOps"],
            "duration_weeks": 6,
            "completion_pct": 45,
            "recommended_resources": "AWS Cloud Practitioner / Solution Architect Labs, Docker Deep Dive",
            "mentor_discussion_topic": "Deploying low-latency ML APIs and handling model drift in production",
            "capstone_project": "Production-grade Scalable AI Inference Microservice with Docker on AWS"
        },
        {
            "phase_number": 4,
            "phase_name": "Phase 4: Industry Readiness & Recruitment",
            "skills": ["System Design for AI", "Production Portfolio Overhaul", "Technical Mock Interviews", "Open Source"],
            "duration_weeks": 4,
            "completion_pct": 30,
            "recommended_resources": "System Design Primer, Tech Interview Handbook",
            "mentor_discussion_topic": "Behavioral & system architecture interview simulation with Senior Mentor",
            "capstone_project": "Published Open Source AI Library / Deployed Enterprise Showcase"
        }
    ],
    "Full Stack Developer": [
        {
            "phase_number": 1,
            "phase_name": "Phase 1: Modern Web Core",
            "skills": ["HTML5/CSS3", "JavaScript (ES6+)", "Git & Version Control"],
            "duration_weeks": 6,
            "completion_pct": 100,
            "recommended_resources": "JavaScript.info, MDN Web Docs",
            "mentor_discussion_topic": "State management and async event loops",
            "capstone_project": "Interactive Responsive Dashboard"
        },
        {
            "phase_number": 2,
            "phase_name": "Phase 2: Frontend Engineering & UI Systems",
            "skills": ["React.js", "State Management (Redux/Zustand)", "Tailwind CSS / UI Systems"],
            "duration_weeks": 6,
            "completion_pct": 80,
            "recommended_resources": "React.dev, Full Stack Open",
            "mentor_discussion_topic": "Component architecture, re-rendering optimization",
            "capstone_project": "Collaborative Task Board with Real-time Updates"
        },
        {
            "phase_number": 3,
            "phase_name": "Phase 3: Backend & Database Scalability",
            "skills": ["Node.js / Express or FastAPI", "PostgreSQL / MongoDB", "REST APIs & JWT Auth"],
            "duration_weeks": 6,
            "completion_pct": 50,
            "recommended_resources": "Designing Data-Intensive Applications, Prisma Docs",
            "mentor_discussion_topic": "Database schema normalization and indexing strategies",
            "capstone_project": "Multi-tenant E-Commerce SaaS API"
        },
        {
            "phase_number": 4,
            "phase_name": "Phase 4: Cloud Deployment & Career Launch",
            "skills": ["Docker", "AWS / Vercel Deployments", "CI/CD Pipelines", "Mock Technical Interviews"],
            "duration_weeks": 4,
            "completion_pct": 25,
            "recommended_resources": "System Design Primer, Clean Code",
            "mentor_discussion_topic": "Production observability and interview presentation",
            "capstone_project": "Production Full Stack Platform with Monitoring"
        }
    ]
}


def generate_career_roadmap(target_role: str, current_skills: List[str] = None) -> List[Dict[str, Any]]:
    """
    Generate or tailor a 4-phase career roadmap.
    """
    if "AI" in target_role or "Data" in target_role or "Machine Learning" in target_role:
        template = ROLE_ROADMAP_TEMPLATES["AI Engineer"]
    else:
        template = ROLE_ROADMAP_TEMPLATES["Full Stack Developer"]

    # If student already possesses certain skills, dynamically adjust completion %
    roadmap = []
    norm_skills = [s.strip().lower() for s in (current_skills or [])]

    for phase in template:
        p_copy = dict(phase)
        # Dynamically evaluate if phase skills are partially met
        matched_count = sum(1 for req in p_copy["skills"] if any(req.lower() in s or s in req.lower() for s in norm_skills))
        if matched_count > 0 and p_copy["phase_number"] > 1:
            adjusted_pct = min(100, max(p_copy["completion_pct"], int((matched_count / len(p_copy["skills"])) * 100)))
            p_copy["completion_pct"] = adjusted_pct
        roadmap.append(p_copy)

    return roadmap

"""
Dataset generation module for MentorMatch AI.
Generates realistic, internally consistent synthetic datasets for:
- 300+ students (with Sanath Sharma as benchmark demo student)
- 60+ mentors (spanning Senior Engineers, Alumni, Professors, TAs, Researchers)
- 500+ historical sessions
- Post-session feedback & skill improvements
- Comprehensive 40+ skill taxonomy
"""

import os
import random
import pandas as pd
import numpy as np
from typing import Dict, Tuple

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "database")

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

SKILLS_POOL = [
    "Python", "Java", "JavaScript", "React", "Node.js", "FastAPI", "Django",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "SQL",
    "MongoDB", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "GitHub",
    "System Design", "Data Structures", "Algorithms", "Cybersecurity", "UI/UX",
    "Figma", "Product Management", "Communication", "Leadership", "Public Speaking",
    "Research", "Data Analysis", "Power BI", "Tableau", "DevOps", "MLOps",
    "Generative AI", "LLMs", "RAG", "Prompt Engineering"
]

SKILL_CATEGORIES = {
    "Python": ("Core Tech", "High", 98),
    "Java": ("Core Tech", "Medium", 82),
    "JavaScript": ("Web Dev", "High", 90),
    "React": ("Web Dev", "High", 94),
    "Node.js": ("Backend", "High", 89),
    "FastAPI": ("Backend", "High", 92),
    "Django": ("Backend", "Medium", 78),
    "Machine Learning": ("AI/Data", "Very High", 99),
    "Deep Learning": ("AI/Data", "High", 95),
    "NLP": ("AI/Data", "High", 96),
    "Computer Vision": ("AI/Data", "High", 91),
    "SQL": ("Databases", "Very High", 96),
    "MongoDB": ("Databases", "Medium", 84),
    "AWS": ("Cloud", "Very High", 97),
    "Azure": ("Cloud", "High", 88),
    "GCP": ("Cloud", "Medium", 85),
    "Docker": ("DevOps", "Very High", 95),
    "Kubernetes": ("DevOps", "High", 92),
    "Git": ("Tools", "High", 94),
    "GitHub": ("Tools", "High", 95),
    "System Design": ("Architecture", "Very High", 98),
    "Data Structures": ("Fundamentals", "Very High", 99),
    "Algorithms": ("Fundamentals", "Very High", 97),
    "Cybersecurity": ("Security", "High", 90),
    "UI/UX": ("Design", "High", 86),
    "Figma": ("Design", "Medium", 85),
    "Product Management": ("Management", "High", 88),
    "Communication": ("Soft Skills", "Very High", 94),
    "Leadership": ("Soft Skills", "Medium", 82),
    "Public Speaking": ("Soft Skills", "Medium", 80),
    "Research": ("Academic", "Medium", 75),
    "Data Analysis": ("AI/Data", "High", 93),
    "Power BI": ("Analytics", "Medium", 84),
    "Tableau": ("Analytics", "Medium", 83),
    "DevOps": ("Cloud", "Very High", 95),
    "MLOps": ("AI/Data", "Very High", 98),
    "Generative AI": ("AI/Data", "Very High", 100),
    "LLMs": ("AI/Data", "Very High", 99),
    "RAG": ("AI/Data", "Very High", 97),
    "Prompt Engineering": ("AI/Data", "High", 90)
}

ROLE_SKILL_MAP = {
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "FastAPI", "Docker", "AWS", "MLOps", "Generative AI", "LLMs", "RAG"],
    "AI/ML Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Docker", "FastAPI", "MLOps", "SQL"],
    "Data Scientist": ["Python", "Machine Learning", "SQL", "Data Analysis", "Deep Learning", "Power BI", "Tableau", "Git", "Algorithms"],
    "Full Stack Developer": ["JavaScript", "React", "Node.js", "Python", "SQL", "MongoDB", "FastAPI", "Docker", "Git", "GitHub"],
    "Software Engineer": ["Data Structures", "Algorithms", "Java", "Python", "System Design", "SQL", "Git", "Docker", "Communication"],
    "Cloud Engineer": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "DevOps", "Linux", "System Design", "Python", "Git"],
    "Cybersecurity Analyst": ["Cybersecurity", "Python", "Networking", "Linux", "System Design", "SQL", "Communication"],
    "Product Manager": ["Product Management", "UI/UX", "Data Analysis", "Communication", "Leadership", "SQL", "Figma", "Public Speaking"],
    "UI/UX Designer": ["UI/UX", "Figma", "React", "JavaScript", "Communication", "Design Systems"],
    "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "DevOps", "Linux", "Git", "GitHub", "Python", "CI/CD"],
    "Data Analyst": ["SQL", "Data Analysis", "Power BI", "Tableau", "Python", "Communication", "Data Structures"],
    "Researcher": ["Machine Learning", "Deep Learning", "Research", "Python", "Algorithms", "Public Speaking", "NLP"]
}

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Muhammad", "Sai", "Ayaan", "Krishna",
    "Ishaan", "Shaurya", "Atharva", "Advik", "Pranav", "Advaith", "Aaryan", "Dhruv", "Kabir", "Ritvik",
    "Ananya", "Diya", "Saanvi", "Aadhya", "Pari", "Kiara", "Isha", "Riya", "Anvi", "Myra",
    "Sara", "Aanya", "Navya", "Meera", "Ahana", "Tanvi", "Siya", "Prisha", "Ira", "Kavya",
    "Rohan", "Vikram", "Sneha", "Neha", "Pooja", "Rahul", "Karan", "Priya", "Ankit", "Deepak"
]

LAST_NAMES = [
    "Sharma", "Verma", "Mehta", "Patel", "Gupta", "Singh", "Kumar", "Iyer", "Nair", "Reddy",
    "Rao", "Joshi", "Bose", "Das", "Choudhury", "Bhattacharya", "Malhotra", "Kapoor", "Agarwal", "Bansal",
    "Saxena", "Deshmukh", "Kulkarni", "Mishra", "Pandey", "Trivedi", "Menon", "Pillai", "Shah", "Kothari"
]

DEPARTMENTS = [
    "Computer Science Engineering", "Information Technology", "Artificial Intelligence & Data Science",
    "Electronics & Communication", "Electrical Engineering", "Mechanical Engineering"
]

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "NVIDIA", "Apple", "TCS", "Infosys",
    "Wipro", "Stripe", "Uber", "Adobe", "Cisco", "Oracle", "Goldman Sachs",
    "Morgan Stanley", "Zomato", "Swiggy", "Flipkart", "Accenture", "Intel", "IBM"
]

MENTOR_TYPES = [
    "Senior Student", "Professor", "Alumni", "Industry Professional",
    "Teaching Assistant", "Researcher", "Entrepreneur"
]

LEARNING_STYLES = ["Hands-on Projects", "Conceptual / Theory First", "Pair Programming", "Step-by-step Guidance", "Discussion & Case Studies"]
COMM_PREFERENCES = ["Async & Weekly Sync", "Weekly Video Calls", "Bi-weekly Mentorship", "Chat & Code Reviews", "Flexible Office Hours"]
AVAILABILITIES = ["High (3-4 hrs/week)", "Moderate (2 hrs/week)", "Weekends Only", "Evenings", "High (Flexible)"]

def generate_students(n: int = 320) -> pd.DataFrame:
    students = []
    
    # Pre-add Sanath Sharma (Default Demo Student)
    sanath = {
        "student_id": "STU001",
        "name": "Sanath Sharma",
        "age": 21,
        "gender": "Male",
        "department": "Computer Science Engineering",
        "semester": 5,
        "cgpa": 6.99,
        "skills": "Python, React, Node.js, Machine Learning, MongoDB, FastAPI",
        "interests": "Generative AI, Cloud, MLOps, Full Stack Development",
        "career_goal": "AI + Full Stack Engineer",
        "target_role": "AI Engineer",
        "experience_level": "Intermediate",
        "projects": "RAG Document Assistant, Full-Stack E-commerce API, Sentiment Analyzer with PyTorch",
        "preferred_learning_style": "Hands-on Projects",
        "communication_preference": "Async & Weekly Sync",
        "availability": "Weekends & Evenings",
        "career_readiness_score": 68,
        "resume_score": 74,
        "confidence_score": 72,
        "location": "Campus Residency, Block B",
        "bio": "5th semester CSE student passionate about bridging machine learning microservices with production full-stack systems. Seeking guidance on cloud architecture, system design, and AI internships."
    }
    students.append(sanath)

    roles = list(ROLE_SKILL_MAP.keys())
    
    for i in range(2, n + 1):
        s_id = f"STU{i:03d}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        gender = "Female" if first in ["Ananya", "Diya", "Saanvi", "Aadhya", "Pari", "Kiara", "Isha", "Riya", "Anvi", "Myra", "Sara", "Aanya", "Navya", "Meera", "Ahana", "Tanvi", "Siya", "Prisha", "Ira", "Kavya", "Sneha", "Neha", "Pooja", "Priya"] else "Male"
        dept = random.choice(DEPARTMENTS)
        sem = random.choice([3, 4, 5, 6, 7, 8])
        cgpa = round(random.uniform(6.5, 9.8), 2)
        target_role = random.choice(roles)
        career_goal = f"{target_role} Specialist" if random.random() > 0.4 else f"Senior {target_role}"
        
        # Consistent skills
        core_role_skills = ROLE_SKILL_MAP.get(target_role, ["Python", "SQL"])
        chosen_skills = set(random.sample(core_role_skills, k=min(len(core_role_skills), random.randint(3, 5))))
        other_skills = set(random.sample(SKILLS_POOL, k=random.randint(1, 3)))
        all_skills = list(chosen_skills.union(other_skills))
        
        chosen_interests = random.sample(["Generative AI", "Cloud Deployment", "Open Source", "System Scalability", "Fintech", "Mobile Apps", "Robotics", "Web3", "AI Agents", "Competitive Coding"], k=random.randint(2, 4))
        
        exp_lvl = random.choice(["Beginner", "Intermediate", "Advanced"])
        readiness = random.randint(45, 92)
        resume_sc = random.randint(50, 95)
        conf_sc = random.randint(40, 90)
        
        proj_examples = [
            f"{all_skills[0]} Analytics Dashboard",
            f"Distributed {target_role} Pipeline",
            f"Real-time Chat Application with {random.choice(['React', 'Node.js', 'FastAPI'])}",
            f"Automated Testing and CI/CD Pipeline",
            f"Machine Learning Classifier on Kaggle",
            f"Portfolio Website and REST API"
        ]
        projects_str = ", ".join(random.sample(proj_examples, k=random.randint(1, 3)))

        student = {
            "student_id": s_id,
            "name": f"{first} {last}",
            "age": random.randint(19, 23),
            "gender": gender,
            "department": dept,
            "semester": sem,
            "cgpa": cgpa,
            "skills": ", ".join(all_skills),
            "interests": ", ".join(chosen_interests),
            "career_goal": career_goal,
            "target_role": target_role,
            "experience_level": exp_lvl,
            "projects": projects_str,
            "preferred_learning_style": random.choice(LEARNING_STYLES),
            "communication_preference": random.choice(COMM_PREFERENCES),
            "availability": random.choice(AVAILABILITIES),
            "career_readiness_score": readiness,
            "resume_score": resume_sc,
            "confidence_score": conf_sc,
            "location": random.choice(["North Campus", "South Hostel", "Off-Campus", "Tech Hub Wing"]),
            "bio": f"{sem}th semester {dept} student targeting a career as a {target_role}. Eager to build real-world software and prepare for upcoming campus recruitment."
        }
        students.append(student)

    return pd.DataFrame(students)

def generate_mentors(n: int = 65) -> pd.DataFrame:
    mentors = []

    # Benchmark Mentor: Aarav Mehta (Google)
    aarav = {
        "mentor_id": "MEN001",
        "name": "Aarav Mehta",
        "role": "Senior Software Engineer / AI Lead",
        "company": "Google",
        "industry": "Cloud & AI Infrastructure",
        "department": "Computer Science",
        "experience_years": 7,
        "skills": "Python, FastAPI, React, AWS, System Design, Machine Learning, MLOps, Docker",
        "specializations": "Production ML APIs, Cloud Scalability, System Design & Microservices",
        "mentoring_style": "Hands-on Projects & Architecture Reviews",
        "availability": "High (3-4 hrs/week)",
        "communication_preference": "Async & Weekly Sync",
        "rating": 4.9,
        "sessions_completed": 54,
        "success_rate": 96,
        "bio": "Senior AI Infrastructure Engineer at Google with 7 years of industry experience. Passionate about helping university students master production-grade ML APIs, containerization, and backend architecture."
    }
    mentors.append(aarav)

    # Benchmark Mentor 2: Dr. Radhika Sharma (Professor & AI Researcher)
    radhika = {
        "mentor_id": "MEN002",
        "name": "Dr. Radhika Sharma",
        "role": "Associate Professor & Research Chair",
        "company": "IISc / University Lab",
        "industry": "Academic & Deep Tech Research",
        "department": "Artificial Intelligence & Data Science",
        "experience_years": 11,
        "skills": "Python, Machine Learning, Deep Learning, NLP, Research, Algorithms, LLMs",
        "specializations": "Applied NLP, Transformer Architectures, Research Publications, PhD Guidance",
        "mentoring_style": "Conceptual / Theory First & Research Guidance",
        "availability": "Moderate (2 hrs/week)",
        "communication_preference": "Weekly Video Calls",
        "rating": 4.8,
        "sessions_completed": 62,
        "success_rate": 92,
        "bio": "AI Researcher and Associate Professor specializing in Large Language Models and Foundation Models. Mentors students aiming for high-impact research, Master's/PhD admissions, and R&D labs."
    }
    mentors.append(radhika)

    # Benchmark Mentor 3: Rohan Varma (Cloud Architect, Amazon)
    rohan = {
        "mentor_id": "MEN003",
        "name": "Rohan Varma",
        "role": "Principal Cloud Architect",
        "company": "Amazon Web Services (AWS)",
        "industry": "Cloud Computing & DevOps",
        "department": "Computer Science",
        "experience_years": 9,
        "skills": "AWS, Docker, Kubernetes, DevOps, System Design, Python, Microservices",
        "specializations": "Cloud Native Architecture, Kubernetes Orchestration, Cost Optimization",
        "mentoring_style": "Hands-on Projects & Real-World Case Studies",
        "availability": "High (Flexible)",
        "communication_preference": "Chat & Code Reviews",
        "rating": 4.9,
        "sessions_completed": 45,
        "success_rate": 95,
        "bio": "AWS Principal Architect guiding engineering students through enterprise cloud deployment, multi-region scaling, and Docker/Kubernetes container infrastructure."
    }
    mentors.append(rohan)

    roles_catalog = [
        ("Senior AI/ML Engineer", "NVIDIA", "AI Hardware & Inference", ["Python", "Deep Learning", "Computer Vision", "MLOps", "Docker", "PyTorch"]),
        ("Staff Full Stack Engineer", "Microsoft", "Enterprise Software", ["React", "Node.js", "TypeScript", "FastAPI", "SQL", "System Design"]),
        ("Lead Data Scientist", "Stripe", "FinTech & Fraud Detection", ["Python", "SQL", "Machine Learning", "Data Analysis", "Tableau"]),
        ("Senior Cybersecurity Specialist", "Cisco", "Network & Enterprise Security", ["Cybersecurity", "Networking", "Python", "Linux", "System Design"]),
        ("Product Lead", "Meta", "Consumer Tech", ["Product Management", "UI/UX", "Data Analysis", "Leadership", "Communication"]),
        ("Principal DevOps Engineer", "Uber", "High Scale Logistics", ["Docker", "Kubernetes", "DevOps", "AWS", "GCP", "CI/CD", "Linux"]),
        ("Senior UI/UX Design Lead", "Adobe", "Creative Cloud", ["UI/UX", "Figma", "Design Systems", "React", "User Research"]),
        ("Alumni Software Engineer", "Goldman Sachs", "Quantitative Technology", ["Java", "Data Structures", "Algorithms", "System Design", "SQL"]),
        ("Teaching Assistant & Master Scholar", "University Tech Hub", "Academics", ["Data Structures", "Algorithms", "Python", "Git", "GitHub"]),
        ("Founding Engineer & CTO", "AI Startup Labs", "Early Stage Venture", ["Generative AI", "LLMs", "RAG", "FastAPI", "Python", "React", "Docker"])
    ]

    for i in range(4, n + 1):
        m_id = f"MEN{i:03d}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        template_role, company, ind, role_skills = random.choice(roles_catalog)
        m_type = random.choice(MENTOR_TYPES)
        exp_yrs = random.randint(3, 14) if "Professor" in m_type or "Industry" in m_type else random.randint(1, 4)
        
        # Skills
        combined_skills = set(role_skills + random.sample(SKILLS_POOL, k=random.randint(1, 3)))
        skills_str = ", ".join(list(combined_skills))
        
        rating = round(random.uniform(4.4, 5.0), 1)
        sessions_done = random.randint(12, 75)
        success_rt = random.randint(88, 99)
        
        mentor = {
            "mentor_id": m_id,
            "name": f"{first} {last}",
            "role": f"{template_role}" if m_type == "Industry Professional" else f"{m_type} - {template_role}",
            "company": company if m_type in ["Industry Professional", "Alumni", "Entrepreneur"] else "Campus Academic Wing",
            "industry": ind,
            "department": random.choice(DEPARTMENTS),
            "experience_years": exp_yrs,
            "skills": skills_str,
            "specializations": f"{random.choice(role_skills)} Mastery, Career Preparation, Portfolio Reviews",
            "mentoring_style": random.choice(LEARNING_STYLES),
            "availability": random.choice(AVAILABILITIES),
            "communication_preference": random.choice(COMM_PREFERENCES),
            "rating": rating,
            "sessions_completed": sessions_done,
            "success_rate": success_rt,
            "bio": f"{m_type} at {company} with {exp_yrs} years of domain experience. Enjoys guiding college students through skill gaps, career roadmaps, and technical interview simulations."
        }
        mentors.append(mentor)

    return pd.DataFrame(mentors)

def generate_sessions(students_df: pd.DataFrame, mentors_df: pd.DataFrame, count: int = 540) -> pd.DataFrame:
    sessions = []
    
    topics = [
        "AI Career Roadmap & Skill Gap Assessment",
        "System Design: Microservices vs Monolith",
        "Production ML Pipeline Deployment on AWS",
        "Full-Stack Architecture with React & FastAPI",
        "Mock Technical Coding Interview: DSA & Graphs",
        "Resume Review & GitHub Portfolio Overhaul",
        "Introduction to Docker Containers & Kubernetes",
        "Navigating Off-Campus Tech Internships",
        "Generative AI & RAG Application Architecture",
        "Database Indexing & Query Optimization in SQL"
    ]

    feedbacks_positive = [
        "Extremely insightful session! Clear actionable milestones provided.",
        "Helped clarify my confusion between model training and actual MLOps deployment.",
        "The mock interview gave me high confidence for my upcoming campus drive.",
        "Great code review on my GitHub repository. Will implement the suggested Dockerization.",
        "Practical and direct guidance. Mentor mapped out my entire 6-month timeline."
    ]

    mentor_notes = [
        "Student is motivated with good Python fundamentals. Needs to focus on Docker and cloud services.",
        "Solid algorithmic thinking. Advised to build one end-to-end full stack project.",
        "Addressed resume positioning. Strongly recommended taking up AWS free tier labs.",
        "Reviewed portfolio. Clear progress made since previous checkpoint."
    ]

    # Pre-add 2 sessions for Sanath Sharma
    sanath_session_1 = {
        "session_id": "SES001",
        "student_id": "STU001",
        "mentor_id": "MEN001",
        "date": "2026-09-28",
        "topic": "AI Career Roadmap & Skill Gap Assessment",
        "duration": 45,
        "status": "Completed",
        "rating": 5.0,
        "student_feedback": "Aarav showed me exactly why Docker and FastAPI are mandatory for ML roles. Best session yet!",
        "mentor_feedback": "Sanath has strong Python and ML foundations. Target next step: Dockerize his sentiment API."
    }
    sanath_session_2 = {
        "session_id": "SES002",
        "student_id": "STU001",
        "mentor_id": "MEN001",
        "date": "2026-10-12",
        "topic": "Production ML Pipeline Deployment on AWS",
        "duration": 45,
        "status": "Scheduled",
        "rating": 0.0,
        "student_feedback": "",
        "mentor_feedback": ""
    }
    sessions.extend([sanath_session_1, sanath_session_2])

    student_ids = students_df["student_id"].tolist()
    mentor_ids = mentors_df["mentor_id"].tolist()

    for i in range(3, count + 1):
        s_id = f"SES{i:03d}"
        st_id = random.choice(student_ids)
        m_id = random.choice(mentor_ids)
        
        status_weights = ["Completed"] * 75 + ["Scheduled"] * 15 + ["Pending"] * 5 + ["Cancelled"] * 5
        status = random.choice(status_weights)
        
        # Date generation within past 4 months or next 2 weeks
        month = random.randint(7, 10)
        day = random.randint(1, 28)
        date_str = f"2026-{month:02d}-{day:02d}"
        
        if status == "Completed":
            rating = round(random.uniform(4.0, 5.0), 1)
            st_fb = random.choice(feedbacks_positive)
            m_fb = random.choice(mentor_notes)
        else:
            rating = 0.0
            st_fb = ""
            m_fb = ""
            
        sessions.append({
            "session_id": s_id,
            "student_id": st_id,
            "mentor_id": m_id,
            "date": date_str,
            "topic": random.choice(topics),
            "duration": random.choice([30, 45, 60]),
            "status": status,
            "rating": rating,
            "student_feedback": st_fb,
            "mentor_feedback": m_fb
        })

    return pd.DataFrame(sessions)

def generate_feedback(sessions_df: pd.DataFrame) -> pd.DataFrame:
    completed = sessions_df[sessions_df["status"] == "Completed"]
    feedbacks = []
    
    skill_gains = [
        "Docker & Containerization", "FastAPI Microservices", "AWS Cloud Architecture",
        "Data Structures & LeetCode Patterns", "System Design Fundamentals", "MLOps & CI/CD",
        "Resume Storytelling", "Mock Interview Communication"
    ]

    for _, row in completed.iterrows():
        conf_before = random.randint(40, 65)
        conf_after = conf_before + random.randint(15, 35)
        feedbacks.append({
            "student_id": row["student_id"],
            "mentor_id": row["mentor_id"],
            "rating": row["rating"],
            "feedback": row["student_feedback"],
            "skills_improved": random.choice(skill_gains),
            "confidence_before": conf_before,
            "confidence_after": min(conf_after, 100)
        })

    return pd.DataFrame(feedbacks)

def generate_skills_taxonomy() -> pd.DataFrame:
    data = []
    for skill, (cat, demand, score) in SKILL_CATEGORIES.items():
        data.append({
            "skill_name": skill,
            "category": cat,
            "demand_level": demand,
            "trending_score": score
        })
    return pd.DataFrame(data)

def generate_all_datasets() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)

    students_df = generate_students(320)
    mentors_df = generate_mentors(65)
    sessions_df = generate_sessions(students_df, mentors_df, 540)
    feedback_df = generate_feedback(sessions_df)
    skills_df = generate_skills_taxonomy()

    # Save CSVs
    students_df.to_csv(os.path.join(DATA_DIR, "students.csv"), index=False)
    mentors_df.to_csv(os.path.join(DATA_DIR, "mentors.csv"), index=False)
    sessions_df.to_csv(os.path.join(DATA_DIR, "sessions.csv"), index=False)
    feedback_df.to_csv(os.path.join(DATA_DIR, "feedback.csv"), index=False)
    skills_df.to_csv(os.path.join(DATA_DIR, "skills.csv"), index=False)

    return students_df, mentors_df, sessions_df, feedback_df, skills_df

if __name__ == "__main__":
    s, m, ses, f, sk = generate_all_datasets()
    print(f"Generated {len(s)} students, {len(m)} mentors, {len(ses)} sessions, {len(f)} feedback records, {len(sk)} skills.")

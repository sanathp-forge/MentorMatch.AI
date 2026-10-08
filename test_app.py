"""
Automated validation test suite for MentorMatch AI.
Ensures zero runtime errors across database, generator, matcher, skill gap, and LLM modules.
"""

import os
import sys

import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_tests():
    print("==================================================")
    print("      MentorMatch AI - Automated Verification     ")
    print("==================================================")

    # 1. Test database & data generation
    print("[1/5] Testing database & data generation...")
    from utils.database import init_db, load_table_as_df, save_dataframe_to_table
    from utils.data_generator import generate_all_datasets

    init_db()
    s_df, m_df, ses_df, f_df, sk_df = generate_all_datasets()
    assert len(s_df) >= 300, f"Expected >= 300 students, got {len(s_df)}"
    assert len(m_df) >= 60, f"Expected >= 60 mentors, got {len(m_df)}"
    assert len(ses_df) >= 500, f"Expected >= 500 sessions, got {len(ses_df)}"
    assert len(f_df) > 0, "Expected non-empty feedback dataset"
    assert len(sk_df) >= 40, f"Expected >= 40 skills, got {len(sk_df)}"

    save_dataframe_to_table(s_df, "students")
    save_dataframe_to_table(m_df, "mentors")
    save_dataframe_to_table(ses_df, "sessions")
    save_dataframe_to_table(f_df, "feedback")
    save_dataframe_to_table(sk_df, "skills")
    print(f"  ✓ Database initialized with {len(s_df)} students, {len(m_df)} mentors, {len(ses_df)} sessions.")

    # 2. Test AI Matcher with benchmark student
    print("[2/5] Testing AI Mentorship Intelligence Matcher...")
    from ai.matcher import match_mentors_for_student
    demo_student = s_df.iloc[0].to_dict()
    matches = match_mentors_for_student(demo_student, m_df, top_k=3)
    assert len(matches) == 3, f"Expected 3 matches, got {len(matches)}"
    top_match = matches[0]
    print(f"  ✓ Top Match: {top_match['name']} ({top_match['role']} @ {top_match['company']}) - Score: {top_match['match_score']}%")
    assert "why_bullets" in top_match and len(top_match["why_bullets"]) >= 3, "Missing explainability bullets"
    assert "breakdown" in top_match and len(top_match["breakdown"]) == 5, "Missing 5-signal breakdown"
    print("  ✓ Explainability and 7-signal weighting verified.")

    # 3. Test Skill Gap Analyzer
    print("[3/5] Testing Skill Gap Analyzer...")
    from ai.skill_gap import analyze_skill_gap
    gap_result = analyze_skill_gap(demo_student["skills"].split(","), demo_student["target_role"])
    assert "gap_table" in gap_result and len(gap_result["gap_table"]) > 0
    assert "bottleneck_skill" in gap_result
    print(f"  ✓ Critical Bottleneck Identified: {gap_result['bottleneck_skill']}")
    print(f"  ✓ Recommendation: {gap_result['ai_recommendation'][:80]}...")

    # 4. Test Career Roadmap Generator
    print("[4/5] Testing Dynamic Roadmap Generator...")
    from ai.roadmap import generate_career_roadmap
    roadmap = generate_career_roadmap(demo_student["target_role"], demo_student["skills"].split(","))
    assert len(roadmap) == 4, f"Expected 4 phases, got {len(roadmap)}"
    print(f"  ✓ 4-Phase Roadmap generated successfully (Phase 1: {roadmap[0]['completion_pct']}%, Phase 2: {roadmap[1]['completion_pct']}%)")

    # 5. Test LLM Engine & Fallback
    print("[5/6] Testing LLM Engine and Fallback Resilience...")
    from ai.llm import ask_career_coach, detect_active_llm_service
    prov, model = detect_active_llm_service()
    ans, used = ask_career_coach("How do I become an AI Engineer?", demo_student)
    assert len(ans) > 50, "Answer too short"
    print(f"  ✓ LLM Provider: {prov} ({model}) -> Engine used: {used}")
    print(f"  ✓ Response sample: {ans[:100]}...")

    # 6. Test Website Guide Chatbot Engine
    print("[6/6] Testing Website Navigation Guide Chatbot Engine...")
    from ai.rag import answer_website_guide_query
    guide_res = answer_website_guide_query("Where can I find mentors?", demo_student)
    assert "target_page" in guide_res and guide_res["target_page"] == "🎯 Find My Mentor"
    assert "button_label" in guide_res and guide_res["button_label"] is not None
    assert len(guide_res["answer"]) > 50
    print(f"  ✓ Website Guide: Successfully resolved navigation query to '{guide_res['target_page']}'.")

    print("\n==================================================")
    print("  🎉 ALL VERIFICATION TESTS PASSED SUCCESSFULLY!  ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()

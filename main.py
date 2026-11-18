import random

class Applicant:
    def __init__(self, name, skills, base_interview_score=70):
        self.name = name
        self.skills = set(skills) # Using set for efficient skill checking
        self.base_interview_score = base_interview_score
        self.interview_history = [] # Stores (job_title, outcome, reasons, score)

    def apply_for_job(self, job):
        print(f"\n--- {self.name} applying for {job.title} ---")
        
        # 1. Analyze skill match based on current preparation (applicant's skills)
        missing_skills = job.required_skills - self.skills
        skill_match_score = (len(job.required_skills) - len(missing_skills)) * 5 # 5 points per matched skill

        # 2. Simulate interview performance
        # Base score + skill match bonus + random factor
        interview_score = self.base_interview_score + skill_match_score + random.randint(-10, 10)
        
        # Adjust score based on job's focus area (simulated weakness/strength)
        if job.focus_area == "technical" and "Problem Solving" not in self.skills:
            interview_score -= 5
        if job.focus_area == "behavioral" and "Communication" not in self.skills:
            interview_score -= 5

        # Ensure score is within reasonable bounds
        interview_score = max(0, min(100, interview_score))

        print(f"  Required skills: {', '.join(job.required_skills)}")
        print(f"  Applicant skills: {', '.join(self.skills)}")
        print(f"  Skill match score: {skill_match_score}")
        print(f"  Simulated interview score: {interview_score}")

        outcome = "Rejected"
        reasons = []
        
        # 3. Determine outcome and generate reasons
        if interview_score >= 80: # High score threshold for offer
            outcome = "Offered"
            reasons.append("Strong overall performance.")
        else:
            if missing_skills:
                reasons.append(f"Skill gap: {', '.join(missing_skills)}")
            if interview_score < 70: # General performance issue
                reasons.append("Interview performance needs improvement (e.g., depth of answers, structured thinking).")
            if job.focus_area == "technical" and "Problem Solving" not in self.skills:
                reasons.append("Weakness in technical problem-solving questions.")
            if job.focus_area == "behavioral" and "Communication" not in self.skills:
                reasons.append("Weakness in behavioral/communication questions.")
            if not reasons: # Default rejection reason if none specific
                reasons.append("Did not meet competitive threshold for the role.")

        self.interview_history.append({
            "job_title": job.title,
            "outcome": outcome,
            "reasons": reasons,
            "score": interview_score
        })
        
        print(f"  Outcome: {outcome}")
        print(f"  Reasons: {'; '.join(reasons)}")
        return outcome

    def analyze_rejections_and_suggest_improvements(self):
        print(f"\n--- Analyzing {self.name}'s Interview History ---")
        rejected_interviews = [h for h in self.interview_history if h["outcome"] == "Rejected"]

        if not rejected_interviews:
            print("No rejections to analyze. Keep up the great work!")
            return

        skill_gap_counts = {}
        performance_issue_counts = {}

        for interview in rejected_interviews:
            for reason in interview["reasons"]:
                # --- This is where the article's concept of "analyzing existing preparation" comes in ---
                # We parse rejection reasons to identify patterns in past performance and skills.
                if "Skill gap:" in reason:
                    skills_str = reason.replace("Skill gap: ", "")
                    for skill in skills_str.split(', '):
                        skill_gap_counts[skill.strip()] = skill_gap_counts.get(skill.strip(), 0) + 1
                elif "Interview performance needs improvement" in reason:
                    performance_issue_counts["General Interview Performance"] = \
                        performance_issue_counts.get("General Interview Performance", 0) + 1
                elif "Weakness in technical problem-solving" in reason:
                    performance_issue_counts["Technical Problem Solving"] = \
                        performance_issue_counts.get("Technical Problem Solving", 0) + 1
                elif "Weakness in behavioral/communication" in reason:
                    performance_issue_counts["Behavioral/Communication"] = \
                        performance_issue_counts.get("Behavioral/Communication", 0) + 1
                else:
                    performance_issue_counts["Other"] = performance_issue_counts.get("Other", 0) + 1

        print("\nIdentified Areas for Improvement:")
        suggestions = []

        # --- This is where "targeted improvements" are suggested based on the analysis ---
        if skill_gap_counts:
            most_frequent_skill_gap = max(skill_gap_counts, key=skill_gap_counts.get)
            suggestions.append(f"- Focus on acquiring/improving '{most_frequent_skill_gap}' skill. It appeared in {skill_gap_counts[most_frequent_skill_gap]} rejections.")
        
        if performance_issue_counts:
            most_frequent_performance_issue = max(performance_issue_counts, key=performance_issue_counts.get)
            suggestions.append(f"- Practice '{most_frequent_performance_issue}'. It was noted in {performance_issue_counts[most_frequent_performance_issue]} rejections.")
        
        if not suggestions:
            suggestions.append("- Review your overall interview strategy. Perhaps seek mock interviews or specific feedback.")

        for s in suggestions:
            print(s)
        
        print("\nRemember: Each rejection is a valuable learning opportunity, not a reason to discard all your preparation.")
        print("Analyze, adapt, and improve!")

class Job:
    def __init__(self, title, required_skills, focus_area="general"):
        self.title = title
        self.required_skills = set(required_skills)
        self.focus_area = focus_area # e.g., "technical", "behavioral", "domain-specific"

# --- Main execution ---
if __name__ == "__main__":
    # Define an applicant with initial skills and performance
    applicant = Applicant(
        name="Ayşe",
        skills=["Python", "SQL", "Data Analysis", "Communication"],
        base_interview_score=65 # Ayşe starts with a decent but not top-tier base score
    )

    # Define several jobs with different requirements
    jobs = [
        Job("Junior Data Analyst", ["Python", "SQL", "Data Analysis", "Excel"], "technical"),
        Job("Business Intelligence Dev", ["SQL", "Data Visualization", "Communication"], "behavioral"),
        Job("Python Developer", ["Python", "Django", "Git", "Problem Solving"], "technical"),
        Job("Data Scientist Intern", ["Python", "Statistics", "Machine Learning"], "technical")
    ]

    # Simulate application process for multiple jobs
    for job in jobs:
        applicant.apply_for_job(job)

    # Analyze rejections and suggest improvements based on the accumulated history
    applicant.analyze_rejections_and_suggest_improvements()

    # --- Simulate Ayşe improving based on the feedback ---
    print("\n" + "="*50)
    print("Ayşe decides to improve based on the analysis and applies again!")
    print("="*50)
    # Ayşe adds a new skill and slightly improves her base performance
    applicant.skills.add("Problem Solving") # Targeted improvement based on common tech feedback
    applicant.base_interview_score += 5 # General interview practice
    print(f"Ayşe's updated skills: {', '.join(applicant.skills)}")
    print(f"Ayşe's updated base interview score: {applicant.base_interview_score}")

    # Apply for a new job or re-apply for a suitable one with improved profile
    new_job = Job("Mid-level Data Analyst", ["Python", "SQL", "Data Analysis", "Problem Solving", "Communication"], "technical")
    applicant.apply_for_job(new_job)

    # Final analysis after improvement and new application
    applicant.analyze_rejections_and_suggest_improvements()

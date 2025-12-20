import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

print("Starting script...")

# ---------------- PARAMETERS ----------------
num_candidates = 2000
num_jobs = 500
num_applications = 5000
num_matches = 1000

# ---------------- NEW DEPARTMENTS ----------------
departments = ["Software Development", "Data Science", "Cloud Services", "Cybersecurity", "Business Intelligence", "Project Management", "HR Talent", "Finance Accounting", "Marketing Communications", "Sales Customer Success", "Operations Logistics", "Quality Assurance", "Product Management", "Research Innovation", "Design UXUI", "Legal Compliance", "DevOps Infrastructure", "AIML Research", "Analytics Insights", "Support Helpdesk", "Procurement Supply Chain", "Internal Audit", "Training Development", "Strategy Planning", "Risk Management", "Facilities Administration", "Networking IT", "Content Media", "Public Relations Events", "Advanced Analytics"]

# ---------------- SKILLS ----------------
skills_pool = ["Python", "SQL", "Java", "C++", "JavaScript", "Power BI", "Excel", "Machine Learning", "Deep Learning", "NLP", "Communication", "Leadership", "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Tableau", "Snowflake", "ETL", "Data Modeling", "Linux", "Git", "Agile", "Networking", "Security"]

# ---------------- JOB TITLES ----------------
job_titles = ["Data Analyst", "Software Engineer", "Machine Learning Engineer", "Project Manager", "Cloud Architect", "Business Analyst", "DevOps Engineer", "Data Scientist", "Backend Developer", "Frontend Developer"]

# ---------------- DEPARTMENT SKILLS ----------------
department_skills = {
    "Software Development": ["Python", "Java", "C++", "Git"],
    "Data Science": ["Python", "SQL", "Machine Learning", "Deep Learning"],
    "Cloud Services": ["AWS", "Azure", "GCP", "Docker"],
    "Cybersecurity": ["Security", "Networking", "Linux"],
    "Business Intelligence": ["SQL", "Power BI", "Tableau", "Excel"],
    "Project Management": ["Leadership", "Agile", "Communication"],
    "HR Talent": ["Communication", "Leadership"],
    "Finance Accounting": ["Excel", "SQL"],
    "Marketing Communications": ["Communication", "Leadership"],
    "Sales Customer Success": ["Communication", "Excel"],
    "Operations Logistics": ["Excel", "Power BI"],
    "Quality Assurance": ["Excel", "Python"],
    "Product Management": ["Leadership", "Communication"],
    "Research Innovation": ["Python", "Machine Learning"],
    "Design UXUI": ["Communication", "Leadership"],
    "Legal Compliance": ["Communication"],
    "DevOps Infrastructure": ["Docker", "Kubernetes", "AWS"],
    "AIML Research": ["Python", "Machine Learning", "Deep Learning"],
    "Analytics Insights": ["SQL", "Power BI", "Tableau"],
    "Support Helpdesk": ["Networking", "Linux"],
    "Procurement Supply Chain": ["Excel", "Power BI"],
    "Internal Audit": ["Excel", "SQL"],
    "Training Development": ["Communication", "Leadership"],
    "Strategy Planning": ["Leadership", "Excel"],
    "Risk Management": ["Excel", "SQL"],
    "Facilities Administration": ["Excel"],
    "Networking IT": ["Networking", "Linux"],
    "Content Media": ["Communication"],
    "Public Relations Events": ["Communication", "Leadership"],
    "Advanced Analytics": ["Python", "SQL", "Machine Learning"]
}

# ---------------- HELPER ----------------
def safe_sample(skills, k):
    if len(skills) >= k:
        return random.sample(skills, k)
    return skills + random.sample(skills_pool, k - len(skills))

def fast_fake(n, method):
    return [method() for _ in range(n)]

# ---------------- CANDIDATES ----------------
print("Generating candidates...")
df_candidates = pd.DataFrame({
    "CandidateID": np.arange(1, num_candidates + 1),
    "CandidateName": fast_fake(num_candidates, fake.name),
    "ExperienceYears": np.round(np.random.uniform(0.5, 15, num_candidates), 1),
    "Location": fast_fake(num_candidates, fake.city),
    "Education": np.random.choice(["B.Tech", "M.Tech", "MBA", "B.Sc", "M.Sc", "PhD"], num_candidates),
    "ResumeScore": np.round(np.random.uniform(40, 100, num_candidates), 2)
})

# ---------------- JOBS ----------------
print("Generating jobs...")
job_depts = np.random.choice(departments, num_jobs)
df_jobs = pd.DataFrame({
    "JobID": np.arange(1, num_jobs + 1),
    "JobTitle": np.random.choice(job_titles, num_jobs),
    "Department": job_depts,
    "Location": fast_fake(num_jobs, fake.city),
    "ExperienceRequired": np.round(np.random.uniform(1, 10, num_jobs), 1),
    "PostedDate": fast_fake(num_jobs, lambda: fake.date_between('-200d', 'today'))
})

# ---------------- JOB SKILLS ----------------
print("Generating job skills...")
job_skills_list = []
for i in range(num_jobs):
    dept = job_depts[i]
    relevant = department_skills.get(dept, skills_pool)
    skills = safe_sample(relevant, random.randint(3, 6))
    for s in skills:
        job_skills_list.append((i + 1, s))
df_job_skills = pd.DataFrame(job_skills_list, columns=["JobID", "RequiredSkill"])

# ---------------- CANDIDATE SKILLS ----------------
print("Generating candidate skills...")
candidate_skills_list = []
cand_departments = np.random.choice(departments, num_candidates)
for i in range(num_candidates):
    dept = cand_departments[i]
    relevant = department_skills.get(dept, skills_pool)
    skills = safe_sample(relevant, random.randint(3, 7))
    for s in skills:
        candidate_skills_list.append((i + 1, s))
df_candidate_skills = pd.DataFrame(candidate_skills_list, columns=["CandidateID", "Skill"])

# ---------------- APPLICATIONS ----------------
print("Generating applications...")
df_applications = pd.DataFrame({
    "ApplicationID": np.arange(1, num_applications + 1),
    "CandidateID": np.random.randint(1, num_candidates + 1, num_applications),
    "JobID": np.random.randint(1, num_jobs + 1, num_applications),
    "ApplicationDate": fast_fake(num_applications, lambda: fake.date_between('-180d', 'today')),
    "Status": np.random.choice(["Applied", "Shortlisted", "Interviewed", "Hired", "Rejected"], num_applications)
})

# ---------------- MATCHES ----------------
print("Generating matches...")
df_matches = pd.DataFrame({
    "MatchID": np.arange(1, num_matches + 1),
    "CandidateID": np.random.randint(1, num_candidates + 1, num_matches),
    "JobID": np.random.randint(1, num_jobs + 1, num_matches),
    "SimilarityScore": np.round(np.random.uniform(50, 100, num_matches), 2)
})

# ---------------- SYSTEM METRICS ----------------
print("Generating system metrics...")
df_metrics = pd.DataFrame({
    "MetricID": np.arange(1, 101),
    "MetricName": np.random.choice(["API Latency", "Match Computation Time", "DB Query Time", "System Load"], 100),
    "MetricValue": np.round(np.random.uniform(10, 500, 100), 2),
    "DateRecorded": fast_fake(100, lambda: fake.date_between('-120d', 'today'))
})

# ---------------- EXPORT CSV ----------------
print("Saving CSV files...")
df_candidates.to_csv("Candidates.csv", index=False)
df_jobs.to_csv("Jobs.csv", index=False)
df_candidate_skills.to_csv("CandidateSkills.csv", index=False)
df_job_skills.to_csv("JobSkills.csv", index=False)
df_applications.to_csv("Applications.csv", index=False)
df_matches.to_csv("Matches.csv", index=False)
df_metrics.to_csv("SystemMetrics.csv", index=False)

print("ALL DATASETS GENERATED SUCCESSFULLY!")

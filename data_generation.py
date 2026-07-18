"""Generate validated synthetic data for a recruitment analytics dashboard.

This project is for analytics and data-engineering practice. It creates
synthetic records only and must not be used to make real hiring decisions.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


DEPARTMENT_SKILLS = {
    "Software Development": ["Python", "Java", "JavaScript", "Git"],
    "Data Science": ["Python", "SQL", "Machine Learning", "Statistics"],
    "Cloud Services": ["AWS", "Azure", "GCP", "Docker"],
    "Cybersecurity": ["Security", "Networking", "Linux", "Risk Management"],
    "Business Intelligence": ["SQL", "Power BI", "Tableau", "Data Modeling"],
    "Project Management": ["Leadership", "Agile", "Communication", "Planning"],
    "HR Talent": ["Communication", "Recruiting", "Leadership", "Analytics"],
    "Finance Accounting": ["Excel", "SQL", "Financial Analysis", "Power BI"],
    "Operations Logistics": ["Excel", "Power BI", "Process Improvement", "SQL"],
    "Quality Assurance": ["Python", "Testing", "Automation", "SQL"],
    "Product Management": ["Leadership", "Communication", "Analytics", "Agile"],
    "DevOps Infrastructure": ["Docker", "Kubernetes", "AWS", "Linux"],
    "AI/ML Research": ["Python", "Machine Learning", "Deep Learning", "NLP"],
    "Analytics Insights": ["SQL", "Power BI", "Tableau", "Statistics"],
    "Support Helpdesk": ["Networking", "Linux", "Communication", "ITSM"],
}

SKILLS_POOL = sorted({skill for skills in DEPARTMENT_SKILLS.values() for skill in skills})

JOB_TITLES = [
    "Data Analyst",
    "Data Engineer",
    "Software Engineer",
    "Machine Learning Engineer",
    "Project Manager",
    "Cloud Engineer",
    "Business Analyst",
    "DevOps Engineer",
    "Data Scientist",
    "Product Analyst",
]

APPLICATION_STATUSES = ["Applied", "Screened", "Interviewed", "Offered", "Hired", "Rejected"]

FIRST_NAMES = [
    "Avery",
    "Cameron",
    "Casey",
    "Devon",
    "Jordan",
    "Kai",
    "Morgan",
    "Parker",
    "Quinn",
    "Riley",
    "Robin",
    "Sam",
    "Taylor",
]

LAST_NAMES = [
    "Adams",
    "Bennett",
    "Chen",
    "Davis",
    "Diaz",
    "Foster",
    "Gupta",
    "Johnson",
    "Kim",
    "Martinez",
    "Patel",
    "Rivera",
    "Williams",
]

LOCATIONS = [
    "Atlanta",
    "Austin",
    "Boston",
    "Chicago",
    "Dallas",
    "Denver",
    "Los Angeles",
    "New York",
    "Phoenix",
    "San Francisco",
    "Seattle",
    "St. Louis",
]


@dataclass(frozen=True)
class Config:
    """Controls dataset size and reproducibility."""

    seed: int = 42
    candidates: int = 2_000
    jobs: int = 500
    applications: int = 5_000
    matches: int = 1_000
    users: int = 25
    system_metrics: int = 100
    as_of_date: date = date(2025, 12, 1)


def _random_dates(
    rng: np.random.Generator,
    count: int,
    end_date: date,
    lookback_days: int,
) -> list[date]:
    offsets = rng.integers(0, lookback_days + 1, size=count)
    return [end_date - timedelta(days=int(offset)) for offset in offsets]


def _sample_skills(
    randomizer: random.Random,
    department: str,
    minimum: int,
    maximum: int,
) -> list[str]:
    preferred = DEPARTMENT_SKILLS.get(department, SKILLS_POOL)
    count = randomizer.randint(minimum, maximum)
    candidates = list(dict.fromkeys(preferred + SKILLS_POOL))
    return randomizer.sample(candidates, k=min(count, len(candidates)))


def _synthetic_names(randomizer: random.Random, count: int) -> list[str]:
    return [
        f"{randomizer.choice(FIRST_NAMES)} {randomizer.choice(LAST_NAMES)}"
        for _ in range(count)
    ]


def _synthetic_locations(randomizer: random.Random, count: int) -> list[str]:
    return [randomizer.choice(LOCATIONS) for _ in range(count)]


def generate_datasets(config: Config = Config()) -> dict[str, pd.DataFrame]:
    """Create eight related, deterministic synthetic datasets."""

    if min(
        config.candidates,
        config.jobs,
        config.applications,
        config.matches,
        config.users,
        config.system_metrics,
    ) <= 0:
        raise ValueError("All dataset sizes must be positive integers.")

    rng = np.random.default_rng(config.seed)
    randomizer = random.Random(config.seed)

    departments = list(DEPARTMENT_SKILLS)

    candidate_departments = rng.choice(departments, size=config.candidates)
    candidates = pd.DataFrame(
        {
            "CandidateID": np.arange(1, config.candidates + 1),
            "CandidateName": _synthetic_names(randomizer, config.candidates),
            "DepartmentInterest": candidate_departments,
            "ExperienceYears": np.round(rng.uniform(0, 15, config.candidates), 1),
            "Location": _synthetic_locations(randomizer, config.candidates),
            "Education": rng.choice(
                ["Associate", "Bachelor", "Master", "Doctorate"],
                size=config.candidates,
                p=[0.08, 0.56, 0.32, 0.04],
            ),
            "ResumeScore": np.round(rng.uniform(40, 100, config.candidates), 2),
        }
    )

    job_departments = rng.choice(departments, size=config.jobs)
    jobs = pd.DataFrame(
        {
            "JobID": np.arange(1, config.jobs + 1),
            "JobTitle": rng.choice(JOB_TITLES, size=config.jobs),
            "Department": job_departments,
            "Location": _synthetic_locations(randomizer, config.jobs),
            "ExperienceRequired": np.round(rng.uniform(0, 10, config.jobs), 1),
            "PostedDate": _random_dates(rng, config.jobs, config.as_of_date, 200),
        }
    )

    candidate_skill_rows: list[tuple[int, str]] = []
    for candidate_id, department in enumerate(candidate_departments, start=1):
        for skill in _sample_skills(randomizer, str(department), 3, 7):
            candidate_skill_rows.append((candidate_id, skill))
    candidate_skills = pd.DataFrame(
        candidate_skill_rows,
        columns=["CandidateID", "Skill"],
    )

    job_skill_rows: list[tuple[int, str]] = []
    for job_id, department in enumerate(job_departments, start=1):
        for skill in _sample_skills(randomizer, str(department), 3, 6):
            job_skill_rows.append((job_id, skill))
    job_skills = pd.DataFrame(job_skill_rows, columns=["JobID", "RequiredSkill"])

    user_roles = rng.choice(
        ["Recruiter", "Recruiting Manager", "System Analyst"],
        size=config.users,
        p=[0.72, 0.16, 0.12],
    )
    users = pd.DataFrame(
        {
            "UserID": np.arange(1, config.users + 1),
            "UserName": _synthetic_names(randomizer, config.users),
            "Role": user_roles,
            "BusinessUnit": rng.choice(departments, size=config.users),
            "Active": rng.choice([True, False], size=config.users, p=[0.92, 0.08]),
        }
    )

    applications = pd.DataFrame(
        {
            "ApplicationID": np.arange(1, config.applications + 1),
            "CandidateID": rng.integers(1, config.candidates + 1, config.applications),
            "JobID": rng.integers(1, config.jobs + 1, config.applications),
            "RecruiterID": rng.integers(1, config.users + 1, config.applications),
            "ApplicationDate": _random_dates(
                rng,
                config.applications,
                config.as_of_date,
                180,
            ),
            "Status": rng.choice(
                APPLICATION_STATUSES,
                size=config.applications,
                p=[0.28, 0.18, 0.14, 0.06, 0.08, 0.26],
            ),
        }
    )

    matches = pd.DataFrame(
        {
            "MatchID": np.arange(1, config.matches + 1),
            "CandidateID": rng.integers(1, config.candidates + 1, config.matches),
            "JobID": rng.integers(1, config.jobs + 1, config.matches),
            "SimilarityScore": np.round(rng.uniform(50, 100, config.matches), 2),
            "ScoringVersion": rng.choice(["v1.0", "v1.1"], size=config.matches),
        }
    )

    system_metrics = pd.DataFrame(
        {
            "MetricID": np.arange(1, config.system_metrics + 1),
            "MetricName": rng.choice(
                [
                    "API Latency",
                    "Match Computation Time",
                    "Data Refresh Duration",
                    "Validation Failure Count",
                ],
                size=config.system_metrics,
            ),
            "MetricValue": np.round(rng.uniform(5, 500, config.system_metrics), 2),
            "RecordedDate": _random_dates(
                rng,
                config.system_metrics,
                config.as_of_date,
                120,
            ),
        }
    )

    datasets = {
        "Candidates": candidates,
        "CandidateSkills": candidate_skills,
        "Applications": applications,
        "Jobs": jobs,
        "JobSkills": job_skills,
        "Matches": matches,
        "Users": users,
        "SystemMetrics": system_metrics,
    }
    validate_datasets(datasets)
    return datasets


def validate_datasets(datasets: dict[str, pd.DataFrame]) -> None:
    """Raise ValueError when a primary-key, foreign-key, or range check fails."""

    required = {
        "Candidates",
        "CandidateSkills",
        "Applications",
        "Jobs",
        "JobSkills",
        "Matches",
        "Users",
        "SystemMetrics",
    }
    missing = required.difference(datasets)
    if missing:
        raise ValueError(f"Missing datasets: {', '.join(sorted(missing))}")

    errors: list[str] = []

    for dataset_name, key in {
        "Candidates": "CandidateID",
        "Applications": "ApplicationID",
        "Jobs": "JobID",
        "Matches": "MatchID",
        "Users": "UserID",
        "SystemMetrics": "MetricID",
    }.items():
        frame = datasets[dataset_name]
        if frame[key].isna().any():
            errors.append(f"{dataset_name}.{key} contains null values")
        if not frame[key].is_unique:
            errors.append(f"{dataset_name}.{key} is not unique")

    foreign_keys = [
        ("CandidateSkills", "CandidateID", "Candidates", "CandidateID"),
        ("JobSkills", "JobID", "Jobs", "JobID"),
        ("Applications", "CandidateID", "Candidates", "CandidateID"),
        ("Applications", "JobID", "Jobs", "JobID"),
        ("Applications", "RecruiterID", "Users", "UserID"),
        ("Matches", "CandidateID", "Candidates", "CandidateID"),
        ("Matches", "JobID", "Jobs", "JobID"),
    ]
    for child_name, child_key, parent_name, parent_key in foreign_keys:
        child_values = set(datasets[child_name][child_key])
        parent_values = set(datasets[parent_name][parent_key])
        if not child_values.issubset(parent_values):
            errors.append(
                f"{child_name}.{child_key} contains values missing from "
                f"{parent_name}.{parent_key}"
            )

    range_checks = [
        ("Candidates", "ResumeScore", 0, 100),
        ("Candidates", "ExperienceYears", 0, 60),
        ("Jobs", "ExperienceRequired", 0, 60),
        ("Matches", "SimilarityScore", 0, 100),
    ]
    for dataset_name, column, minimum, maximum in range_checks:
        if not datasets[dataset_name][column].between(minimum, maximum).all():
            errors.append(
                f"{dataset_name}.{column} contains values outside "
                f"{minimum}–{maximum}"
            )

    if errors:
        raise ValueError("Data validation failed:\n- " + "\n- ".join(errors))


def write_datasets(
    datasets: dict[str, pd.DataFrame],
    output_dir: Path | str = Path("data"),
) -> list[Path]:
    """Write datasets to CSV and return the generated paths."""

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for dataset_name, frame in datasets.items():
        path = target / f"{dataset_name}.csv"
        frame.to_csv(path, index=False)
        written.append(path)
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate validated synthetic recruitment analytics datasets."
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--candidates", type=int, default=2_000)
    parser.add_argument("--jobs", type=int, default=500)
    parser.add_argument("--applications", type=int, default=5_000)
    parser.add_argument("--matches", type=int, default=1_000)
    parser.add_argument("--users", type=int, default=25)
    parser.add_argument("--system-metrics", type=int, default=100)
    parser.add_argument(
        "--as-of-date",
        type=date.fromisoformat,
        default=date(2025, 12, 1),
        help="Reference date in YYYY-MM-DD format (default: 2025-12-01).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = Config(
        seed=args.seed,
        candidates=args.candidates,
        jobs=args.jobs,
        applications=args.applications,
        matches=args.matches,
        users=args.users,
        system_metrics=args.system_metrics,
        as_of_date=args.as_of_date,
    )
    datasets = generate_datasets(config)
    paths = write_datasets(datasets, args.output_dir)

    print(f"Generated {len(paths)} validated datasets in {args.output_dir.resolve()}:")
    for path in paths:
        print(f"- {path.name}: {len(datasets[path.stem]):,} rows")


if __name__ == "__main__":
    main()

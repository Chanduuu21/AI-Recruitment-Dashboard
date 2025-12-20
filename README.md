# AI Recruitment Dashboard

## Project Overview

An AI-powered recruitment dashboard designed to streamline hiring workflows, enhance candidate evaluation, and monitor system performance. This comprehensive analytics platform provides data-driven insights for talent acquisition teams to make informed hiring decisions.

**Academic Project | Master's in Information Technology**  
**Project Duration:** May 2025 - December 2025

---

## Key Features

### 1. Recruiter Insights
- Application volume tracking by recruiter
- Candidate quality assessment through resume score distribution
- Skill pattern analysis and role suitability matching
- KPI cards for average experience, match scores, and application load

### 2. Candidate Experience
- Comprehensive candidate profile overview (skills, education, experience)
- Communication timeline tracking
- Resume strength visualization
- Experience and skill fit analysis charts

### 3. Hiring Pipeline Overview
- Complete application funnel (Applied → Screened → Interviewed → Hired)
- Drop-off rate analysis at each stage
- Time-to-hire trend monitoring
- Department and job title comparisons

### 4. System Metrics
- AI match score performance tracking
- System latency monitoring
- Computation time analysis
- Detailed log summaries for debugging

---

## Technologies Used

- **Programming Language:** Python 3.x
- **Data Processing:** Pandas, NumPy
- **Data Generation:** Faker library
- **Visualization:** Power BI Desktop
- **Data Analysis:** DAX (Data Analysis Expressions)
- **Version Control:** Git & GitHub

---

## Datasets

The dashboard integrates **8 synthetic datasets:**

1. **Candidates** - Personal information, education, experience, resume scores
2. **CandidateSkills** - Skill mappings for each candidate
3. **Applications** - Application records with status tracking
4. **Jobs** - Job postings with requirements
5. **JobSkills** - Required skills for each position
6. **Matches** - AI-driven candidate-job similarity scores
7. **Users** - Recruiter and system user information
8. **SystemMetrics** - Performance monitoring data

---

## Installation & Setup

### Prerequisites
```bash
python --version  # Python 3.7 or higher
pip --version
```

### Install Dependencies
```bash
pip install pandas numpy faker
```

### Generate Synthetic Data
```bash
python data_generation.py
```

This will create 8 CSV files:
- `Candidates.csv` (2,000+ records)
- `Jobs.csv` (500+ records)
- `Applications.csv` (4,000+ records)
- `CandidateSkills.csv`
- `JobSkills.csv`
- `Matches.csv`
- `Users.csv`
- `SystemMetrics.csv`

### Power BI Setup
1. Open Power BI Desktop
2. Import all generated CSV files
3. Create relationships between tables (CandidateID, JobID as primary keys)
4. Load the dashboard visualizations

---

## Key Performance Indicators (KPIs)

- **Average Time to Hire** - Tracks hiring efficiency
- **Hiring Funnel Conversion Rate** - Monitors candidate progression
- **Drop-off Rate** - Identifies bottlenecks in hiring stages
- **Resume Score Distribution** - Evaluates candidate quality
- **Candidate Match Score** - AI-driven job fit analysis
- **System Latency** - Performance monitoring

---

## Academic Context

### Target User Profile
**Talent Acquisition Lead / Recruitment Manager** at medium-to-large organizations

**Key Responsibilities:**
- Monitoring overall hiring performance
- Supporting recruiters with data-driven analytics
- Ensuring efficient candidate pipeline flow
- Improving candidate experience
- Identifying operational trends and bottlenecks

### Relevant Coursework
- **Data Visualization & Storytelling** - Dashboard design and insight communication
- **Information Retrieval** - Multi-table data relationships and access patterns
- **Enterprise Architecture** - System component identification and structural alignment
- **Business Analytics** - KPI development and decision-support design
- **Machine Learning Foundations** - AI scoring and similarity matching

---

## Security & Ethics

### Technical Safeguards
- Access permission controls to prevent data leakage
- Audit trails for metric updates and model changes
- System monitoring for latency spikes and failures
- Regular validation of job-skill mappings

### Ethical Considerations
- **Fairness:** Balanced training data to reduce AI bias
- **Transparency:** Clear explanation of AI-driven scoring mechanisms
- **Privacy:** Secure handling of applicant data
- **Non-discrimination:** Avoiding biased outcomes in candidate evaluation

---

## Business Impact

- Faster candidate screening through AI similarity and resume scoring
- Reduced time-to-hire with trend monitoring and bottleneck identification
- Skill gap analysis for targeted recruitment strategies
- Improved recruiter productivity with performance tracking
- Enhanced candidate experience through transparent evaluation
- Data-driven hiring decisions replacing intuition-based approaches

---

## Future Enhancements

- Integration with live ATS (Applicant Tracking Systems)
- Advanced AI similarity models using NLP
- Predictive analytics for hiring demand forecasting
- Real-time recruiter alerts and notifications
- Bias detection algorithms
- Mobile dashboard access

---

## Project Structure

```
AI-Recruitment-Dashboard/
│
├── data_generation.py          # Synthetic data generation script
├── draft.py                    # Advanced application logic script
├── README.md                   # Project documentation
├── Final-Project-Report.docx   # Detailed project report
├── AI_Recruitment_Final_Report.docx  # Comprehensive analysis
│
├── data/                       # Generated CSV files (after running scripts)
│   ├── Candidates.csv
│   ├── Jobs.csv
│   ├── Applications.csv
│   ├── CandidateSkills.csv
│   ├── JobSkills.csv
│   ├── Matches.csv
│   ├── Users.csv
│   └── SystemMetrics.csv
│
└── dashboard/                  # Power BI dashboard files
    └── RecruitmentDashboard.pbix
```

---

## Author

**Chandra Sai Ettneni**  
Master's in Information Technology  
GitHub: [@Chanduuu21](https://github.com/Chanduuu21)  
LinkedIn: [Chandra Sai Ettneni](https://linkedin.com/in/chanduuu21)

---

## License

This project was developed as an academic assignment. Feel free to use it for educational purposes.

---

## Acknowledgments

- Faker Library for realistic synthetic data generation
- Power BI Community for dashboard design inspiration
- University Faculty for guidance on business analytics and data visualization

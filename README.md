
# Job Recommendation System

This repository contains a simple job recommendation system built using Flask (for the backend) and Streamlit (for the frontend). This Job Recommendation System is designed to provide users with tailored job suggestions based on their skillset, job preferences, and experience level. The system allows users to create a profile with details about their skills, preferred job roles, location preferences, and job type (e.g., full-time, part-time). Once the profile is created, the system fetches relevant job postings from a backend API and scores them based on the user's profile.

## Features
- **User Profile Input**: Users can input their name, skills, job preferences (roles, locations, type), and experience level.
- **Job Recommendations**: The system fetches job postings from a backend service and recommends the top 5 jobs based on a scoring mechanism.
- **Skill Matching**: The system displays both matching and missing skills for each recommended job, helping users identify areas for improvement.
- **Flexible Job Preferences**: Users can select job types, desired roles, and specify location preferences (remote, on-site, hybrid).
- **Backend Integration**: The application fetches job data from a Flask backend, which reads from a SQLite database populated with job postings from a JSON file.

## Tech Stack
- **Frontend**: Streamlit, Python
- **Backend**: Flask, SQLite

## How it Works

1. **User Input**:
   The user provides the following details through the Streamlit interface:
   - Name
   - Skills (from a pre-populated list fetched from the backend)
   - Desired Job Roles
   - Preferred Location (Remote, On-site, Hybrid)
   - Job Type (Full-time, Part-time, Internship, Contract)
   - Experience Level (Entry-level, Mid-level, Senior-level)

2. **Job Recommendations**:
   Once the user submits their profile, the frontend sends a request to the Flask backend with the user’s details. The backend processes the user's profile and fetches jobs from the database. A scoring mechanism is used to rank jobs based on the following criteria:
   - **Skill Match**: Matches between user skills and required job skills.
   - **Experience Level**: Match between the user’s experience and the job's requirements.
   - **Location Match**: Whether the job’s location aligns with the user's preferences.
   - **Job Type Match**: Whether the job type matches the user's preferred type (e.g., full-time, part-time).

   The system returns the top 5 jobs, along with matching and missing skills, to the frontend.

## Installation and Setup

### Prerequisites:
- Python 3.x
- Flask
- Streamlit
- SQLite3

### 1. Clone the Repository
```bash
git clone https://github.com/mohammedazif/job-recommendation-system.git
cd job-recommendation-system
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server
First, initialize the database and start the Flask server:
```bash
python backend.py
```
The backend server will be accessible at `http://127.0.0.1:5000/`.

### 4. Start the Streamlit Frontend
In a separate terminal window, run:
```bash
streamlit run frontend.py
```
The frontend will be available in your browser at `http://localhost:8501/`.

## Sample Job Posting Data
The job postings are stored in a `job_postings.json` file, which is loaded into an SQLite database when the backend server starts. Here’s a sample of how the job data is structured:

```json
[
  {
    "job_id": 1,
    "job_title": "Software Engineer",
    "company": "Tech Solutions Inc.",
    "required_skills": ["Python", "Flask", "JavaScript"],
    "location": "New York",
    "job_type": "Full-time",
    "experience_level": "Mid-level"
  },
  {
    "job_id": 2,
    "job_title": "Data Scientist",
    "company": "Data Corp",
    "required_skills": ["Python", "Machine Learning", "Statistics"],
    "location": "Remote",
    "job_type": "Part-time",
    "experience_level": "Entry-level"
  }
]
```

## APIs

### 1. `/recommend` (POST)
Endpoint for receiving job recommendations based on the user profile.

**Request Body**:
```json
{
  "name": "Jane Doe",
  "skills": ["Python", "Flask", "Machine Learning"],
  "experience_level": "Mid-level",
  "preferences": {
    "desired_roles": ["Data Scientist", "Software Engineer"],
    "locations": ["Remote", "New York"],
    "job_type": "Full-time"
  }
}
```

**Response**:
```json
[
    {
        "company": "Tech Solutions Inc.",
        "experience_level": "Mid-level",
        "job_title": "Software Engineer",
        "job_type": "Full-time",
        "location": "New York",
        "required_skills": ["Python", "Flask", "JavaScript"],
        "score": 15
    },
    {
        "company": "Data Corp",
        "experience_level": "Entry-level",
        "job_title": "Data Scientist",
        "job_type": "Part-time",
        "location": "Remote",
        "required_skills": ["Python", "Machine Learning", "Statistics"],
        "score": 9
    }
]
```

### 2. `/metadata` (GET)
Fetches available skills and job roles from the database.

**Response**:
```json
{
  "skills": ["Python", "Flask", "JavaScript", "Machine Learning", ...],
  "job_roles": ["Software Engineer", "Data Scientist", ...]
}
```

## Future Enhancements
- **User Authentication**: Allow users to log in and save their profiles for personalized job recommendations.
- **Advanced Filtering**: Add options to filter job recommendations by company, salary range, or industry.
- **Email Notifications**: Send users email alerts when new job postings matching their profile are added to the system.

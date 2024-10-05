from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Database initialization (Run once)
def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY, 
                  job_title TEXT, 
                  company TEXT, 
                  required_skills TEXT, 
                  location TEXT, 
                  job_type TEXT, 
                  experience_level TEXT)''')

    # Insert mock data from the JSON file
    try:
        with open('job_postings.json', 'r') as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print("job_postings.json not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from job_postings.json.")
        return

    for job in jobs:
        c.execute('''INSERT OR REPLACE INTO jobs 
                     (id, job_title, company, required_skills, location, job_type, experience_level) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (job['job_id'], job['job_title'], job['company'], 
                   json.dumps(job['required_skills']), job['location'], 
                   job['job_type'], job['experience_level']))

    conn.commit()
    conn.close()

# Function to generate job recommendations based on user profile
def get_job_recommendations(user_profile):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    # Fetch all jobs
    c.execute("SELECT * FROM jobs")
    all_jobs = c.fetchall()

    # Scoring mechanism
    scored_jobs = []
    user_skills = set(user_profile['skills'])
    desired_roles = [role.lower() for role in user_profile['preferences']['desired_roles']]
    preferred_locations = set(user_profile['preferences']['locations'])
    preferred_job_type = user_profile['preferences']['job_type']
    user_experience_level = user_profile['experience_level']

    for job in all_jobs:
        job_title = job[1]
        job_skills = set(json.loads(job[3]))  # job[3] is required_skills

        # Check if the job title matches any of the desired roles and if there's at least one matching skill
        if any(role in job_title.lower() for role in desired_roles) and user_skills.intersection(job_skills):
            score = 0
            job_location = job[4]
            job_type = job[5]
            job_experience_level = job[6]

            # Score based on matching skills
            skill_match = len(job_skills.intersection(user_skills))
            score += skill_match * 3  # Increase weight for skill match (max 9 if 3 skills match)

            # Score based on experience level match
            if job_experience_level == user_experience_level:
                score += 4  # Experience level match (max 4)

            # Score based on location match
            if job_location in preferred_locations:
                score += 3  # Location match (max 3)

            # Score based on job type match
            if job_type == preferred_job_type:
                score += 2  # Job type match (max 2)

            # Ensure the score does not exceed 20
            score = min(score, 20)

            scored_jobs.append((job, score))

    # Sort jobs by score and get top 5
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    top_jobs = scored_jobs[:5]

    # Format recommendations
    recommendations = []
    for job, score in top_jobs:
        recommendations.append({
            "job_title": job[1],
            "company": job[2],
            "required_skills": json.loads(job[3]),
            "location": job[4],
            "job_type": job[5],
            "experience_level": job[6],
            "score": score  
        })

    conn.close()
    return recommendations

# Route for job recommendations
@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    user_profile = request.json
    try:
        recommendations = get_job_recommendations(user_profile)
        return jsonify(recommendations)
    except Exception as e:
        print(f"Error during job recommendation: {str(e)}")
        return jsonify({"error": str(e)}), 400

# API to get all available skills and job roles
@app.route('/metadata', methods=['GET'])
def get_metadata():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    # Fetch all jobs
    c.execute("SELECT required_skills, job_title FROM jobs")
    all_jobs = c.fetchall()

    skills = set()
    job_roles = set()

    for job in all_jobs:
        job_skills = set(json.loads(job[0]))
        skills.update(job_skills)
        job_roles.add(job[1])

    conn.close()

    return jsonify({
        "skills": list(skills),
        "job_roles": list(job_roles)
    })

# Basic route to check if the server is running
@app.route('/')
def home():
    return "Job Recommendation System is running."

if __name__ == '__main__':
    init_db()  # Initialize the database when the server starts
    print("Database initialized.")
    app.run(debug=True)
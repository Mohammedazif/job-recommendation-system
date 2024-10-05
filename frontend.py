import streamlit as st
import requests

# Title of the application
st.title("Job Recommendation System")

# User input for name
name = st.text_input("Enter your name:")

# Fetch available skills and job roles from the Flask backend
metadata_url = "http://127.0.0.1:5000/metadata"
response = requests.get(metadata_url)
if response.status_code == 200:
    metadata = response.json()
    available_skills = metadata["skills"]
    available_job_roles = metadata["job_roles"]
else:
    st.error("Error fetching metadata from the backend.")
    available_skills = []
    available_job_roles = []

# User input for skills and job preferences
st.header("User Profile")
selected_skills = st.multiselect("Select your skills:", available_skills)
desired_roles = st.multiselect("Select your desired job roles:", available_job_roles)
preferred_location = st.selectbox("Select preferred location type:", ["Remote", "On-site", "Hybrid"])

# Conditional input for specific location
if preferred_location != "Remote":
    specific_location = st.text_input("Enter preferred location:")
else:
    specific_location = "Remote"

preferred_job_type = st.selectbox("Select job type:", ["Full-time", "Part-time", "Internship", "Contract"])
user_experience_level = st.selectbox("Select experience level:", ["Entry-level", "Mid-level", "Senior-level"])

# Button to submit the user profile
if st.button("Get Job Recommendations"):
    if not name:
        st.error("Please enter your name.")
    elif not selected_skills:
        st.error("Please select at least one skill.")
    elif not desired_roles:
        st.error("Please select at least one desired job role.")
    else:
        user_profile = {
            "name": name,
            "skills": selected_skills,
            "preferences": {
                "desired_roles": desired_roles,
                "locations": [specific_location],
                "job_type": preferred_job_type
            },
            "experience_level": user_experience_level
        }

        with st.spinner('Fetching job recommendations...'):
            # Send request to Flask backend
            recommendation_url = "http://127.0.0.1:5000/recommend"
            response = requests.post(recommendation_url, json=user_profile)

        if response.status_code == 200:
            recommendations = response.json()
            if recommendations:
                st.header("Recommended Jobs:")
                for job in recommendations:
                    st.subheader(f"{job['job_title']} at {job['company']}")
                    st.write(f"Location: {job['location']}")
                    st.write(f"Job Type: {job['job_type']}")
                    st.write(f"Experience Level: {job['experience_level']}")
                    st.write(f"Required Skills: {', '.join(job['required_skills'])}")
                    st.write(f"Match Score: {job['score']}/20")
                    
                    # Display matching and missing skills
                    matching_skills = set(selected_skills) & set(job['required_skills'])
                    missing_skills = set(job['required_skills']) - set(selected_skills)
                    
                    if matching_skills:
                        st.write("Matching Skills:", ", ".join(matching_skills))
                    if missing_skills:
                        st.write("Skills to Improve:", ", ".join(missing_skills))
                    
                    st.write("---")
            else:
                st.warning("No job recommendations found. Your skills may not match any available jobs for the selected roles.")
        else:
            st.error("Error fetching job recommendations from the backend.")
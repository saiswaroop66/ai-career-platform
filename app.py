import streamlit as st
import PyPDF2
import pandas as pd

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="AI Career Recommendation Platform",
    layout="wide"
)

# ---------------------------------
# CUSTOM CSS (PREMIUM UI)
# ---------------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1E1E1E;
    margin-bottom: 20px;
    box-shadow: 0px 0px 10px rgba(255,255,255,0.1);
}

.role-title {
    font-size: 28px;
    font-weight: bold;
    color: #00FFAA;
}

.salary {
    font-size: 20px;
    color: #FFD700;
}

.section-title {
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# TITLE
# ---------------------------------
st.markdown("<h1 style='text-align:center;'>🚀 AI Career Recommendation Platform</h1>", unsafe_allow_html=True)

st.write("### Upload your resume and discover the best career roles for your skills.")

# ---------------------------------
# FILE UPLOAD
# ---------------------------------
uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

# ---------------------------------
# SKILLS DATABASE
# ---------------------------------
skills_db = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "data science",
    "excel",
    "power bi",
    "communication",
    "html",
    "css",
    "javascript",
    "react",
    "streamlit",
    "flask",
    "django",
    "c++",
    "c",
    "mongodb",
    "mysql"
]

# ---------------------------------
# JOB ROLE DATABASE
# ---------------------------------
job_roles = {
    "Data Scientist": [
        "python",
        "machine learning",
        "data science",
        "sql"
    ],

    "AI Engineer": [
        "python",
        "deep learning",
        "machine learning"
    ],

    "Data Analyst": [
        "excel",
        "sql",
        "power bi"
    ],

    "Software Developer": [
        "python",
        "java",
        "sql"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react"
    ],

    "Backend Developer": [
        "python",
        "flask",
        "django",
        "mysql"
    ]
}

# ---------------------------------
# JOB IMAGES
# ---------------------------------
job_images = {
    "Data Scientist": "data.jpeg",
    "AI Engineer": "ai.jpeg",
    "Data Analyst": "analys.jpeg",
    "Software Developer": "software.jpeg",
    "Web Developer": "web.jpeg",
    "Backend Developer": "back.jpeg"
}

# ---------------------------------
# SALARY DATABASE
# ---------------------------------
salary_db = {
    "Data Scientist": "₹10 - ₹20 LPA",
    "AI Engineer": "₹12 - ₹25 LPA",
    "Data Analyst": "₹6 - ₹12 LPA",
    "Software Developer": "₹5 - ₹15 LPA",
    "Web Developer": "₹4 - ₹10 LPA",
    "Backend Developer": "₹6 - ₹14 LPA"
}

# ---------------------------------
# ROLE DESCRIPTIONS
# ---------------------------------
role_description = {
    "Data Scientist":
        "Works on AI, ML, analytics and prediction systems.",

    "AI Engineer":
        "Builds intelligent AI systems and automation tools.",

    "Data Analyst":
        "Analyzes business data and creates reports/dashboard.",

    "Software Developer":
        "Builds software applications and backend systems.",

    "Web Developer":
        "Develops websites and responsive web applications.",

    "Backend Developer":
        "Handles server-side logic, APIs and databases."
}

# ---------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------
def extract_text_from_pdf(file):

    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


# ---------------------------------
# SKILL EXTRACTION
# ---------------------------------
def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_db:

        if skill in text:
            found_skills.append(skill)

    return found_skills


# ---------------------------------
# JOB RECOMMENDATION ENGINE
# ---------------------------------
def recommend_jobs(user_skills):

    all_results = []

    for role, role_skills in job_roles.items():

        matched = 0

        for skill in role_skills:

            if skill in user_skills:
                matched += 1

        score = int((matched / len(role_skills)) * 100)

        missing = [
            skill for skill in role_skills
            if skill not in user_skills
        ]

        all_results.append({
            "Role": role,
            "Score": score,
            "Missing Skills": ", ".join(missing)
        })

    # Sort by score
    all_results = sorted(
        all_results,
        key=lambda x: x["Score"],
        reverse=True
    )

    return all_results


# ---------------------------------
# MAIN EXECUTION
# ---------------------------------
if uploaded_file:

    # Extract text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Show Resume Content
    st.markdown("<div class='section-title'>📄 Resume Content</div>", unsafe_allow_html=True)

    with st.expander("View Resume Text"):
        st.write(resume_text)

    # Extract Skills
    skills = extract_skills(resume_text)

    st.markdown("<div class='section-title'>🧠 Extracted Skills</div>", unsafe_allow_html=True)

    if skills:
        st.success(", ".join(skills))
    else:
        st.warning("No skills detected")

    # Job Recommendation
    results = recommend_jobs(skills)

    # Top Recommended Job
    top_role = results[0]["Role"]
    top_score = results[0]["Score"]
    top_missing = results[0]["Missing Skills"]

    st.markdown("<div class='section-title'>💼 Best Career Match</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(job_images[top_role], width=300)

    with col2:

        st.markdown(
            f"<div class='role-title'>{top_role}</div>",
            unsafe_allow_html=True
        )

        st.progress(top_score / 100)

        st.write(f"### 📊 Match Score: {top_score}%")

        st.markdown(
            f"<div class='salary'>💰 Salary: {salary_db[top_role]}</div>",
            unsafe_allow_html=True
        )

        st.info(role_description[top_role])

        st.error(f"⚠️ Missing Skills: {top_missing}")

    # ---------------------------------
    # TOP 3 RECOMMENDATIONS
    # ---------------------------------
    st.markdown("<div class='section-title'>🏆 Top Career Recommendations</div>", unsafe_allow_html=True)

    top3 = results[:3]

    for result in top3:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 3])

        with c1:
            st.image(job_images[result["Role"]], width=180)

        with c2:

            st.markdown(
                f"<div class='role-title'>{result['Role']}</div>",
                unsafe_allow_html=True
            )

            st.progress(result["Score"] / 100)

            st.write(f"### 📊 Match Score: {result['Score']}%")

            st.write(f"### 💰 Salary: {salary_db[result['Role']]}")

            st.info(role_description[result["Role"]])

            st.warning(f"Missing Skills: {result['Missing Skills']}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # TABLE VIEW
    # ---------------------------------
    st.markdown("<div class='section-title'>📋 All Career Matches</div>", unsafe_allow_html=True)

    df = pd.DataFrame(results)

    st.dataframe(df, use_container_width=True)

else:
    st.info("📄 Upload a resume PDF to begin.")
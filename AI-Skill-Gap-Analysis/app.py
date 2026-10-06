import re
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "job_skills.csv"

st.set_page_config(page_title="AI Skill Gap Analysis", page_icon="🎯", layout="wide")


@st.cache_data
def load_job_data():
    data = pd.read_csv(DATA_FILE)
    data.columns = [column.strip() for column in data.columns]
    data["job_role"] = data["job_role"].astype(str).str.strip()
    data["skill"] = data["skill"].astype(str).str.strip()
    return data


job_data = load_job_data()

SKILLS = [
    "Natural Language Processing", "Machine Learning", "Data Visualization",
    "Deep Learning", "JavaScript", "TensorFlow", "PyTorch", "Statistics",
    "Python", "Pandas", "NumPy", "Power BI", "Excel", "Java", "SQL",
    "HTML", "CSS", "React", "GitHub", "Git", "OOP", "APIs", "Django",
    "Spring", "NLP", "Data Analysis", "Data Science", "C++", "C"
]

ROADMAP_INFO = {
    "Python": ("Beginner", "7 days", "Variables, data types, loops, functions", "Build a Python mini-project"),
    "SQL": ("Beginner", "7 days", "SELECT, WHERE, JOIN, GROUP BY", "Solve 20 SQL queries"),
    "Statistics": ("Beginner", "7 days", "Mean, median, probability, variance", "Solve statistics exercises"),
    "Pandas": ("Beginner", "4 days", "DataFrames, filtering, grouping", "Analyze a CSV dataset"),
    "NumPy": ("Beginner", "3 days", "Arrays, indexing, calculations", "Perform numerical operations"),
    "Machine Learning": ("Intermediate", "14 days", "Regression, classification, evaluation", "Build a prediction model"),
    "Deep Learning": ("Advanced", "14 days", "Neural networks and model training", "Build a simple neural network"),
    "Data Visualization": ("Beginner", "5 days", "Charts, graphs, dashboards", "Create a data dashboard"),
    "Excel": ("Beginner", "4 days", "Formulas, functions, pivot tables", "Create a spreadsheet dashboard"),
    "Power BI": ("Beginner", "7 days", "Import data, visuals, dashboards", "Build a sales dashboard"),
    "Git": ("Beginner", "3 days", "Repositories, commits, branches", "Upload a project to GitHub"),
    "OOP": ("Beginner", "5 days", "Classes, objects, inheritance", "Build an OOP-based application"),
    "APIs": ("Intermediate", "4 days", "REST, JSON, requests", "Use an API in a mini-project"),
    "Java": ("Beginner", "7 days", "Classes, objects, collections", "Build a Java mini-project"),
    "HTML": ("Beginner", "3 days", "Tags, forms, semantic HTML", "Create a portfolio page"),
    "CSS": ("Beginner", "4 days", "Selectors, flexbox, responsive design", "Style a responsive webpage"),
    "JavaScript": ("Beginner", "7 days", "Variables, functions, DOM", "Create an interactive webpage"),
    "React": ("Intermediate", "14 days", "Components, props, state", "Build a small dashboard"),
    "Django": ("Intermediate", "14 days", "URLs, views, models", "Create a CRUD web app"),
    "Spring": ("Intermediate", "14 days", "Spring Boot and REST APIs", "Build a Java REST API"),
    "TensorFlow": ("Advanced", "14 days", "Tensors, layers, training", "Train a simple neural network"),
}


def extract_skills(text):
    found = []
    normalized_text = text.lower()
    for skill in SKILLS:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill.lower()) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, normalized_text):
            found.append(skill)
    # NLP and Natural Language Processing are equivalent for this demo.
    if "Natural Language Processing" in found and "NLP" not in found:
        found.append("NLP")
    return found


def analyze_skills(student_skills, role):
    required = job_data.loc[job_data["job_role"] == role, "skill"].tolist()
    student_lower = {skill.lower() for skill in student_skills}
    strong = [skill for skill in required if skill.lower() in student_lower]
    missing = [skill for skill in required if skill.lower() not in student_lower]
    percentage = round(100 * len(strong) / len(required)) if required else 0
    return required, strong, missing, percentage


def make_roadmap(missing):
    roadmap = []
    for skill in missing:
        level, duration, topics, practice = ROADMAP_INFO.get(
            skill, ("Beginner", "7 days", f"Learn {skill} fundamentals", f"Build a small {skill} project")
        )
        roadmap.append({
            "skill": skill,
            "level": level,
            "duration": duration,
            "topics": topics,
            "practice": practice,
        })
    return roadmap


if "result" not in st.session_state:
    st.session_state.result = None
if "completed" not in st.session_state:
    st.session_state.completed = set()

st.sidebar.title("🎯 SkillPath AI")
page = st.sidebar.radio("Navigation", ["Home", "Skill Gap Analysis", "Learning Roadmap", "About"])

st.title("🎯 AI Skill Gap Analysis")
st.caption("Find your skill gap. Build your future.")
st.write("Analyze resume skills, compare them with a target career, and get a suggested learning roadmap.")

if page == "Home":
    st.header("Student Details")
    name = st.text_input("Student name", placeholder="Enter your name")
    roles = sorted(job_data["job_role"].dropna().unique().tolist())
    role = st.selectbox("Target job role", roles)
    resume_text = st.text_area(
        "Paste resume text or list your skills",
        height=220,
        placeholder="Example: I know Python, SQL, Pandas and Excel."
    )
    st.info("This beginner version uses a local skill dictionary and does not need a paid API.")
    if st.button("🚀 Analyze My Skills", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Please enter your name.")
        elif not resume_text.strip():
            st.error("Please paste your resume text or skills.")
        else:
            detected = extract_skills(resume_text)
            required, strong, missing, percentage = analyze_skills(detected, role)
            st.session_state.result = {
                "name": name.strip(),
                "role": role,
                "detected": detected,
                "required": required,
                "strong": strong,
                "missing": missing,
                "percentage": percentage,
                "roadmap": make_roadmap(missing),
            }
            st.session_state.completed = set()
            if detected:
                st.success("Analysis completed.")
                st.write("**Skills detected:** " + ", ".join(detected))
            else:
                st.warning("No known skills were detected. Try mentioning skills such as Python, SQL, or Pandas.")
            st.caption("Open Skill Gap Analysis or Learning Roadmap from the sidebar to see results.")

elif page == "Skill Gap Analysis":
    st.header("📊 Skill Gap Analysis")
    result = st.session_state.result
    if not result:
        st.warning("Go to Home, enter your details, and analyze your skills first.")
    else:
        st.write(f"**Student:** {result['name']}  |  **Target role:** {result['role']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Skill match", f"{result['percentage']}%")
        c2.metric("Matching skills", len(result["strong"]))
        c3.metric("Missing skills", len(result["missing"]))
        st.progress(result["percentage"] / 100)
        left, right = st.columns(2)
        with left:
            st.subheader("✅ Skills found")
            if result["strong"]:
                for skill in result["strong"]:
                    st.success(skill)
            else:
                st.info("No required skills matched yet.")
        with right:
            st.subheader("❌ Skills to learn")
            if result["missing"]:
                for skill in result["missing"]:
                    st.error(skill)
            else:
                st.success("All listed skills matched!")
        with st.expander("Show all skills detected from resume"):
            st.write(", ".join(result["detected"]) if result["detected"] else "No skills detected.")

elif page == "Learning Roadmap":
    st.header("🗺️ Personalized Learning Roadmap")
    result = st.session_state.result
    if not result:
        st.warning("Analyze your skills from the Home page first.")
    elif not result["roadmap"]:
        st.success("You matched all skills listed for this role. Consider building a portfolio project.")
    else:
        st.write("Suggested order based on the missing skills. Estimated durations are illustrative.")
        for index, item in enumerate(result["roadmap"]):
            with st.container(border=True):
                st.subheader(f"Step {index + 1}: {item['skill']}")
                st.write(f"**Level:** {item['level']}  |  **Estimated time:** {item['duration']}")
                st.write(f"**Topics:** {item['topics']}")
                st.write(f"**Practice task:** {item['practice']}")
                is_done = st.checkbox("Mark as completed", key=f"complete_{index}", value=index in st.session_state.completed)
                if is_done:
                    st.session_state.completed.add(index)
                else:
                    st.session_state.completed.discard(index)
        total = len(result["roadmap"])
        completed = len(st.session_state.completed)
        progress = completed / total
        st.subheader("Progress")
        st.progress(progress)
        st.write(f"{completed} of {total} roadmap steps completed ({round(progress * 100)}%).")

else:
    st.header("About this project")
    st.write(
        "This college-project prototype uses Python, Streamlit, Pandas, regular-expression-based "
        "skill extraction, a local job-skills CSV dataset, and rule-based roadmap suggestions."
    )
    st.warning(
        "This is a prototype, not a validated hiring assessment. Skill match is calculated as "
        "the proportion of listed job skills detected in the supplied text."
    )
    st.write("To improve it later, add PDF/DOCX parsing, semantic matching with sentence-transformers, and resource links.")

st.divider()
st.caption("AI Skill Gap Analysis | CSE (Data Science) student project")

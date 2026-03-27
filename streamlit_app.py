import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Smart Study Planner + Performance Analyzer", layout="wide")

# ---------------------------
# Session state initialization
# ---------------------------
if "subjects" not in st.session_state:
    st.session_state.subjects = []

if "progress_data" not in st.session_state:
    st.session_state.progress_data = pd.DataFrame(
        columns=["Date", "Subject", "Planned Hours", "Actual Hours", "Score", "Completion %"]
    )

# ---------------------------
# Helper functions
# ---------------------------
def difficulty_weight(level: str) -> int:
    mapping = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3
    }
    return mapping.get(level, 1)

def preparation_penalty(level: str) -> int:
    mapping = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }
    return mapping.get(level, 1)

def generate_plan(subjects, hours_per_day, days_left):
    total_weight = 0
    weighted_subjects = []

    for sub in subjects:
        weight = difficulty_weight(sub["Difficulty"]) + preparation_penalty(sub["Preparation"])
        total_weight += weight
        weighted_subjects.append({
            "Subject": sub["Subject"],
            "Difficulty": sub["Difficulty"],
            "Preparation": sub["Preparation"],
            "Weight": weight
        })

    if total_weight == 0:
        return pd.DataFrame()

    plan_rows = []
    for day in range(1, days_left + 1):
        for sub in weighted_subjects:
            allocated = round((sub["Weight"] / total_weight) * hours_per_day, 2)
            plan_rows.append({
                "Day": f"Day {day}",
                "Subject": sub["Subject"],
                "Difficulty": sub["Difficulty"],
                "Preparation": sub["Preparation"],
                "Allocated Hours": allocated
            })

    return pd.DataFrame(plan_rows)

def get_ai_suggestions(progress_df):
    suggestions = []

    if progress_df.empty:
        return ["No progress data yet. Start entering your study progress to get suggestions."]

    grouped = progress_df.groupby("Subject").agg({
        "Planned Hours": "sum",
        "Actual Hours": "sum",
        "Score": "mean",
        "Completion %": "mean"
    }).reset_index()

    for _, row in grouped.iterrows():
        subject = row["Subject"]
        planned = row["Planned Hours"]
        actual = row["Actual Hours"]
        score = row["Score"]
        completion = row["Completion %"]

        if actual < planned:
            suggestions.append(f"You are behind schedule in **{subject}**. Study more hours for this subject.")
        if score < 50:
            suggestions.append(f"**{subject}** needs urgent revision. Your average score is below 50.")
        elif score < 70:
            suggestions.append(f"Focus a bit more on **{subject}** to improve your performance.")
        else:
            suggestions.append(f"Good job in **{subject}**. Keep maintaining your score.")

        if completion < 50:
            suggestions.append(f"Your syllabus completion in **{subject}** is low. Increase topic coverage.")

    if not suggestions:
        suggestions.append("You are doing well overall. Keep following your study plan consistently.")

    return suggestions

# ---------------------------
# App title
# ---------------------------
st.title("Smart Study Planner + Performance Analyzer")
st.write("Plan your study schedule, track progress, analyze performance, and get AI-based suggestions.")

# ---------------------------
# Sidebar inputs
# ---------------------------
st.sidebar.header("Student Setup")

student_name = st.sidebar.text_input("Student Name", "Student")
hours_per_day = st.sidebar.number_input("Available Study Hours per Day", min_value=1.0, max_value=24.0, value=5.0, step=0.5)
days_left = st.sidebar.number_input("Days Left for Exam", min_value=1, max_value=365, value=7, step=1)

st.sidebar.subheader("Add Subject")

subject_name = st.sidebar.text_input("Subject Name")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
preparation = st.sidebar.selectbox("Preparation Level", ["High", "Medium", "Low"])

if st.sidebar.button("Add Subject"):
    if subject_name.strip():
        st.session_state.subjects.append({
            "Subject": subject_name.strip(),
            "Difficulty": difficulty,
            "Preparation": preparation
        })
        st.sidebar.success(f"{subject_name} added.")
    else:
        st.sidebar.warning("Enter a valid subject name.")

if st.sidebar.button("Clear Subjects"):
    st.session_state.subjects = []
    st.sidebar.success("All subjects cleared.")

# ---------------------------
# Show subject list
# ---------------------------
st.subheader(f"Welcome, {student_name}")

if st.session_state.subjects:
    subjects_df = pd.DataFrame(st.session_state.subjects)
    st.write("### Added Subjects")
    st.dataframe(subjects_df, use_container_width=True)
else:
    st.info("No subjects added yet. Add subjects from the sidebar.")

# ---------------------------
# Generate study plan
# ---------------------------
st.write("## Study Plan")

plan_df = generate_plan(st.session_state.subjects, hours_per_day, days_left)

if not plan_df.empty:
    st.dataframe(plan_df, use_container_width=True)
else:
    st.warning("Add at least one subject to generate the study plan.")

# ---------------------------
# Progress tracker
# ---------------------------
st.write("## Progress Tracker")

if st.session_state.subjects:
    subject_options = [sub["Subject"] for sub in st.session_state.subjects]

    with st.form("progress_form"):
        progress_date = st.date_input("Date", value=date.today())
        progress_subject = st.selectbox("Subject", subject_options)
        planned_hours = st.number_input("Planned Hours", min_value=0.0, value=1.0, step=0.5)
        actual_hours = st.number_input("Actual Hours Studied", min_value=0.0, value=1.0, step=0.5)
        score = st.number_input("Test Score", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
        completion = st.number_input("Completion Percentage", min_value=0.0, max_value=100.0, value=50.0, step=1.0)

        submitted = st.form_submit_button("Add Progress")

        if submitted:
            new_row = pd.DataFrame([{
                "Date": progress_date,
                "Subject": progress_subject,
                "Planned Hours": planned_hours,
                "Actual Hours": actual_hours,
                "Score": score,
                "Completion %": completion
            }])

            st.session_state.progress_data = pd.concat(
                [st.session_state.progress_data, new_row],
                ignore_index=True
            )
            st.success("Progress added successfully.")

else:
    st.info("Add subjects first to start tracking progress.")

if not st.session_state.progress_data.empty:
    st.write("### Progress Data")
    st.dataframe(st.session_state.progress_data, use_container_width=True)

# ---------------------------
# Analytics dashboard
# ---------------------------
st.write("## Performance Dashboard")

if not st.session_state.progress_data.empty:
    progress_df = st.session_state.progress_data.copy()

    grouped = progress_df.groupby("Subject").agg({
        "Planned Hours": "sum",
        "Actual Hours": "sum",
        "Score": "mean",
        "Completion %": "mean"
    }).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Subject-wise Average Score")
        fig1, ax1 = plt.subplots()
        ax1.bar(grouped["Subject"], grouped["Score"])
        ax1.set_xlabel("Subject")
        ax1.set_ylabel("Average Score")
        ax1.set_title("Average Score by Subject")
        st.pyplot(fig1)

    with col2:
        st.write("### Planned vs Actual Study Hours")
        fig2, ax2 = plt.subplots()
        x = range(len(grouped))
        ax2.bar([i - 0.2 for i in x], grouped["Planned Hours"], width=0.4, label="Planned Hours")
        ax2.bar([i + 0.2 for i in x], grouped["Actual Hours"], width=0.4, label="Actual Hours")
        ax2.set_xticks(list(x))
        ax2.set_xticklabels(grouped["Subject"])
        ax2.set_xlabel("Subject")
        ax2.set_ylabel("Hours")
        ax2.set_title("Planned vs Actual Hours")
        ax2.legend()
        st.pyplot(fig2)

    st.write("### Completion Percentage")
    fig3, ax3 = plt.subplots()
    ax3.bar(grouped["Subject"], grouped["Completion %"])
    ax3.set_xlabel("Subject")
    ax3.set_ylabel("Completion %")
    ax3.set_title("Syllabus Completion by Subject")
    st.pyplot(fig3)

    overall_score = round(progress_df["Score"].mean(), 2)
    overall_completion = round(progress_df["Completion %"].mean(), 2)
    total_planned = round(progress_df["Planned Hours"].sum(), 2)
    total_actual = round(progress_df["Actual Hours"].sum(), 2)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Avg Score", overall_score)
    c2.metric("Overall Completion %", overall_completion)
    c3.metric("Total Planned Hours", total_planned)
    c4.metric("Total Actual Hours", total_actual)

else:
    st.info("No progress data available yet.")

# ---------------------------
# AI suggestions
# ---------------------------
st.write("## AI Suggestions")

suggestions = get_ai_suggestions(st.session_state.progress_data)
for s in suggestions:
    st.write(f"- {s}")

# ---------------------------
# Optional download
# ---------------------------
st.write("## Download Progress Data")

if not st.session_state.progress_data.empty:
    csv = st.session_state.progress_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="study_progress.csv",
        mime="text/csv"
    )

# ---------------------------
# Reset button
# ---------------------------
st.write("## Reset App Data")
if st.button("Reset All Data"):
    st.session_state.subjects = []
    st.session_state.progress_data = pd.DataFrame(
        columns=["Date", "Subject", "Planned Hours", "Actual Hours", "Score", "Completion %"]
    )
    st.success("All app data has been reset.")

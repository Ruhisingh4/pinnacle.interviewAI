# -----------------------------
# Pinnacle AI HR Mock Interviewer (Offline)
# -----------------------------
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

import streamlit as st
import PyPDF2
from nlp_utils import extract_skills

# -----------------------------
# Initialize session state
# -----------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

if "questions" not in st.session_state:
    st.session_state.questions = []

if "skills" not in st.session_state:
    st.session_state.skills = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []

# -----------------------------
# LOGIN
# -----------------------------
if st.session_state.user_name == "":
    st.title("🤖 Pinnacle – AI HR Mock Interviewer (Offline)")
    st.session_state.user_name = st.text_input("Enter your name to start:", "")
    if st.session_state.user_name != "":
        st.success(f"Hello {st.session_state.user_name}! Upload your resume to begin.")
else:
    st.title(f"Hello {st.session_state.user_name}, let's start your mock interview!")

    # -----------------------------
    # RESUME UPLOAD
    # -----------------------------
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file and not st.session_state.skills:
        # Extract text
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""

        # Extract skills
        skills = extract_skills(resume_text)
        st.session_state.skills = skills
        st.write("Detected Skills:", ", ".join(skills[:10]))

        # Predefined questions (offline)
        top_skills = skills[:5] if len(skills) >= 5 else skills
        st.session_state.questions = [
            f"Can you explain your experience with {top_skills[0]}?",
            f"How have you applied {top_skills[1]} in your projects?",
            f"Describe a challenge you faced using {top_skills[2]} and how you solved it.",
            f"What tools or frameworks have you used for {top_skills[3]}?",
            f"How do you stay updated on {top_skills[4]}?",
            "Tell me about a project where you demonstrated problem-solving skills.",
            "How do you handle tight deadlines and multiple tasks in a project?"
        ]

        # Predefined feedback for each question (you can customize)
        st.session_state.feedback = [
            "Great! Your experience sounds solid.",
            "Good application, it shows practical knowledge.",
            "Excellent problem-solving approach.",
            "Nice, familiarity with tools is important.",
            "Good to keep learning and staying updated.",
            "Well done, projects showcase skills.",
            "Good time management and prioritization skills."
        ]

    # -----------------------------
    # INTERVIEW FLOW
    # -----------------------------
    if st.session_state.skills and st.session_state.current_question_index < len(st.session_state.questions):
        current_q = st.session_state.questions[st.session_state.current_question_index]
        user_answer = st.text_area(current_q, key=st.session_state.current_question_index)

        if st.button("Submit Answer"):
            # Store user's answer
            st.session_state.answers.append(user_answer)

            # Provide offline feedback
            feedback_text = st.session_state.feedback[st.session_state.current_question_index]
            st.session_state.current_question_index += 1
            st.success(f"🤖 Interviewer Feedback: {feedback_text}")

    elif st.session_state.current_question_index >= len(st.session_state.questions):
        st.success("🎉 You have completed the mock interview!")
        st.write("### Your Answers:")
        for i, ans in enumerate(st.session_state.answers):
            st.write(f"Q{i+1}: {st.session_state.questions[i]}")
            st.write(f"Your Answer: {ans}")
            st.write(f"Feedback: {st.session_state.feedback[i]}")

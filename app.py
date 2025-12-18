import streamlit as st
import openai
import PyPDF2
from nlp_utils import extract_skills

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AIVEE 🤖 – AI HR Mock Interviewer",
    page_icon="🤖",
    layout="centered",
)

# ----------------------------
# API KEY
# ----------------------------
# Use st.secrets for securely managing the API key
try:
    client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    st.stop()


# ----------------------------
# SESSION STATE
# ----------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_college" not in st.session_state:
    st.session_state.user_college = ""
if "skills" not in st.session_state:
    st.session_state.skills = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "scores" not in st.session_state:
    st.session_state.scores = []
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0


# ----------------------------
# LOGIN
# ----------------------------
if not st.session_state.user_name:
    st.title("AIVEE 🤖 – AI HR Mock Interviewer")
    name = st.text_input("Enter your name to start:")
    college = st.text_input("Enter your college name:")
    if st.button("Start Interview"):
        if name and college:
            st.session_state.user_name = name
            st.session_state.user_college = college
            st.rerun()
        else:
            st.warning("Please enter both your name and college.")
else:
    # ----------------------------
    # MAIN APP
    # ----------------------------
    st.title(f"Hello {st.session_state.user_name}, let's begin!")

    # --- RESUME UPLOAD & SKILL EXTRACTION ---
    if not st.session_state.skills:
        uploaded_file = st.file_uploader("Upload Your Resume (PDF) to tailor the questions", type=["pdf"])
        if uploaded_file:
            with st.spinner("Analyzing your resume..."):
                try:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    resume_text = ""
                    for page in pdf_reader.pages:
                        resume_text += page.extract_text() or ""
                    
                    skills = extract_skills(resume_text)
                    st.session_state.skills = skills
                    st.write("Detected Skills:", ", ".join(skills[:10]))

                    # Generate questions based on skills
                    top_skills = skills[:5] if len(skills) >= 5 else skills
                    st.session_state.questions = [
                        f"Can you explain your experience with {top_skills[0]}?",
                        f"How have you applied {top_skills[1]} in your projects?",
                        f"Describe a challenge you faced using {top_skills[2]} and how you solved it.",
                        "Tell me about a project where you demonstrated problem-solving skills.",
                        "How do you handle tight deadlines and multiple tasks?"
                    ]
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing PDF: {e}")

    # --- INTERVIEW FLOW ---
    if st.session_state.skills and st.session_state.current_question_index < len(st.session_state.questions):
        current_q = st.session_state.questions[st.session_state.current_question_index]
        user_answer = st.text_area(f"Question {st.session_state.current_question_index + 1}/{len(st.session_state.questions)}: {current_q}", key=f"q_{st.session_state.current_question_index}")

        if st.button("Submit Answer"):
            if user_answer:
                st.session_state.answers.append(user_answer)

                # Generate dynamic feedback
                with st.spinner("AIVEE 🤖 is generating feedback..."):
                    try:
                        prompt = f\"\"\"Question: {current_q}
Answer: {user_answer}

Provide a score for this answer on a scale of 1 to 10, where 1 is poor and 10 is excellent. Then, provide constructive feedback on this answer for a job interview in 2-3 sentences. Address the user directly. Format your response as follows:

Score: [Your Score]/10

Feedback: [Your Feedback]\"\"\"
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are an expert HR interviewer providing feedback and scores. Your name is AIVEE."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        full_response = response.choices[0].message.content.strip()
                        
                        # Parse score and feedback
                        score_line = full_response.split('\\n')[0]
                        feedback_text = '\\n'.join(full_response.split('\\n')[2:])
                        score = score_line.replace("Score: ", "").strip()

                    except openai.RateLimitError:
                        feedback_text = "I'm experiencing high demand right now. Please check your OpenAI account for billing and usage details. You may need to wait a bit before trying again."
                        score = "N/A"
                    except Exception as e:
                        st.error(f"An error occurred while generating feedback: {e}")
                        feedback_text = "Sorry, I was unable to generate feedback for this answer."
                        score = "N/A"
                
                st.session_state.feedback.append(feedback_text)
                st.session_state.scores.append(score)
                st.session_state.current_question_index += 1
                st.rerun()
            else:
                st.warning("Please provide an answer before submitting.")

    # --- INTERVIEW COMPLETION ---
    elif st.session_state.skills:
        st.success("🎉 You have completed the mock interview!")
        st.balloons()
        st.write("### Final Report:")
        for i, ans in enumerate(st.session_state.answers):
            with st.expander(f"Q{i+1}: {st.session_state.questions[i]}"):
                st.write(f"**Your Answer:** {ans}")
                st.write(f"**AIVEE 🤖's Feedback:** {st.session_state.feedback[i]}")
                st.write(f"**Score:** {st.session_state.scores[i]}")

        if st.button("Start New Interview"):
            # Clear session state to restart
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
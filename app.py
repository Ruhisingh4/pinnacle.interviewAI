// ... existing code ...
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AIVEE 🤖 – AI HR Mock Interviewer",
    page_icon="🤖",
    layout="centered",
)

# -----------------------------
# LOGIN
# -----------------------------
if not st.session_state.user_name:
    st.title("AIVEE 🤖 – AI HR Mock Interviewer")
    name = st.text_input("Enter your name to start:")
    college = st.text_input("Enter your college name:")
else:
    st.title(f"Hello {st.session_state.user_name}, let's start your mock interview!")

    # -----------------------------
    # RESUME UPLOAD
    # -----------------------------
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file and not st.session_state.skills:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""

        # Extract skills
        skills = extract_skills(resume_text)
        st.session_state.skills = skills
        st.write("Detected Skills:", ", ".join(skills[:10]))

        # Predefined questions based on top skills
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

    # -----------------------------
    # INTERVIEW FLOW
    # -----------------------------
    if st.session_state.skills and st.session_state.current_question_index < len(st.session_state.questions):
        current_q = st.session_state.questions[st.session_state.current_question_index]
        user_answer = st.text_area(current_q, key=st.session_state.current_question_index)

        if st.button("Submit Answer"):
            if user_answer:
                st.session_state.answers.append(user_answer)

                # Generate dynamic feedback
                with st.spinner("AIVEE 🤖 is generating feedback..."):
                    prompt = f"Question: {current_q}\\nAnswer: {user_answer}\\n\\nProvide constructive feedback on this answer for a job interview in 2-3 sentences. Address the user directly."
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert HR interviewer providing feedback. Your name is AIVEE."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    feedback_text = response.choices[0].message.content.strip()
                
                st.session_state.feedback.append(feedback_text)
                st.session_state.current_question_index += 1
                st.rerun()
            else:
                st.warning("Please provide an answer before submitting.")

    # --- INTERVIEW COMPLETION ---
    else:
        st.success("🎉 You have completed the mock interview!")
        st.balloons()
        st.write("### Final Report:")
        for i, ans in enumerate(st.session_state.answers):
            with st.expander(f"Q{i+1}: {st.session_state.questions[i]}"):
                st.write(f"**Your Answer:** {ans}")
                st.write(f"**AIVEE 🤖's Feedback:** {st.session_state.feedback[i]}")

        if st.button("Start New Interview"):
            # Clear session state to restart
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
// ... existing code ...
# -----------------------------
# LOGIN
# -----------------------------
if st.session_state.user_name == "":
    st.title("AIVEE 🤖 – AI HR Mock Interviewer")
    st.session_state.user_name = st.text_input("Enter your name to start:", "")
    st.session_state.user_college = st.text_input("Enter your college name:", "")
// ... existing code ...
            st.session_state.feedback.append(feedback_text)
            st.session_state.current_question_index += 1
            st.success(f"AIVEE 🤖: {feedback_text}")

    elif st.session_state.current_question_index >= len(st.session_state.questions):
        st.success("🎉 You have completed the mock interview!")
// ... existing code ...

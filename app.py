// ... existing code ...
        if st.button("Submit Answer"):
            if user_answer:
                st.session_state.answers.append(user_answer)

                # Generate dynamic feedback
                with st.spinner("AIVEE 🤖 is generating feedback..."):
                    try:
                        prompt = f"Question: {current_q}\\nAnswer: {user_answer}\\n\\nProvide constructive feedback on this answer for a job interview in 2-3 sentences. Address the user directly."
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are an expert HR interviewer providing feedback. Your name is AIVEE."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        feedback_text = response.choices[0].message.content.strip()
                    except openai.RateLimitError:
                        feedback_text = "I'm experiencing high demand right now. Please check your OpenAI account for billing and usage details. You may need to wait a bit before trying again."
                    except Exception as e:
                        st.error(f"An error occurred while generating feedback: {e}")
                        feedback_text = "Sorry, I was unable to generate feedback for this answer."
                
                st.session_state.feedback.append(feedback_text)
// ... existing code ...

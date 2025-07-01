import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# App title
st.set_page_config(page_title="Regex Generator & Explainer", layout="centered")
st.title("🔍 Regex Generator & Explainer")
st.caption("Describe the pattern and get a regex with explanation")

# Initialize memory
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_area("📝 Describe the pattern you want to match", height=100)

if st.button("Generate Regex"):
    if user_input.strip() == "":
        st.warning("Please enter a valid description.")
    else:
        with st.spinner("Thinking with Gemini..."):

            prompt = f"""
You are a Regex Tutor.

The user described a text pattern as: "{user_input}"

1. Generate the correct regex pattern.
2. Explain the pattern in simple terms, breaking down each component.
3. Do not return any code or markdown formatting.

Reply in this format:
REGEX: <pattern>
EXPLANATION: <explanation>
            """

            try:
                response = model.generate_content(prompt)
                output = response.text.strip()

                # Parse response
                if "REGEX:" in output:
                    regex = output.split("REGEX:")[1].split("EXPLANATION:")[0].strip()
                    explanation = output.split("EXPLANATION:")[1].strip()
                else:
                    regex = "Could not parse response"
                    explanation = output

                # Save in memory
                st.session_state.history.append({
                    "description": user_input,
                    "regex": regex,
                    "explanation": explanation
                })

                # Show result
                st.subheader("Generated Regex")
                st.code(regex, language="regex")

                st.subheader("Explanation")
                st.write(explanation)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

# Show memory
if st.session_state.history:
    with st.expander("View Past Patterns"):
        for idx, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"**{idx}.** _{item['description']}_")
            st.code(item['regex'], language="regex")
            st.write(item['explanation'])

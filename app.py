import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize model
def get_llm():
    return genai.Client(api_key=API_KEY)

# Function to summarize notes
def summarize_notes(notes):
    llm = get_llm()

    prompt = f"""
    Summarize these study notes in exactly this format:

    SHORT SUMMARY:
    (4–5 lines)

    KEY POINTS:
    - Point 1
    - Point 2
    - Point 3
    - Point 4

    EXAM READY BULLETS:
    • Bullet 1
    • Bullet 2
    • Bullet 3
    • Bullet 4

    Notes to summarize:
    {notes}
    """

    response = llm.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text


# ---------------- UI ---------------- #

st.set_page_config(page_title="AI Notes Summarizer", page_icon="📚")

st.title("📚 AI Notes Summarizer")
st.write("Convert your long notes into **short summaries, key points & exam bullets** ✨")

# Input area
notes = st.text_area(
    "✍️ Paste your study notes here:",
    height=250,
    placeholder="Enter your notes..."
)

# Button
if st.button("🚀 Summarize"):
    if not API_KEY:
        st.error("❌ API Key not found. Please check your .env file.")
    elif not notes.strip():
        st.warning("⚠️ Please enter some notes first.")
    else:
        with st.spinner("Generating summary... ⏳"):
            try:
                result = summarize_notes(notes)
                st.success("✅ Summary Generated!")

                # Output
                st.subheader("📄 Result")
                st.markdown(result)

            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit + Gemini AI")
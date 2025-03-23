import streamlit as st
import pdfplumber
from docx import Document
from transformers import pipeline
import google.generativeai as genai
import requests
import speech_recognition as sr
import pyttsx3
import openai

# Initialize Gemini AI
API_KEY = 'Paste your API Key to work fucntionally'
if not API_KEY:
    st.error("❌ API Key for Gemini AI is missing. Set the environment variable `GEMINI_API_KEY`.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize TTS engine
tts_engine = pyttsx3.init()


def generate_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text if response else "⚠️ No response generated."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# --- Resume Analysis ---
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text if text.strip() else "⚠️ No text found in this PDF."





def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])


def analyze_resume(content):
    prompt = f"""
    Analyze the following resume text and provide:
    - An ATS score (out of 100)
    - Strengths and weaknesses
    - Improvement suggestions
    - Personalized learning recommendations (courses, certifications, etc.)
    - Relevant job matches based on current market trends
    - Suggested cover letter improvements and LinkedIn profile tips
    - AI-powered professional networking and mentorship suggestions, including:
      - Recommended mentors and professional networks based on industry trends
      - Alumni, industry leaders, and career coach connections
      - Networking strategies and event suggestions to enhance career growth

    Resume Content:
    {content}
    """
    response = generate_response(prompt)
    return response


# --- Streamlit UI ---
st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;
        }
        .main-title {
            text-align: center;
            color: #4CAF50;
            font-size: 3rem;
            font-weight: bold;
        }
        .sub-header {
            color: #555;
            text-align: center;
            font-size: 1.2rem;
        }
        .section-title {
            color: #FF9800;
            font-size: 1.5rem;
            margin-top: 20px;
        }
        .stTextInput input, .stTextArea textarea {
            border-radius: 10px;
            border: 2px solid #4CAF50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: #fff;
            font-weight: bold;
            border-radius: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Title
st.markdown("<h1 class='main-title'>💼 Career Compass: Your Guide</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Upload your resume and let AI guide you to the perfect job roles!</p>",
            unsafe_allow_html=True)

# Chatbot Section
st.markdown("### 🚀 Career Companion - Ask Anything About Your Future!")
user_input = st.text_input("Type your message here:")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        response = generate_response(user_input)
        st.write(response)

# Resume Analyzer
st.markdown("<h3 class='section-title'>🛂 Upload Your Resume</h3>", unsafe_allow_html=True)
resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
if resume_file:
    if resume_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_file)
    elif resume_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(resume_file)

    st.markdown("<h3 style='color: #009688;'>📋 Extracted Resume Text</h3>", unsafe_allow_html=True)
    st.text_area("", resume_text, height=150)

    if st.button("🔍 Analyze Resume"):
        with st.spinner("🔎 Analyzing your resume..."):
            analysis = analyze_resume(resume_text)
        st.markdown(
            "<h3 style='color: #FF5722;'>📊 AI Resume Analysis, ATS Score, Improvement Suggestions & Job Recommendations</h3>",
            unsafe_allow_html=True)
        st.write(analysis)

# Sidebar
st.sidebar.markdown("<h2 style='color: #3F51B5;'>🔎 Navigation</h2>", unsafe_allow_html=True)
st.sidebar.markdown("- AI Resume Analyzer")
st.sidebar.markdown("- AI Chatbot")

st.sidebar.markdown("<h3 style='color: #795548;'>ℹ️ About</h3>", unsafe_allow_html=True)
st.sidebar.info("AI-powered career guidance system designed to help users achieve their career goals.")

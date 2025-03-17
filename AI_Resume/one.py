import streamlit as st
import google.generativeai as genai
import chromadb
from fpdf import FPDF
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Configure Google Gemini API
genai.configure(api_key="AIzaSyD0H_WeVN3k4Hxae1RNDp_hFBEiG4zbrTc")

# Initialize ChromaDB for storing generated resumes
chroma_client = chromadb.PersistentClient(path="resume_db")
collection = chroma_client.get_or_create_collection(name="resumes")

# Streamlit UI Configuration
st.set_page_config(page_title="AI Resume Generator", page_icon="📄", layout="centered")
st.title("📄 AI Resume & Cover Letter Generator 🚀")

# User Inputs
name = st.text_input("Enter Your Name:")
email = st.text_input("Enter Your Email:")
phone = st.text_input("Enter Your Phone Number:")
skills = st.text_area("List Your Skills (comma-separated):")
experience = st.text_area("Describe Your Work Experience:")
job_role = st.text_input("Job Role You Are Applying For:")

# Function to generate AI resume
def generate_resume(name, email, phone, skills, experience, job_role):
    prompt = f"""
    Generate a professional, ATS-friendly resume for {name} who is applying for {job_role}.
    Contact: {email}, {phone}
    Skills: {skills}
    Experience: {experience}
    Ensure it's formatted properly with sections for Summary, Skills, Experience, and Education.
    """
    return genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt).text

# Function to generate AI cover letter
def generate_cover_letter(name, job_role, skills, experience):
    prompt = f"""
    Write a compelling cover letter for {name} applying for {job_role}.
    Mention the key skills: {skills} and highlight relevant experience: {experience}.
    The letter should be professional, engaging, and customized for the role.
    """
    return genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt).text

# Function to export resume/cover letter as PDF (Fixed Unicode Error)
def export_pdf(name, text, file_type):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Fix Unicode Error by replacing unsupported characters
    text = text.encode("latin-1", "replace").decode("latin-1")

    for line in text.split("\n"):
        pdf.cell(200, 10, line, ln=True, align='L')

    pdf_file = f"{name}_{file_type}.pdf"
    pdf.output(pdf_file, "F")  # Save the file correctly
    return pdf_file

# Function to save cover letter as CSV
def export_csv(name, cover_letter):
    csv_file = f"{name}_Cover_Letter.csv"
    df = pd.DataFrame({"Cover Letter": [cover_letter]})
    df.to_csv(csv_file, index=False)
    return csv_file

# Function to save cover letter as PNG
def export_png(name, cover_letter):
    wrapped_text = textwrap.fill(cover_letter, width=60)
    
    img = Image.new('RGB', (800, 500), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 50), wrapped_text, fill=(0, 0, 0), font=font)
    
    png_file = f"{name}_Cover_Letter.png"
    img.save(png_file)
    return png_file

# Generate Resume & Download Option
if st.button("Generate Resume"):
    resume = generate_resume(name, email, phone, skills, experience, job_role)
    st.subheader("📄 Generated Resume:")
    st.text_area("", resume, height=400)

    pdf_file = export_pdf(name, resume, "Resume")
    st.download_button(label="📥 Download Resume", data=open(pdf_file, "rb"), file_name=pdf_file, mime="application/pdf")

# Generate Cover Letter & Download Options
if st.button("Generate Cover Letter"):
    cover_letter = generate_cover_letter(name, job_role, skills, experience)
    st.subheader("📩 Generated Cover Letter:")
    st.text_area("", cover_letter, height=300)

    # Export files
    pdf_file = export_pdf(name, cover_letter, "Cover_Letter")
    csv_file = export_csv(name, cover_letter)
    png_file = export_png(name, cover_letter)

    # Download buttons
    st.download_button(label="📥 Download Cover Letter (PDF)", data=open(pdf_file, "rb"), file_name=pdf_file, mime="application/pdf")
    st.download_button(label="📥 Download Cover Letter (CSV)", data=open(csv_file, "rb"), file_name=csv_file, mime="text/csv")
    st.download_button(label="📥 Download Cover Letter (PNG)", data=open(png_file, "rb"), file_name=png_file, mime="image/png")

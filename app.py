from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os
from PIL import Image
import pdf2image
import io
import google.generativeai as genai
import base64

genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))


# this will be the funtion handling the pdf to image content 
#input is the job description and pdf_content is the content extrating from the pdf and promt will tell me model what to do 
def get_response(input_text,pdf_content,promt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text,pdf_content[0],promt])
    return response.text

# this will be the processing that we are doing after converting it into the image 
def input_pdf_data(upload_file):
    if upload_file is not None:
        images = pdf2image.convert_from_bytes(upload_file.read())
        first_page = images[0]

        # now here we convert it into bytes
        image_bytes_arr = io.BytesIO()
        first_page.save(image_bytes_arr, format='JPEG')
        image_bytes_arr = image_bytes_arr.getvalue()

        #here the parts and encoding with base 64 library will be done 
        pdf_parts = [
            {
                "mime_type": "image/jpeg", 
                'data': base64.b64encode(image_bytes_arr).decode() # this will be encoding this 
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError('no uploaded file')
    
# HERE THE MAIN STREAMLIT APP CODE WILL BE SEEN
st.set_page_config(page_title='Resume Expert')
st.header('Resume Tracking System')
input_text = st.text_area('Job Description', key='input')
upload_file = st.file_uploader('Upload Your Resume In Pdf Form....')


if upload_file is not None:
    st.write('pdf file is being uploaded successfully')

submit1 = st.button('Resume Evaluation & Job Fit Score')
submit2 = st.button('Career Progression & Future Plan')
submit3 = st.button('HR & Hiring Manager Insights')

# Prompt 1: Resume Evaluation & Job Fit Score
input_prompt1 = """
You are an advanced ATS (Applicant Tracking System) with deep expertise in technical hiring. 
Your task is to evaluate the provided resume against the given job description for a {Job Role}. 
Analyze the match based on technical skills, relevant experience, certifications, and soft skills. 
Provide a job fit percentage score, highlighting key strengths and areas for improvement. 

The output should be structured as follows:
1. Match Score: {XX}%
2. Top Matching Skills: {List of relevant skills}
3. Missing/Weak Skills: {List of gaps}
4. Overall Verdict: {Brief summary of how well the candidate fits}
"""

# Prompt 2: Career Progression & Future Plan
input_prompt2 = """
Based on the evaluation, create a detailed career roadmap for the candidate to improve their suitability for this role.
Provide suggestions for:
- Essential Skill Development: (Programming, frameworks, tools, etc.)
- Recommended Certifications or Courses: (Industry-standard certifications)
- Project Recommendations: (Real-world projects to build expertise)
- Soft Skills & Leadership Development: (Teamwork, problem-solving, communication)
- Expected Timeline for Improvement: (Short-term & long-term plan)
"""

# Prompt 3: HR & Hiring Manager Insights
input_prompt3 = """
As an experienced HR professional with expertise in technical hiring, evaluate the resume for {Job Role} from a recruitment perspective. 
Provide insights on:
- How the candidate will perform in an interview
- Whether they meet industry benchmarks for this role
- Potential red flags or concerns
- Final hiring recommendation (Strong match, Partial match, Needs improvement)
"""

if submit1 :
    if upload_file is not None:
        pdf_content = input_pdf_data (upload_file)
        response = get_response(input_text, pdf_content, input_prompt1)
        st.subheader('THE RESPONSE IS')
        st.write(response)
    else:
        st.write('upload your resume')
elif submit2:
    if upload_file is not None:
        pdf_content = input_pdf_data (upload_file)
        response = get_response(input_text, pdf_content, input_prompt2)
        st.subheader('THE RESPONSE IS')
        st.write(response)
    else:
        st.write('upload your resume')
elif submit3:
    if upload_file is not None:
        pdf_content = input_pdf_data (upload_file)
        response = get_response(input_text, pdf_content, input_prompt3)
        st.subheader('THE RESPONSE IS')
        st.write(response)
    else:
        st.write('upload your resume')




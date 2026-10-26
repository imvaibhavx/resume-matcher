import streamlit as st

st.title("Resume-to-Job Matcher")
st.write("Paste your resume and a job description to see how well they match.")

resume_text = st.text_area("Your resume", height=250)
job_text = st.text_area("Job description", height=250)

if st.button("Match"):
    st.write("Resume characters:", len(resume_text))
    st.write("Job description characters:", len(job_text))
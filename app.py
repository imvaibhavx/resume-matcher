import streamlit as st
from semantic import analyze

st.title("Resume-to-Job Matcher")
st.write("Paste your resume and a job description to see how well they match.")
st.caption("Tip: leave out your phone number, email and address. The matcher doesn't need them.")

resume_text = st.text_area("Your resume", height=250)
job_text = st.text_area("Job description", height=250)

if st.button("Match"):
    if len(resume_text.split()) < 10 or len(job_text.split()) < 10:
        st.warning("Please paste a bit more text into both boxes.")
    else:
        with st.spinner("Matching..."):
            results = analyze(resume_text, job_text)
        for status, score, text, evidence in results:
            st.write(f"**[{status}] {score:.2f}** | {text}")
            if evidence:
                st.caption(f"Evidence: {evidence}")
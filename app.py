import streamlit as st
from semantic import analyze
from skills import load_skills, find_skills

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

        if not results:
            st.warning("No requirements found in the job description. Try pasting only the responsibilities and requirements.")
        else:
            covered = [r for r in results if r[0] == "COVERED"]
            partial = [r for r in results if r[0] == "PARTIAL"]
            gaps = [r for r in results if r[0] == "GAP"]

            col1, col2, col3 = st.columns(3)
            col1.metric("Covered", len(covered))
            col2.metric("Partial", len(partial))
            col3.metric("Gaps", len(gaps))

            st.subheader("Biggest gaps")
            for status, score, text, evidence in sorted(gaps, key=lambda r: r[1])[:5]:
                st.write(f"**{score:.2f}** | {text}")

            skills = load_skills()
            gap_text = " ".join(r[2] for r in gaps)
            gap_skills = sorted(find_skills(gap_text, skills))
            if gap_skills:
                st.subheader("Skills to learn or mention")
                st.write(", ".join(gap_skills))
                st.caption("If you already have one of these, add it to your resume with a concrete example. If not, a small project is the fastest way to learn it.")

            with st.expander(f"Partial matches ({len(partial)})"):
                for status, score, text, evidence in partial:
                    st.write(f"**{score:.2f}** | {text}")
                    st.caption(f"Evidence: {evidence}")

            with st.expander(f"Covered ({len(covered)})"):
                for status, score, text, evidence in covered:
                    st.write(f"**{score:.2f}** | {text}")
                    st.caption(f"Evidence: {evidence}")
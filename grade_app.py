import pandas as pd
import streamlit as st

def score_to_grade(score):
    try:
        score = float(score)
        if not 0 <= score <= 100:
            return "—", None
        if score >= 90:
            return "A+", 4.3
        elif score >= 85:
            return "A", 4.0
        elif score >= 80:
            return "A-", 3.7
        elif score >= 77:
            return "B+", 3.3
        elif score >= 73:
            return "B", 3.0
        elif score >= 70:
            return "B-", 2.7
        elif score >= 67:
            return "C+", 2.3
        elif score >= 63:
            return "C", 2.0
        elif score >= 60:
            return "C-", 1.7
        elif score >= 50:
            return "D", 1.0
        elif score >= 40:
            return "E", 0.8
        else:
            return "F", 0.0
    except Exception:
        pass
    return "-", None

st.title("NSYSU Grade Converter")

tab1, tab2 = st.tabs(["Query", "Upload File for Batch conversion"])

with tab1:
    with st.form("score_form"):
        value = st.number_input("Enter score:", min_value=0.0, 
            max_value=100.0, value=85.0, step=0.1)
        submitted = st.form_submit_button("Convert")
    if submitted:
        letter, gpa = score_to_grade(value)
        st.success(f"**Grade:** {letter} | **GPA points:** {gpa}")

with tab2:
    upl = st.file_uploader("Upload a CSV with students' scores", type="csv")
    use_example = st.checkbox("Use Example File")
    df = None
    if upl is not None and not use_example:
        try:
            df = pd.read_csv(upl)
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
    if use_example:
        df = pd.read_csv("data/grades.csv")
    if df is not None:
        # let user choose which column holds the scores
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if not num_cols:
            st.error("No numeric columns detected in the file.")
            st.stop()
        col = st.selectbox("Select the score column:", num_cols)
        out = df.copy()
        out["Grade"], out["GPA_points"] = zip(*out[col].apply(score_to_grade))
        st.subheader("Coverted grades")
        st.dataframe(out)
        # download button
        out_csv = out.to_csv(index=False)
        st.download_button("Download graded CSV", data=out_csv, 
                           icon=":material/download:",
                           file_name="coverted_grades.csv")
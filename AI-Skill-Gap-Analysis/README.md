# AI Skill Gap Analysis

A beginner-friendly Streamlit project for comparing resume skills with the skills listed for a target job role and generating a suggested learning roadmap.

## Requirements
- Python 3.11.9 recommended
- pip

## Windows setup

Open a terminal in this folder and run:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit, usually http://localhost:8501.

## Test input
Name: Student
Target role: Data Scientist
Resume text: `I know Python, SQL, Pandas and Excel.`

## Notes
This beginner version uses local CSV data and dictionary/regular-expression skill extraction. It does not need an API key. The skill-match percentage reflects the fraction of listed job skills found in the entered text; it is not a validated hiring score.

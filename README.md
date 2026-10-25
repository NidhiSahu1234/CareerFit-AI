# CareerFit AI

CareerFit AI is a Streamlit workspace for reviewing resumes, comparing them with a job posting, and preparing a tailored resume. Its job-match estimate is explainable and heuristic; it is not an official ATS score.

**Repository:** [NidhiSahu1234/CareerFit-AI](https://github.com/NidhiSahu1234/CareerFit-AI)

**Live application:** [deployed](https://careerfit-ai-x6qebypew6pa397t9rzgrn.streamlit.app/?utm_source=chatgpt.com) 

## Features

- Resume analysis for a selected role, with structure, formatting, skill, and recommendation feedback.
- Optional Google Gemini analysis. It requires a configured API key and explicit consent before resume text is sent to Google.
- Resume builder with Modern, Professional, Minimal, and Creative templates.
- Explainable resume-to-job comparison with required and preferred skills, evidence excerpts, date-based experience estimates, and actionable gaps.
- Bullet feedback that preserves the candidate's facts. Automatic rewrites only rephrase eligible opening phrases.
- Up to 20 session-only job-match snapshots with score and skill-gap comparison. History stores comparison metadata, never resume or job-description text.
- Role-based learning resources, a dashboard, job search, and feedback pages.
- PDF and DOCX input for job matching (maximum 5 MB) and downloadable Markdown reports.

## Technology

- Python and Streamlit
- SQLite for optional resume-builder/dashboard data
- pandas and Plotly for analysis views
- pypdf/pdfplumber and python-docx for document handling
- Google Gemini through the maintained `google-genai` SDK for the optional AI analyzer
- Selenium and Chromium for job-search features that need browser automation

## Configuration and data handling

- AI analysis sends the extracted resume text and any job description to Google Gemini after the user checks the consent box. Review Google's terms and data practices before enabling it.
- The two legacy analyzer and builder pages offer an unchecked-by-default option to save resume details in the app's local SQLite database. The database is not encrypted and this app does not provide separate end-user accounts.
- Job-match history lasts for the current Streamlit session only. The downloadable history includes role labels, scores, and skill gaps, not resume text.
- This clean repository snapshot excludes local SQLite databases and spreadsheet exports and starts without inherited Git history. Keep real resume data, generated exports, and secrets out of source control. `.gitignore` helps prevent local data files from being added but cannot remove files already tracked or erase old versions.


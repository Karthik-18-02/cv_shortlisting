from flask import Flask, render_template, request
import os
import pandas as pd
import json

app = Flask(__name__)

# Load pre-saved outputs from your notebook
DATA_FOLDER = os.path.join(app.root_path, "data")

# Load job descriptions (if needed) – for example, to list available jobs
job_description_csv = os.path.join(DATA_FOLDER, "job_description.csv")
job_df = pd.read_csv(job_description_csv, encoding='ISO-8859-1')

# Load match scores DataFrame
match_scores_csv = os.path.join(DATA_FOLDER, "match_scores.csv")
if os.path.exists(match_scores_csv):
    match_scores_df = pd.read_csv(match_scores_csv, index_col=0)
else:
    match_scores_df = None

# Load shortlisted candidates JSON
shortlisted_json = os.path.join(DATA_FOLDER, "shortlisted_candidates.json")
if os.path.exists(shortlisted_json):
    with open(shortlisted_json, "r") as f:
        shortlisted_candidates = json.load(f)
else:
    shortlisted_candidates = {}

# Load email data DataFrame
email_data_csv = os.path.join(DATA_FOLDER, "email_data.csv")
if os.path.exists(email_data_csv):
    email_df = pd.read_csv(email_data_csv)
else:
    email_df = pd.DataFrame()

# Home page: List job descriptions (use your job_df or final job summaries)
@app.route("/")
def index():
    # For simplicity, display job titles and summaries from job_df (assuming your notebook produced them)
    # Modify this as needed if your notebook output is different.
    jobs = job_df[['Job Title', 'Job Description']].to_dict(orient="records")
    return render_template("index.html", jobs=jobs)

# Route to display match scores as an HTML table
@app.route("/match_scores")
def show_match_scores():
    if match_scores_df is not None:
        scores_html = match_scores_df.to_html(classes="table table-striped")
        return render_template("results.html", scores_html=scores_html)
    else:
        return "Match scores not available. Please run your notebook to generate them."

# Route to display shortlisted candidates for each job title
# @app.route("/shortlisted")
# def show_shortlisted():
#     if shortlisted_candidates:
#         return render_template("shortlisted.html", shortlisted=shortlisted_candidates)
#     else:
#         return "Shortlisted candidate data not available. Please run your notebook to generate it."
    
# Route to display shortlisted candidates for each job title
@app.route("/shortlisted", methods=["GET", "POST"])
def show_shortlisted():
    search_query = request.args.get('search', '').lower()

    if shortlisted_candidates:
        shortlisted_filtered = {}
        
        # Filter candidates by the search query for each job
        for job_title, candidates in shortlisted_candidates.items():
            filtered_candidates = [candidate for candidate in candidates if search_query in candidate.lower()]
            
            # Add job title to dictionary only if there are matching candidates
            if filtered_candidates:
                shortlisted_filtered[job_title] = filtered_candidates
            else:
                shortlisted_filtered[job_title] = []

        return render_template("shortlisted.html", shortlisted=shortlisted_filtered, search_query=search_query)
    else:
        return "Shortlisted candidate data not available. Please run your notebook to generate it."


# Route to display extracted emails (optional)
@app.route("/emails")
def show_emails():
    if not email_df.empty:
        emails_html = email_df.to_html(classes="table table-striped", index=False)
        return render_template("results.html", scores_html=emails_html)
    else:
        return "Email data not available. Please run your notebook to generate it."

if __name__ == "__main__":
    app.run(debug=True)

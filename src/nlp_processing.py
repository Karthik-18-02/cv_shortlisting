import data_preprocessing as dp

# Define the BERT summarization function
from transformers import pipeline

# Load the BERT summarizer pipeline
summarizer = pipeline("summarization")

def summarize_with_bert(job_description):
    summary = summarizer(job_description, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Apply BERT summarization to the cleaned job descriptions
summarized_descriptions = dp.job_description_df['Cleaned Job Description'].apply(summarize_with_bert)

# Add the summaries to the dataframe
dp.job_description_df['Summary'] = summarized_descriptions

# Display the job titles along with their summaries
dp.job_description_df[['Job Title', 'Summary']].head()

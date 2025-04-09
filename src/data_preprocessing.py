import pandas as pd

job_description_df = pd.read_csv("job_description.csv", encoding='ISO-8859-1')

# Display the first few rows of the file to understand its structure
job_description_df = job_description_df.iloc[:, :2]
job_description_df.head()

# Clean the 'Job Description' column by removing unwanted text (like 'Description:')
job_description_df['Cleaned Job Description'] = job_description_df['Job Description'].str.replace(r'^( Description:|Description:|Job Description:)\s*', '', regex=True)

# Display the first few rows of the cleaned job descriptions
job_description_df[['Job Title', 'Cleaned Job Description']].head()

job_description_df['Cleaned Job Description'] = job_description_df['Cleaned Job Description'].str.lower()

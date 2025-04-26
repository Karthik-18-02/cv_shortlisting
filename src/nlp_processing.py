from transformers import pipeline

def summarize_with_bert(job_description):
    summarizer = pipeline("summarization")
    summary = summarizer(job_description, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

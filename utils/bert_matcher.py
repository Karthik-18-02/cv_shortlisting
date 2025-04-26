from transformers import BertTokenizer, BertModel, pipeline
import torch
from sklearn.metrics.pairwise import cosine_similarity

class BERTMatcher:
    def __init__(self, model_name):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.summarizer = pipeline("summarization")

    def get_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state[:, 0, :].numpy()

    def calculate_match_score(self, job_desc, candidate_info):
        job_embedding = self.get_embeddings(job_desc)
        candidate_text = " ".join(candidate_info['skills'] + candidate_info['qualifications'])
        candidate_embedding = self.get_embeddings(candidate_text)
        return cosine_similarity(job_embedding, candidate_embedding)[0][0]
def shortlist_candidates(match_scores, threshold):
    shortlisted = {}
    for job_title, score in match_scores:
        if score >= threshold:
            if job_title not in shortlisted:
                shortlisted[job_title] = []
            shortlisted[job_title].append((job_title, score))
    return shortlisted

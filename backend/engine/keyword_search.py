import string
import os
import pandas as pd
from rank_bm25 import BM25Okapi
from google.cloud import bigquery

_bm25 = None
_df = None

def _tokenize(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

# call this first
def build_index():
    global _df, _bm25
    
    project_id = os.getenv("PROJECT_ID")
    client = bigquery.Client(project=project_id)
    
    query = f"""
        SELECT chunk_id, repo_name, chunk_text 
        FROM `{project_id}.searchme_dataset.embeddings_spark_50k_clean`
    """
    
    print("Connecting to BigQuery and building in-memory index...")
    _df = client.query(query).to_dataframe()
    
    _df['chunk_text'] = _df['chunk_text'].fillna("")
    
    tokenized_corpus = [_tokenize(doc) for doc in _df['chunk_text']]
    _bm25 = BM25Okapi(tokenized_corpus)
    print("Index successfully built!")

def keyword_search(query, k=5):
    global _df, _bm25
    
    if _bm25 is None or _df is None:
        build_index()
    
    tokenized_query = _tokenize(query)
    
    doc_scores = _bm25.get_scores(tokenized_query)
    
    results_df = _df.copy()
    results_df['bm25_score'] = doc_scores
    top_k_results = results_df.nlargest(k, 'bm25_score').copy()
    
    top_k_results['rank'] = range(1, len(top_k_results) + 1)
    
    final_results = top_k_results[['rank', 'bm25_score', 'chunk_id', 'repo_name', 'chunk_text']]
    return final_results.to_dict(orient='records')
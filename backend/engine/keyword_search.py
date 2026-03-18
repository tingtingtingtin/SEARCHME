import string
import pandas as pd
from rank_bm25 import BM25Okapi
from google.cloud import bigquery

_bm25 = None
_df = None

def _tokenize(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

def build_index():
    global _df, _bm25

    client = bigquery.Client()

    query = """
        SELECT chunk_id, repo_name, chunk_text
        FROM `search-me-cs226.searchme_dataset.embeddings_spark_50k_clean`
    """

    _df = client.query(query).to_dataframe()

    _df['chunk_text'] = _df['chunk_text'].fillna("")

    tokenized_corpus = [_tokenize(doc) for doc in _df['chunk_text']]
    _bm25 = BM25Okapi(tokenized_corpus)

    _df.drop(columns=['chunk_text'], inplace=True, errors='ignore') # no longer needed after indexing

def keyword_search(query, k=5):
    global _df, _bm25

    if _bm25 is None or _df is None:
        build_index()

    tokenized_query = _tokenize(query)
    doc_scores = _bm25.get_scores(tokenized_query)

    top_indices = doc_scores.argsort()[::-1][:k]
    return _df.iloc[top_indices]["repo_name"].tolist()
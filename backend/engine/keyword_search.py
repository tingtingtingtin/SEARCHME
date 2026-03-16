import string
import pandas as pd
from rank_bm25 import BM25Okapi

class KeywordSearchEngine:
    def __init__(self):
        self.bm25 = None
        self.df = None

    def _tokenize(self, text):
        text = str(text).lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text.split()
    
    # in the app, get your production data dataframe and run it with build_index first
    def build_index(self, corpus_df):
        self.df = corpus_df.copy()
        self.df['chunk_text'] = self.df['chunk_text'].fillna("")
        tokenized_corpus = [self._tokenize(doc) for doc in self.df['chunk_text']]
        self.bm25 = BM25Okapi(tokenized_corpus)
 
    # needs build_index first
    def search(self, query, k=5):
        if self.bm25 is None:
            raise RuntimeError("BM25 index has not been built; make sure you call build_index() first.")
        tokenized_query = self._tokenize(query)
        
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        results_df = self.df.copy()
        results_df['bm25_score'] = doc_scores
        top_k_results = results_df.nlargest(k, 'bm25_score').copy()
        
        top_k_results['rank'] = range(1, len(top_k_results) + 1)
        
        final_results = top_k_results[['rank', 'bm25_score', 'chunk_id', 'repo_name', 'chunk_text']]
        return final_results.to_dict(orient='records')
import pandas as pd
import string
from rank_bm25 import BM25Okapi


try:
    df = pd.read_csv("data/local_repo_data.csv")
except FileNotFoundError:
    print(f"Error: {"local_repo_data.csv"} not found. Run extract_data.py first, or run keyword_search.py from the root.")
    exit()

df['chunk_text'] = df['chunk_text'].fillna("")
def tokenize(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

# tokenize the texts and initialize a bm25 model with it
tokenized_corpus = [tokenize(doc) for doc in df['chunk_text']]
bm25 = BM25Okapi(tokenized_corpus)

def keyword_search(query, k=5):
    tokenized_query = tokenize(query)
    doc_scores = bm25.get_scores(tokenized_query)
    
    results_df = df.copy()
    results_df['bm25_score'] = doc_scores
    
    top_k_results = results_df.nlargest(k, 'bm25_score')
    
    return top_k_results[['chunk_id', 'repo_name', 'bm25_score', 'chunk_text']]

# testing on a sample query
if __name__ == "__main__":
    test_query = "machine learning models"
    print(f"\nSearching for: '{test_query}'")
    
    results = keyword_search(test_query, k=3) # adjust k for more results
    
    for index, row in results.iterrows():
        print(f"\nRepo: {row['repo_name']}")
        print(f"Chunk ID: {row['chunk_id']}")
        print(f"Score: {row['bm25_score']:.4f}")
        print(f"Snippet: {row['chunk_text'][:150]}...")
import string

import pandas as pd
from rank_bm25 import BM25Okapi


try:
    df = pd.read_csv("data/local_repo_data.csv")
except FileNotFoundError:
    print(
        "Error: data/local_repo_data.csv not found. "
        "Run extract_data.py first from the project root."
    )
    exit()

df["chunk_text"] = df["chunk_text"].fillna("")


def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.split()

# build BM25 index once from the local dataset
tokenized_corpus = [tokenize(doc) for doc in df["chunk_text"]]
bm25 = BM25Okapi(tokenized_corpus)


def keyword_search(query: str, k: int = 5) -> pd.DataFrame:
    tokenized_query = tokenize(query)
    doc_scores = bm25.get_scores(tokenized_query)

    results_df = df.copy()
    results_df["bm25_score"] = doc_scores

    top_k_results = results_df.nlargest(k, "bm25_score")
    top_k_results["rank"] = range(1, len(top_k_results) + 1)

    return top_k_results[["rank", "chunk_id", "repo_name", "bm25_score", "chunk_text"]]


if __name__ == "__main__":
    test_query = "api rate limiting"
    print(f"\nSearching for: '{test_query}'")

    results = keyword_search(test_query, k=3)

    for _, row in results.iterrows():
        print(f"\nRepo: {row['repo_name']}")
        print(f"Chunk ID: {row['chunk_id']}")
        print(f"Score: {row['bm25_score']:.4f}")
        print(f"Snippet: {row['chunk_text'][:150]}...")
from vector_search import vector_search
from keyword_search import keyword_search

def rrf_fusion(vector_results, bm25_results, k=20):
  scores = {}

  # Vector scores (ranks)
  for rank, repo in enumerate(vector_results, start=1):
    scores[repo] = scores.get(repo, 0) + 1 / (k+rank)

  # BM25 scores (ranks)
  for rank, repo in enumerate(bm25_results, start=1):
    scores[repo] = scores.get(repo, 0) + 1 / (k+rank)

  # Sort the scores
  ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
  return [repo for repo, _ in ranked]

def hybrid_search(query, k=10):
  vector_results = vector_search(query, k)
  bm25_results = keyword_search(query, k)
  fused = rrf_fusion(vector_results, bm25_results)
  return fused[:k]

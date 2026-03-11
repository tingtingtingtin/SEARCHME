from keyword_search import keyword_search
import json

with open("data/ground_truth.json") as f:
    ground_truth = json.load(f)

def calculate_metrics(retrieved_ids, relevant_ids, k):
    retrieved_k = retrieved_ids[:k]
    
    relevant_set = set(relevant_ids)
    retrieved_set = set(retrieved_k)
    
    true_positives = len(relevant_set.intersection(retrieved_set))
    
    precision = true_positives / k
    recall = true_positives / len(relevant_set) if len(relevant_set) > 0 else 0.0
    
    return precision, recall

k_value = 5
total_precision = 0.0
total_recall = 0.0

print(f"\nBaseline Keyword Evaluation (K={k_value})")
print("------------------------------------------")

for query, relevant_docs in ground_truth.items():
    results_df = keyword_search(query, k=k_value)
    retrieved_docs = results_df['chunk_id'].tolist()
    
    p, r = calculate_metrics(retrieved_docs, relevant_docs, k_value)
    total_precision += p
    total_recall += r
    
    print(f"Query: '{query}'")
    print(f"- P@{k_value}: {p:.2f}")
    print(f"- R@{k_value}: {r:.2f}")

avg_precision = total_precision / len(ground_truth)
avg_recall = total_recall / len(ground_truth)

print("\nFinal Baseline Scores")
print("------------------------------------------")
print(f"Average Precision@{k_value}: {avg_precision:.4f}")
print(f"Average Recall@{k_value}: {avg_recall:.4f}")
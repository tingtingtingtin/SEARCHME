from google.cloud import bigquery
from sentence_transformers import SentenceTransformer
import torch

_model_cache = {}

def get_model() -> SentenceTransformer:
    if "all-minilm" not in _model_cache:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _model_cache["all-minilm"] = SentenceTransformer(
            'all-MiniLM-L6-v2',
            device=device
        )
    return _model_cache["all-minilm"]


def get_embedding(text: str) -> list[float]:
    model = get_model()

    vec = model.encode(
        text,
        normalize_embeddings=True
    )

    return vec.tolist()

client = bigquery.Client()

PROJECT = "search-me-cs226"
DATASET = "searchme_dataset"
TABLE = "embeddings_spark_50k_clean"


def vector_search(query: str, k: int = 10) -> list[str]:
    embedding = get_embedding(query)
    sql = f"""
    WITH results AS (
        SELECT
            base.repo_name,
            distance
        FROM VECTOR_SEARCH(
            TABLE `{PROJECT}.{DATASET}.{TABLE}`,
            'embedding',
            (SELECT {embedding} AS embedding),
            top_k => {k * 10},
            distance_type => 'COSINE'
        )
    )

    SELECT
        repo_name,
        MIN(distance) AS best_distance
    FROM results
    GROUP BY repo_name
    ORDER BY best_distance ASC
    LIMIT {k}
    """

    df = client.query(sql).to_dataframe()
    return df["repo_name"].tolist()

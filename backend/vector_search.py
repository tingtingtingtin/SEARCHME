from google.cloud import bigquery
import vertexai
from vertexai.language_models import TextEmbeddingModel

vertexai.init(project= "search-me-cs226", location="us-central1")

model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")

client = bigquery.Client()

PROJECT = "search-me-cs226"
DATASET = "searchme_dataset"
TABLE = "subset_50k_gemini_embeddings"

def vector_search(query, k=10):
    embedding = model.get_embeddings([query])[0].values
    sql = f"""
    SELECT
        base.repo_name
    FROM VECTOR_SEARCH(
        TABLE `{PROJECT}.{DATASET}.{TABLE}`, 
        'embedding', 
        (SELECT {embedding} AS embedding),
        top_k => {k}
    )
    """

    df = client.query(sql).to_dataframe()
    return df["repo_name"].tolist()

print(vector_search("A calculator that can do multiplication"))

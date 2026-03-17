import os
from google.cloud import bigquery
import pandas as pd
from dotenv import load_dotenv

load_dotenv() 

project_id = os.getenv("PROJECT_ID")
dataset_name = os.getenv("DATASET_NAME")

client = bigquery.Client(project=project_id)

query = f"""
    SELECT chunk_id, repo_name, chunk_text 
    FROM `{project_id}.searchme_dataset.test_embeddings_cleaned_subset`
"""
df = client.query(query).to_dataframe()

print(f"Extracted {len(df)} rows")
# for having a local copy of the data

csv_filename = "local_repo_data.csv" 
df.to_csv(csv_filename, index=False)


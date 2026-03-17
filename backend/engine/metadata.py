from google.cloud import bigquery

client = bigquery.Client()

def get_metadata(repo_names: list[str]) -> list[dict]:
    ids_str = ", ".join(f'"{r}"' for r in repo_names)
    query = f"""
        SELECT repo_name, stars, license, readme_text
        FROM `search-me-cs226.searchme_dataset.cleaned_readme_subset_50k`
        WHERE repo_name IN ({ids_str})
    """
    rows = list(client.query(query).result())

    rows_by_name = {}
    for row in rows:
        owner = row["repo_name"].split("/")[0]
        rows_by_name[row["repo_name"]] = {
            "repo_name": row["repo_name"],
            "owner": owner,
            "stars": row["stars"],
            "license": row["license"],
            "readme_snippet": row["readme_text"][:300] if row["readme_text"] else None
        }

    return [rows_by_name[name] for name in repo_names if name in rows_by_name]
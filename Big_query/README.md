# README Dataset Preparation Pipeline

## Overview

This document explains how to reproduce the dataset preparation pipeline used to build a README corpus from the BigQuery GitHub public dataset for information retrieval experiments.

The goal of this pipeline is to:

• Identify repositories containing README files  
• Extract README file paths  
• Retrieve README text  
• Clean the dataset  
• Produce a usable corpus for retrieval and embeddings  

---

## Pipeline Architecture

BigQuery GitHub files dataset  
        ↓  
README path extraction  
        ↓  
Root README filtering  
        ↓  
README text extraction  
        ↓  
Clean corpus table  
        ↓  
Experimental subset  

---

## STEP 0 — Verify dataset access

Purpose:
Confirm BigQuery connection works.

Query:

SELECT COUNT(*) AS total_files
FROM `bigquery-public-data.github_repos.files`;

---

## STEP 1 — Inspect dataset structure

Purpose:
Understand available columns.

Query:

SELECT *
FROM `bigquery-public-data.github_repos.files`
LIMIT 1;

Important columns:

repo_name  
path  
size  
content_id  

---

## STEP 2 — Detect README files

Purpose:
Verify README detection logic.

Query:

SELECT
repo_name,
path
FROM `bigquery-public-data.github_repos.files`
WHERE LOWER(path) LIKE '%readme%'
LIMIT 50;

---

## STEP 3 — Create initial README subset

Purpose:
Create manageable working dataset.

Query:

CREATE OR REPLACE TABLE `search-me-cs226.searchme_dataset.readme_subset` AS
SELECT
repo_name,
path AS readme_path
FROM `bigquery-public-data.github_repos.files`
WHERE LOWER(path) LIKE '%readme%'
LIMIT 10000;

Result:
Table containing repo names and README paths.

---

## STEP 4 — Validate dataset size

Purpose:
Confirm table creation.

Query:

SELECT COUNT(*) AS total_readmes
FROM `search-me-cs226.searchme_dataset.readme_subset`;

---

## STEP 5 — Analyze README distribution

Purpose:
Identify repositories with multiple README files.

Query:

SELECT
repo_name,
COUNT(*) AS readme_count
FROM `search-me-cs226.searchme_dataset.readme_subset`
GROUP BY repo_name
ORDER BY readme_count DESC
LIMIT 10;

---

## STEP 6 — Filter root-level READMEs

Purpose:
Keep only root README files.

Valid examples:

README  
README.md  

Removed examples:

docs/README.md  
lib/README.md  
examples/README  

Query:

CREATE OR REPLACE TABLE `search-me-cs226.searchme_dataset.cleaned_readme_subset` AS
SELECT
repo_name,
readme_path
FROM `search-me-cs226.searchme_dataset.readme_subset`
WHERE REGEXP_CONTAINS(readme_path, r'(?i)^readme(\.md)?$');

---

## STEP 7 — Count cleaned dataset

Purpose:
Confirm filtering.

Query:

SELECT COUNT(*) AS cleaned_repo_count
FROM `search-me-cs226.searchme_dataset.cleaned_readme_subset`;

---

## STEP 8 — Export repository list

Purpose:
Generate repo list for README extraction.

Query:

SELECT repo_name
FROM `search-me-cs226.searchme_dataset.cleaned_readme_subset`;

Export this result as CSV.

---

## STEP 9 — README extraction (external step)

Because BigQuery does not expose README text directly, README content was fetched using a Python script `readme_reader.py`.

Process:

1 Export repo list  
2 Fetch README from GitHub raw URLs  
3 Store README text  
4 Upload CSV back into BigQuery  

Result table:

readme_corpus

Typical schema:

string_field_0 → repo_name  
string_field_1 → readme_text  

---

## STEP 10 — Clean uploaded corpus schema

Purpose:
Create proper column names.

Query:

CREATE OR REPLACE TABLE `search-me-cs226.searchme_dataset.readme_corpus_clean` AS
SELECT
string_field_0 AS repo_name,
string_field_1 AS readme_text
FROM `search-me-cs226.searchme_dataset.readme_corpus`;

---

## STEP 11 — Verify README text

Purpose:
Ensure text imported correctly.

Query:

SELECT
repo_name,
LEFT(readme_text,200) AS preview
FROM `search-me-cs226.searchme_dataset.readme_corpus_clean`
LIMIT 5;

---

## STEP 12 — Create final clean corpus

Purpose:
Remove low-quality READMEs.

Query:

CREATE OR REPLACE TABLE `search-me-cs226.searchme_dataset.cleaned_readme_text_subset` AS
SELECT
repo_name,
readme_text
FROM `search-me-cs226.searchme_dataset.readme_corpus_clean`
WHERE LENGTH(readme_text) > 200;

---

## STEP 13 — Final dataset size

Purpose:
Determine usable corpus size.

Query:

SELECT COUNT(*) AS final_repo_count
FROM `search-me-cs226.searchme_dataset.cleaned_readme_text_subset`;

Example result:

224 repositories

---

## STEP 14 — Dataset statistics

Purpose:
Generate metrics for report.

Query:

SELECT
COUNT(*) AS repos,
AVG(LENGTH(readme_text)) AS avg_readme_size,
MAX(LENGTH(readme_text)) AS largest_readme
FROM `search-me-cs226.searchme_dataset.cleaned_readme_text_subset`;

---

## OPTIONAL — Create larger 4K dataset

Purpose:
Create larger experimental corpus.

Query:

CREATE OR REPLACE TABLE `search-me-cs226.searchme_dataset.readme_subset_4k` AS
WITH root_readmes AS (
SELECT DISTINCT
repo_name,
path AS readme_path
FROM `bigquery-public-data.github_repos.files`
WHERE NOT CONTAINS_SUBSTR(path, "/")
AND REGEXP_CONTAINS(LOWER(path), r'^readme(\.md)?$')
)

SELECT
repo_name,
readme_path
FROM root_readmes
ORDER BY FARM_FINGERPRINT(repo_name)
LIMIT 4000;

---

## OPTIONAL — Pull README text from sample_contents

Purpose:
Retrieve README text directly inside BigQuery.

Query:

CREATE OR REPLACE TABLE `search-me-cs226.searchme_dataset.readme_corpus_4k` AS
SELECT
s.repo_name,
s.readme_path,
SAFE_CONVERT_BYTES_TO_STRING(c.content) AS readme_text
FROM `search-me-cs226.searchme_dataset.readme_subset_4k` s
JOIN `bigquery-public-data.github_repos.sample_contents` c
ON c.repo_name = s.repo_name
AND c.path = s.readme_path
WHERE c.content IS NOT NULL;

---

## Final Tables

readme_subset → Initial README paths  
cleaned_readme_subset → Root README paths  
readme_corpus → Uploaded README text  
readme_corpus_clean → Clean schema  
cleaned_readme_text_subset → Final experiment dataset  
readme_subset_4k → Larger candidate set  
readme_corpus_4k → Larger text corpus  

---

## Final Dataset Structure

repo_name      STRING  
readme_text    STRING  

Used for:

BM25 retrieval  
TF-IDF  
Dense embeddings  
Hybrid search  

---

## Notes

Small dataset (200–500 repos):
Used for debugging.

Medium dataset (2k–5k repos):
Used for retrieval experiments.

Large dataset:
Used only after pipeline stability.

---

## Next Steps

This dataset will be used for:

Document indexing  
Tokenization  
Embedding generation  
Retrieval evaluation  
Hybrid search experiments

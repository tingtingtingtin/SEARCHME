CREATE OR REPLACE TABLE `search-me-cs226.searchme_dataset.readme_subset_sample_contents` AS
SELECT
  r.repo_name,
  c.content AS readme_text,
  r.watch_count AS stars,
  l.license
FROM
  `bigquery-public-data.github_repos.sample_repos` AS r
JOIN
  `bigquery-public-data.github_repos.sample_files` AS f ON r.repo_name = f.repo_name
JOIN
  `bigquery-public-data.github_repos.sample_contents` AS c ON f.id = c.id
LEFT JOIN
  `bigquery-public-data.github_repos.licenses` AS l ON r.repo_name = l.repo_name
WHERE
  f.path = 'README.md'
  AND r.watch_count > 5
  AND c.size BETWEEN 200 AND 100000;
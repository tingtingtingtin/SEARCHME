import csv
import time
import random
from pathlib import Path

import requests


INPUT_FILE = r"C:\Users\Vignesh\Desktop\big-data\bquxjob_39862929_19cb7f6f7c3.csv"

# Output CSV with README text
OUTPUT_FILE = "readme_corpus2.csv"

# Optional: write failures for debugging
FAILURES_FILE = "readme_failures.csv"

# Progress / throttling
PRINT_EVERY = 10           # print status every N repos
SLEEP_SECONDS = 0.25       # small delay to be polite (adjust if needed)
TIMEOUT_SECONDS = 15

# If your input CSV is huge, you can limit for testing:
MAX_REPOS = None  # e.g., 200 for quick test, or None for all



def raw_github_url(repo: str, ref: str, path: str) -> str:
    # raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}
    return f"https://raw.githubusercontent.com/{repo}/{ref}/{path.lstrip('/')}"


def candidate_paths_from_row(readme_path: str | None) -> list[str]:
    """
    Build a small set of candidate README paths to try.
    If BigQuery gave you a path (maybe nested), we try:
      1) that exact path
      2) root-level README variants
    """
    candidates = []
    if readme_path:
        candidates.append(readme_path.strip())

        # If it's nested, also try the basename at root (sometimes that’s what you want)
        p = Path(readme_path.strip())
        if str(p.name) and str(p.name) != readme_path.strip():
            candidates.append(p.name)

    # Common root-level README variants
    candidates += [
        "README.md",
        "README.MD",
        "README",
        "readme.md",
        "readme",
        "Readme.md",
        "README.txt",
        "README.rst",
        "README.markdown",
    ]

    # Deduplicate while preserving order
    seen = set()
    out = []
    for c in candidates:
        if c and c not in seen:
            out.append(c)
            seen.add(c)
    return out


def fetch_readme_text(session: requests.Session, repo: str, readme_path: str | None) -> tuple[str | None, str | None]:
    """
    Try multiple refs and multiple paths:
      refs: main, master
      paths: readme_path from input + common root variants
    Returns (text, used_url) or (None, None)
    """
    refs = ["main", "master"]
    paths = candidate_paths_from_row(readme_path)

    for ref in refs:
        for path in paths:
            url = raw_github_url(repo, ref, path)
            try:
                r = session.get(url, timeout=TIMEOUT_SECONDS)
                if r.status_code == 200 and r.text and len(r.text.strip()) > 0:
                    return r.text, url
            except requests.RequestException:
                pass

    return None, None


def main():
    if not Path(INPUT_FILE).exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    # Read repos + readme_path from CSV
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows_in = list(reader)

    if MAX_REPOS is not None:
        rows_in = rows_in[:MAX_REPOS]

    total = len(rows_in)
    if total == 0:
        print("No rows found in input CSV.")
        return

    # Prepare outputs
    out_rows = []
    fail_rows = []

    ok = 0
    missing = 0

    session = requests.Session()
    session.headers.update({
        "User-Agent": "cs226-readme-fetcher/1.0 (educational)"
    })

    start = time.time()

    for i, row in enumerate(rows_in, start=1):
        repo = (row.get("repo_name") or "").strip()
        readme_path = (row.get("readme_path") or "").strip() if row.get("readme_path") else None

        if not repo:
            missing += 1
            fail_rows.append({"repo_name": "", "reason": "missing repo_name", "tried": ""})
            continue

        text, used_url = fetch_readme_text(session, repo, readme_path)

        if text is not None:
            ok += 1
            out_rows.append({
                "repo_name": repo,
                "readme_text": text
            })
        else:
            missing += 1
            fail_rows.append({
                "repo_name": repo,
                "reason": "README not found (tried main/master + variants)",
                "tried": f"input_path={readme_path or ''}"
            })

        # Progress printing
        if i == 1 or i % PRINT_EVERY == 0 or i == total:
            elapsed = time.time() - start
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total - i) / rate if rate > 0 else 0
            print(
                f"[{i}/{total}] ok={ok} missing={missing} "
                f"({ok/ i * 100:.1f}% success) "
                f"elapsed={elapsed:.1f}s ETA={eta:.1f}s"
            )

        # polite delay + tiny jitter (helps avoid rate limiting patterns)
        time.sleep(SLEEP_SECONDS + random.uniform(0, 0.05))

    # Write output CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["repo_name", "readme_text"])
        writer.writeheader()
        writer.writerows(out_rows)

    # Write failures CSV
    with open(FAILURES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["repo_name", "reason", "tried"])
        writer.writeheader()
        writer.writerows(fail_rows)

    elapsed = time.time() - start
    print("\nDONE.")
    print(f"Saved: {OUTPUT_FILE}  (rows={len(out_rows)})")
    print(f"Saved: {FAILURES_FILE} (rows={len(fail_rows)})")
    print(f"Total time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
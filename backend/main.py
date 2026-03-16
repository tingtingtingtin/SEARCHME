from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from engine.vector_search import vector_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://search-me-cs226.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoResult(BaseModel):
    repo_name: str
    owner: str
    stars: int
    license: Optional[str]

class SearchResponse(BaseModel):
    total_results: int
    results: List[RepoResult]

@app.get("/api/search", response_model=SearchResponse)
def search_repos(q: str):
    repo_names = vector_search(q, k=10)

    # stub metadata until BQ lookup is wired in
    results = []
    for repo_name in repo_names:
        owner = repo_name.split("/")[0]
        results.append({
            "repo_name": repo_name,
            "owner": owner,
            "stars": 0,
            "license": None
        })

    return {
        "total_results": len(results),
        "results": results
    }
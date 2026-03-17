from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from engine.rrf import hybrid_search
from engine.metadata import get_metadata

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
    readme_snippet: Optional[str]

class SearchResponse(BaseModel):
    total_results: int
    results: list[RepoResult]

@app.get("/api/search", response_model=SearchResponse)
def search_repos(q: str, k: int = 10):
    repo_names = hybrid_search(q, k=k)
    results = get_metadata(repo_names)
    return {
        "total_results": len(results),
        "results": results
    }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoResult(BaseModel):
    id: str
    repo_name: str
    owner: str
    stars: int
    forks: int
    last_updated: str
    description: str

class SearchResponse(BaseModel):
    total_results: int
    results: List[RepoResult]

@app.get("/api/search", response_model=SearchResponse)
def search_repos(q: str, sort: str = "stars"):
    mock_results = [
        {
            "id": "1",
            "repo_name": "threejs-splat",
            "owner": "tingtingtingtin",
            "stars": 12,
            "forks": 2,
            "last_updated": "4 weeks ago",
            "description": "lorem ipsum lorem ipsum lorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsum"
        },
        {
            "id": "2",
            "repo_name": "bru",
            "owner": "ajarean",
            "stars": 8,
            "forks": 1,
            "last_updated": "2 days ago",
            "description": "lorem ipsum lorem ipsum lorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsum"
        }
    ]
    return {
        "total_results": 30,
        "results": mock_results
    }
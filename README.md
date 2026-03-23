# SEARCHME

SEARCHME is a GitHub repository hybrid search engine.

**Group:** SEARCHME (Group 06)

**Members:**
- Tingxuan Wu
  - 862334354
  - twu148@ucr.edu
- Gurjot Singh
  - 862317808
  - gsing064@ucr.edu
- Vignesh Kumar
  - 862548391
  - vkuma045@ucr.edu
- Andy Jarean
  - 862341917
  - ajare002@ucr.edu
- Sazen Shakya
  - 862375704
  - sshak015@ucr.edu

## Author Contributions

- **Tingxuan Wu**: Frontend development (Vue 3), FastAPI backend and API layer, 
  system integration, Cloud Run and Firebase deployment, documentation.
- **Gurjot Singh**: Vector search implementation (BigQuery IVF index, 
  all-MiniLM-L6-v2 embeddings), reciprocal rank fusion (RRF), hybrid search integration, vector/hybrid search baseline evaluation (Precision@K, Recall@K).
- **Vignesh Kumar**: SQL dataset engineering, BigQuery extraction pipeline, 
  data cleaning and schema design.
- **Andy Jarean**: BM25 keyword search implementation, inverted index, 
  keyword search baseline evaluation (Precision@K, Recall@K).
- **Sazen Shakya**: Text chunking pipeline, distributed embedding generation 
  via Apache Spark, all-MiniLM-L6-v2 embedding model selection and validation.

## Project Structure

- `backend/`: FastAPI service and search engine modules.
- `backend/engine/`: Core retrieval logic.
	- `keyword_search.py`: BM25 keyword retrieval.
	- `vector_search.py`: BigQuery vector retrieval.
	- `reranker.py`: Reciprocal rank fusion for hybrid retrieval.
	- `metadata.py`: Repository metadata lookup and snippet cleanup.
- `frontend/`: Vue 3 + Vite web app.
	- `src/views/`: UI pages (`HomeView.vue`, `ResultsView.vue`).
	- `src/stores/search.ts`: Pinia search state and API calls.
	- `src/router/index.ts`: Application routes.
- `testing/`: Baseline evaluation and local data extraction scripts.
- `notebooks/`: Experimental pipelines and analysis notebooks.

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm 10+
- Google Cloud credentials configured for BigQuery access

## Backend Setup and Run

From the repo root:

```bash
cd backend
python -m venv .venv
```

Activate virtual environment:

- Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

API endpoint:

- `GET /api/search?q=<query>&k=<top_k>`

## Backend Compile/Build Options

Build and run Docker image:

```bash
cd backend
docker build -t searchme-backend .
docker run --rm -p 8080:8080 searchme-backend
```

## Frontend Setup and Run

Add a file called `.env` into the `frontend/` folder with the following contents:

```bash
#.env
VITE_API_URL=http://localhost:8080
```

From the repo root:

```bash
cd frontend
npm install
```

Run development server:

```bash
npm run dev
```

Create production build:

```bash
npm run build
```

Preview production build locally:

```bash
npm run preview
```

Lint frontend:

```bash
npm run lint
```

Format frontend:

```bash
npm run format
```

## Full Local Run (Backend + Frontend)

1. Start backend on `http://localhost:8080`.
2. Start frontend on `http://localhost:5173`.
3. Open frontend URL and submit a query.

## Testing/Data Scripts

The `testing/` scripts are for local baseline experiments and evaluation.

- `extract_data.py`: Pulls chunk data from BigQuery to a local CSV.
- `keyword_search_testing.py`: Runs BM25 retrieval on local CSV.
- `evaluation.py`: Computes precision and recall against local ground truth.

The `data/` scripts are for reproducibility of BigQuery queries not already present in existing scripts within the repository.

Some testing scripts expect local files such as `data/local_repo_data.csv` and `data/ground_truth.json`. These are intentionally not part of this repository archive, and must be generated via the testing scripts.

## Notebooks

- [Spark Embedding Pipeline](https://colab.research.google.com/drive/128jjl_-D-PxoewJgqRKXwoCX_gX_SSqn?usp=sharing)
- Additional notebooks are in `notebooks/` for exploratory workflows.

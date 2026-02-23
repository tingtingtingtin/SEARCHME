## backend folder structure

* **main.py** - fastAPI routes
* **engine/**
    * **keyword_search.py**: bm-25 stuff
    * **reranker.py**: rrf stuff
    * **vector_search.py**: pinecone stuff
* **models/**
    * pydantic schemas will go here (optional prob)
* **Dockerfile**
* **requirements.txt** - put things you install here pls

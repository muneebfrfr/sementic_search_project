from datetime import datetime
import logging
import os
from fastapi import FastAPI, Query, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
import uvicorn

from chromadb import PersistentClient
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


# Configure logging
logging.basicConfig(
    filename='query_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Function to get embedding from OpenAI
openai_client = OpenAI(api_key=os.getenv('OPENAI_KEY'))


def get_embedding(text):
    response = openai_client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


# Initialize ChromaDB client
chroma_client = PersistentClient(path="./final_permits_chroma_storage")

# Create collection with metadata indexing
collection = chroma_client.get_or_create_collection(
    name="permits_vector_data",
    metadata={"hnsw:space": "cosine"}  # ensures cosine similarity
)

app = FastAPI()

# --------- Input Schema ---------


class SearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, str]] = None
    top_k: Optional[int] = 5


# --------- Vector Search Function ---------
def search_permits(query: str, filters: dict = None, top_k: int = 5):
    try:
        # Embed the query
        query_embedding = get_embedding(query)

        # Construct `where` clause if filters are provided
        where_clause = None
        if filters:
            and_conditions = []
            for key, value in filters.items():
                if value is not None and str(value).strip() != "":
                    and_conditions.append({key: value})
            if and_conditions:
                where_clause = {"$and": and_conditions}

        # Perform query
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )

        # Format output
        output = []
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            output.append({
                "document": doc,
                "metadata": meta,
                "similarity_score": round(dist, 4)
            })

        log_entry = {
            "query": query,
            "filters": filters,
            "top_results": results
        }

        logging.info(f"Search Query Log: {log_entry}")

        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- API Route ---------
@app.post("/search")
def search_vector(request: SearchRequest):
    results = search_permits(
        query=request.query,
        filters=request.filters,
        top_k=request.top_k
    )
    return {"results": results}


@app.get("/healthz")
def health_check():
    return {"ok": True}


# --------- Run App ---------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

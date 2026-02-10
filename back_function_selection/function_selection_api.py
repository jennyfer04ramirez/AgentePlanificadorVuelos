from fastapi import FastAPI
import psycopg2
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from fastapi.middleware.cors import CORSMiddleware

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

conn = psycopg2.connect(
    host="aws-1-us-east-1.pooler.supabase.com",
    dbname="postgres",
    user="postgres.znkewdqukpfmzjmkfxea",
    password="planificador123",
    port=5432
)
cur = conn.cursor()



def select_function(query, top_k=3):
    query_emb = model.encode(query).tolist()
    cur.execute(
        """
        SELECT function_id, name,
               1 - (embedding <=> %s::vector) AS score
        FROM business_functions
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (query_emb, query_emb, top_k)
    )

    results = cur.fetchall()

    # Guardar query
    best = results[0]
    cur.execute(
        """
        INSERT INTO query_log (query_text, query_embedding, selected_function_id, score)
        VALUES (%s, %s, %s, %s)
        """,
        (query, query_emb, best[0], best[2])
    )
    conn.commit()

    return results

def select_function_langchain(query, top_k=3):
    query_emb = embedding_model.embed_query(query)

    cur.execute(
        """
        SELECT function_id, name,
               1 - (embedding <=> %s::vector) AS score
        FROM business_functions
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (query_emb, query_emb, top_k)
    )
    return cur.fetchall()



app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SelectFunctionRequest(BaseModel):
    query: str
    top_k: int = 3


@app.get("/")
def root():
    return {"message": "Function Selection API is running."}


@app.post("/select_function")
def api_select_function(req: SelectFunctionRequest):
    results = select_function(req.query, req.top_k)
    return {
        "query": req.query,
        "results": [
            {"function_id": r[0], "name": r[1], "score": r[2]} for r in results
        ]
    }
    
@app.post("/select_function_langchain")
def api_select_function_langchain(req: SelectFunctionRequest):
    results = select_function_langchain(req.query, req.top_k)
    return {
        "query": req.query,
        "results": [
            {"function_id": r[0], "name": r[1], "score": r[2]} for r in results
        ]
    }
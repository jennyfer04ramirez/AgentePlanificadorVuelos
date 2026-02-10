from app.core.database import get_connection

def get_top_functions(query_embedding, top_k):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT function_id, name, category,
               1 - (embedding <=> %s::vector) AS score
        FROM business_functions
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (query_embedding, query_embedding, top_k))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "function_id": r[0],
            "name": r[1],
            "category": r[2],
            "score": r[3]
        }
        for r in results
    ]   

from app.core.embeddings import embed_text
from app.core.vector_store import search_vectors
from app.core.llm import generate_llama_answer

def query_rag(question: str):
    query_emb = embed_text(question)
    results = search_vectors(query_emb)

    # Combine top 2 results for better context
    if results:
        # Take top 2 most relevant chunks
        relevant_chunks = [r.payload['text'] for r in results[:2]]
        context = " ".join(relevant_chunks)[:1500]  # Combine and limit length
        prompt = f"""Question: {question}

Resume information: {context}

Please answer the question based on the resume information above."""
    else:
        prompt = f"Please answer: {question}"

    answer = generate_llama_answer(prompt)

    sources = [r.payload.get("filename", "") for r in results]

    return answer, sources

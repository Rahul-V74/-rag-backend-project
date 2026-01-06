from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Filter, FieldCondition, MatchValue, Distance
from dotenv import load_dotenv
import os

load_dotenv()

# Get Qdrant configuration from environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL:
    raise ValueError("QDRANT_URL environment variable is required")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


COLLECTION = "rag_documents"

def init_vector_store():
    try:
        client.get_collection(collection_name=COLLECTION)
    except:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def insert_vectors(embeddings, texts, metadata=None):
    if metadata is None:
        metadata = {}

    points = [
        PointStruct(
            id=i,
            vector=embeddings[i],
            payload={"text": texts[i], **metadata}
        )
        for i in range(len(texts))
    ]

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )

def search_vectors(query_vector):
    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=5
    )
    return results.points



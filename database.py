import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path="./.chroma_db")

embedding_func = embedding_functions.DefaultEmbeddingFunction()

def get_or_create_session_collection(session_id: str):

    collection = chroma_client.get_or_create_collection(
        name=session_id,
        embedding_function=embedding_func
    )

    return collection

def add_documents_to_collection(session_id: str, chunks: list[str], metadatas: list[dict], ids: list[str]):
    collection = get_or_create_session_collection(session_id)

    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    return True

def query_session_collection(session_id: str, query_text: str, n_results: int = 3):
    try:
        collection = chroma_client.get_collection(
            name=session_id,
            embedding_function=embedding_func
        )
    except Exception:
        return None

    results = collection.query(
        query_texts=[query_text],
        n_results = n_results
    )

    return results

def delete_session_collection(session_id: str):
    try:
        chroma_client.delete_collection(name=session_id)
        return True
    except Exception:
        return False
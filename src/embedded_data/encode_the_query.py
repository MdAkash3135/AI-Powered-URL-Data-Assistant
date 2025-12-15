from sentence_transformers import SentenceTransformer
import faiss

def query_embed_chunks(chunks):
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    vectors = encoder.encode([chunks])


    return vectors
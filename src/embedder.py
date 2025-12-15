from sentence_transformers import SentenceTransformer
import faiss

def embed_chunks(chunks):
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    vectors = encoder.encode(chunks)
    print(vectors.shape)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index 
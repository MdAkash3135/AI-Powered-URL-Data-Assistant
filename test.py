from sentence_transformers import SentenceTransformer
import faiss

def embed_chunks(chunks):
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    vectors = encoder.encode(chunks)
    print(vectors.shape)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index

encoder = SentenceTransformer('all-MiniLM-L6-v2')

index = embed_chunks(chunks = [
                    
    "Sentence transformers create embeddings",  # index 1
    "Python is a programming language"  ,         # index 2
    "FAISS is a vector database"              # index 3
]
)

query = "FAISS is a vector database"
query_vector = encoder.encode([query])

matching_indices = index.search(query_vector, k=2)
print(matching_indices)  # Retrieve top 2 matches

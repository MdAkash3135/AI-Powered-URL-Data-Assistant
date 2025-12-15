import pickle

pickle_file_path = 'src/embedded_data/vector.pkl'

def save_faiss_index(index):
    with open(pickle_file_path, "wb") as f:
        pickle.dump(index, f)

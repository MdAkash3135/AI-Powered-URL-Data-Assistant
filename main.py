import os
import streamlit as st
import pickle
import time

from langchain_community.document_loaders import UnstructuredURLLoader
from sentence_transformers import SentenceTransformer

from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = ""

# llm = ChatGoogleGenerativeAI(model_name="gemini-2.5-flash", temperature=0.2)


from src.data_loader import load_data_from_urls
from src.chunker import chunk_text
from src.embedder import embed_chunks
from src.embedded_data.encode_the_query import query_embed_chunks
from src.embedded_data.store_embeded_data import save_faiss_index
from src.urls import url_receiver
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_classic.chains.retrieval_qa.base import RetrievalQA


st.title("AI-Powered URL Data Assistant")


st.sidebar.title("Finance News URLS")

mainplacefolder = st.empty()

urls = url_receiver()

file_path = 'src/embedded_data/vector.pkl'
pickle_file_path = 'src/embedded_data/vector.pkl'

process_url_clicked = st.sidebar.button("Process URLs")

docs_extractor = None
docs_file_path = 'src/data/urls_chunked_data.txt'


if process_url_clicked:
    #data extract 
    mainplacefolder.text("Data Loading .. Started............")
    data = load_data_from_urls(urls)

    #data chunkink
    docs = chunk_text(data)
    with open(docs_file_path, 'w') as f:
        f.write('\n\n'.join([doc for doc in docs]))
    print((docs[:20]))

    

    mainplacefolder.text("chunking has started .............")
    
    # vectorize the chukns
    embeded_index = embed_chunks(docs)

    #store the vectore in a pickle file
    binary_file = save_faiss_index(embeded_index)


query = mainplacefolder.text_input("Ask Related to this papers ")



if query:
   
    if os.path.exists(file_path):
        with open(pickle_file_path, "rb") as f:
            vectorestore = pickle.load(f)
            # print(vectorestore)
            
            mainplacefolder.text("Vectore store loaded from pickle file.")
            
            print(query)
            encoded_query = query_embed_chunks(query)
            # print("encoded query ", encoded_query)

            matching_vectors = vectorestore.search(encoded_query, k=20)

            
           

            mainplacefolder.text("Top matching chunks:")
            with open(docs_file_path, 'r') as f:
                all_chunks = f.read().split("\n\n")
            print("matching vectors ", matching_vectors)
           

            for i,c in enumerate(all_chunks):
                print("chunk -------------", {i})
                print(c)
            blannk_string = "\n\n"
            for c in matching_vectors[1][0]:
                
                blannk_string += all_chunks[c] + "\n\n"


            # print("blamnkd string ")
            # print(blannk_string)
            context = blannk_string
            question = query

            # print(context)
        
            prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""
                    Use the context below to answer the question concisely.

                    Context:
                    {context}

                    Question:
                    {question}

                    Answer:
                        """
                )


            gemini = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.0,
                max_output_tokens=12,
            )

            # -------- LCEL CHAIN -------- #

            chain = prompt | gemini

            # -------- Run chain -------- #

            response = chain.invoke({
                "context": context,
                "question": question
            })


            mainplacefolder.text_area("Matching Chunks", response.content, height=300)
    
            

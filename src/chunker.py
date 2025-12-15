from langchain_text_splitters import RecursiveCharacterTextSplitter



def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)
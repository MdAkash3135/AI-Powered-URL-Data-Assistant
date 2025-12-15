from langchain_community.document_loaders import UnstructuredURLLoader

def load_data_from_urls(urls):
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    return data[0].page_content
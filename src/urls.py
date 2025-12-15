import streamlit as st

urls = []
def url_receiver():
    for i in range(1, 4):
        url = st.sidebar.text_input(f"Finance News URL {i}", key=f"url_{i}")
        if url:
            st.sidebar.write(f"URL {i}: {url}")
            urls.append(url)
    
    return urls
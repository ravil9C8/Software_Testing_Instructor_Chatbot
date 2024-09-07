
import os
import streamlit as st
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.nvidia import NVIDIA

from document_processors import load_multimodal_data, load_data_from_directory
from utils import set_environment_variables

# Set up the page configuration
st.set_page_config(page_title="Multimodal RAG System", layout="wide", page_icon="🤖")

# Initialize settings
def initialize_settings():
    Settings.embed_model = NVIDIAEmbedding(model="nvidia/nv-embedqa-e5-v5", truncate="END")
    Settings.llm = NVIDIA(model="meta/llama-3.1-70b-instruct")
    Settings.text_splitter = SentenceSplitter(chunk_size=600)

# Create index from documents
def create_index(documents):
    vector_store = MilvusVectorStore(
            host = "127.0.0.1",
            port = 19530,
            dim = 1024
    )
    # vector_store = MilvusVectorStore(uri="./milvus_demo.db", dim=1024, overwrite=True) #For CPU only vector store
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Main function to run the Streamlit app
def main():
    set_environment_variables()
    initialize_settings()

    st.title("🤖 Multimodal RAG System")
    st.markdown("### Upload files or specify a directory, then chat with the assistant below")

    # Create two columns for file upload and directory input side by side
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🖼️ Upload Files")
        uploaded_files = st.file_uploader("Drag and drop files here", accept_multiple_files=True)
        if uploaded_files and st.button("📝 Describe Testing Screenshots"):
            with st.spinner("Processing files..."):
                documents = load_multimodal_data(uploaded_files)
                st.session_state['index'] = create_index(documents)
                st.session_state['history'] = []
                st.success("✅ Files processed and index created!")

    with col2:
        st.subheader("📂 Enter Directory Path")
        directory_path = st.text_input("Enter directory path:")
        if directory_path and st.button("📁 Process Directory"):
            if os.path.isdir(directory_path):
                with st.spinner("Processing directory..."):
                    documents = load_data_from_directory(directory_path)
                    st.session_state['index'] = create_index(documents)
                    st.session_state['history'] = []
                    st.success("✅ Directory processed and index created!")
            else:
                st.error("❌ Invalid directory path. Please enter a valid path.")

    # Chat section below the file upload and directory options
    st.markdown("---")  # Horizontal line to separate sections
    st.subheader("💬 Chat with Assistant")
    
    if 'index' in st.session_state:
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        
        query_engine = st.session_state['index'].as_query_engine(similarity_top_k=20, streaming=True)

        user_input = st.chat_input("💡 Enter your query:")

        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state['history']:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state['history'].append({"role": "user", "content": user_input})
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                response = query_engine.query(user_input)
                for token in response.response_gen:
                    full_response += token
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state['history'].append({"role": "assistant", "content": full_response})

        # Add a clear button with an icon
        if st.button("🧹 Clear Chat"):
            st.session_state['history'] = []
            st.rerun()

if __name__ == "__main__":
    main()

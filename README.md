# Creating Multimodal AI Agent for getting Software Testing Instructions

## Overview

This Streamlit-based web app allows users to upload multiple screenshots and optionally provide context to generate detailed software testing instructions. The back-end leverages a multimodal LLM to process the inputs, generating step-by-step test cases for each functionality. Each test case includes a description, pre-conditions, testing steps, and expected results, ensuring comprehensive testing coverage for various features. The user-friendly interface enables efficient creation of testing documentation with minimal effort.


The system leverages LlamaIndex for efficient information indexing and retrieval, NIM microservices for high-performance inference, and Milvus as a vector database for optimized storage and retrieval of embedding vectors. This integration of technologies enables the application to manage complex multimodal data, perform advanced querying, and deliver fast, context-aware responses to user questions.

## Features

- **Multi-format Document Processing**: Supports text files, PDFs, PowerPoint presentations, and images.
- **Advanced Text Extraction**: Retrieves text from PDFs and PowerPoint slides, including tables and embedded images.
- **Image Analysis**: Employs a VLM (NeVA) for image descriptions and Google's DePlot for analyzing graphs and charts via NIM microservices.
- **Vector Store Indexing**: Generates a searchable index of processed documents using Milvus vector store.
- **Interactive Chat Interface**: Provides a chat-like interface for users to query processed information interactively.

## Setup

1. Clone the repository:
```
git clone https://github.com/NVIDIA/GenerativeAIExamples.git
cd  multimodal_rag
```

2.Create a conda environment or a virtual environment:

   - Using conda:
     ```
     conda create --name your-name python=3.10
     conda activate multimodal-rag
     ```


3. Install the required python packages for the project:
```
pip install -r requirements.txt
```

4. Set up your NVIDIA API key as an environment variable:
```
export NVIDIA_API_KEY="your-api-key-here"
```


## Usage

1. Run the Streamlit app:
```
streamlit run app.py
```

3. Open the provided URL in your web browser.

4. Choose between uploading files or specifying a directory path containing your documents.

5. Process the files by clicking the "Describe Testing Instructions" button.

6. Once processing is complete, use the chat interface to query your documents for it to describe Software testing Instructions. # Software_Testing_Instructor_Chatbot

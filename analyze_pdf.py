import streamlit as st
import openai
from PIL import Image
import cv2
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore

# Set up OpenAI API
openai.api_key = st.secrets["OPEN_AI_API_KEY"]
embeddings = OpenAIEmbeddings(
    openai_api_key=openai.api_key, model="text-embedding-3-small"
)
index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

# Initialize FAISS Vector Store
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)


# Define functions for different processing tasks
def process_text(text):
    st.write("Processing text with Langchain...")
    embedding = embeddings.embed_query(text)
    return embedding


def process_image(image):
    st.write("Processing image using OpenAI Vision API...")
    # Placeholder for processing images and extracting embeddings
    response = openai.Image.create(file=image, purpose="embeddings")
    embedding = response["data"][0]["embedding"]
    return np.array(embedding)


def process_video(video_file):
    st.write("Extracting frames from video...")
    video_capture = cv2.VideoCapture(video_file)
    frames = []
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frames.append(frame)
    video_capture.release()
    return process_image(frames[0])


def add_to_vector_store(embedding, metadata):
    vector_store.add_documents([{"content": embedding, "metadata": metadata}])


def perform_similarity_search(query_embedding):
    st.write("Performing similarity search using Langchain + FAISS...")
    # Perform similarity search using the FAISS index
    results = vector_store.similarity_search(query_embedding, k=5)
    return results


# UI for customer input
st.title("Data Input System")

# Based on selected input type, different options will appear
input_text = st.text_area("Enter text data:")
if st.button("Process Text"):
    embedding = process_text(input_text)
    add_to_vector_store(embedding, {"type": "text", "content": input_text})
    st.write("Text embedding added to vector store.")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image and st.button("Process Image"):
    image = Image.open(uploaded_image)
    embedding = process_image(uploaded_image)
    add_to_vector_store(embedding, {"type": "image"})
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Image embedding added to vector store.")

uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
if uploaded_video and st.button("Process Video"):
    embedding = process_video(uploaded_video)
    add_to_vector_store(embedding, {"type": "video"})
    st.video(uploaded_video)
    st.write("Video embedding added to vector store.")

user_query = st.text_area("Enter your query or filters:")
if st.button("Process Query"):
    query_embedding = process_text(user_query)
    results = perform_similarity_search(query_embedding)
    st.write("Matching Results:", results)

# Similarity Search and Matching Engine
st.write("Matching Results: [Results will be displayed here]")

import os
from flask import Flask, render_template, request
from langchain.document_loaders import PyPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

import numpy as np
import faiss

# get key from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


def get_openai_embeddings(texts, openai_api_key):
    # Initialize the OpenAIEmbeddings object
    embeddings_obj = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Call the appropriate method to get embeddings for the texts
    embeddings = embeddings_obj.embed_documents(texts)

    return np.array(embeddings)


def get_texts_embeddings_and_index_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    data = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    # Get the embeddings for your texts
    embeddings = get_openai_embeddings([t.page_content for t in texts], openai_api_key=OPENAI_API_KEY)

    # Build the FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.astype('float32'))

    return texts, embeddings, index


def get_top_docs(query, index, texts, k=10):
    query_embedding = get_openai_embeddings([query], openai_api_key=OPENAI_API_KEY)
    query_embedding = query_embedding.astype('float32')
    distances, indices = index.search(query_embedding, k=k)

    # Query those docs to get your answer back
    top_docs = [texts[i] for i in indices[0]]
    return top_docs


def query_docs(query, docs):
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    results = chain.run(input_documents=docs, question=query)
    return results


# create flask app
app = Flask(__name__)

# create route


@app.route('/load', methods=['GET'])
def load():
    pdfFile = request.args.get('pdfFile')
    global texts, embeddings, index
    texts, embeddings, index = get_texts_embeddings_and_index_from_pdf(pdfFile)
    return "loaded"


@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('query')
    # get k argument in an int
    k = int(request.args.get('k'))
    top_docs = get_top_docs(query, index, texts, k=k)
    results = query_docs(query, top_docs)
    return results


# run app
if __name__ == '__main__':
    app.run(debug=True)

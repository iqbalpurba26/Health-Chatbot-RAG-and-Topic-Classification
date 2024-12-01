"""retrieval.py for information retrieval from knowledge base chatbot"""
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma


embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory = 'vectorstore'

def get_chromaDB(persist_directory, embedding_function = embedding_model):
    """
    This function to get vectorstore/vectoredb from chromaDB

    Args:
    perist_directory: directory chromaDB where saved
    embedding_function: embedding model used to tokenize knowledge base

    Return:
    vectorstore: A List of knowledge base are tokenized
    """
    print(f"Mencoba untuk menghubungkan ke direktori: {persist_directory}")
    try:
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function
        )
        print("Berhasil terhubung dengan ChromaDB!")
        return vectorstore
    except Exception as e:
        print(f"Gagal menghubungkan ke ChromaDB: {str(e)}")
        return None

def retrieve(topic, prompt, top_k=5, persist_directory=persist_directory):
    """
    This function to information retrieval in vector database or vector store

    Args:
    perist_directory: directory ChromaDB where saved
    intent: intent class from prompt
    prompt: user question
    top_k: maximal information relevant search
    """
    vectorstore = get_chromaDB(persist_directory=persist_directory)
    print('berhasil mendapatkan database')
    retriever = vectorstore.as_retriever()
    retriever.search_kwargs["filter"] = {"intent":topic}
    
    content = retriever.get_relevant_documents(prompt, top_k=top_k)
    information_relevant = [doc.page_content for doc in content]
    print(information_relevant)
    return information_relevant


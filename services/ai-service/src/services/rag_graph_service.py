import uuid
from typing import List, TypedDict

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

from .retrieval_service import get_vector_store_retriever
from ..core import config

# --- 1. Define the State of our Graph ---
# The state is a dictionary that will be passed between nodes.
class GraphState(TypedDict):
    question: str
    warranty_id: uuid.UUID
    documents: List[Document]
    generation: str

# --- 2. Define the Nodes of our Graph ---
# Each node is a function that modifies the state.

def retrieve_documents(state: GraphState):
    """
    Node to retrieve documents from the vector store.
    """
    print("---NODE: RETRIEVE DOCUMENTS---")
    question = state["question"]
    warranty_id = state["warranty_id"]
    
    # Get the retriever for the specific warranty
    retriever = get_vector_store_retriever(warranty_id)
    
    # Retrieve documents and add them to the state
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question, "warranty_id": warranty_id}

def generate_answer(state: GraphState):
    """
    Node to generate an answer using the LLM.
    """
    print("---NODE: GENERATE ANSWER---")
    question = state["question"]
    documents = state["documents"]

    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise."),
        ("human", "Question: {question}\n\nContext:\n{context}")
    ])
    
    # LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=config.GEMINI_API_KEY)
    
    # Format the documents into a single string
    context = "\n\n".join(doc.page_content for doc in documents)
    
    # RAG chain
    rag_chain = prompt | llm | StrOutputParser()
    
    # Run the chain and get the generation
    generation = rag_chain.invoke({"context": context, "question": question})
    return {"documents": documents, "question": question, "generation": generation}

# --- 3. Build and Compile the Graph ---

# Initialize a new graph
workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("retrieve", retrieve_documents)
workflow.add_node("generate", generate_answer)

# Set the entrypoint
workflow.set_entry_point("retrieve")

# Add the edges
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

# Compile the graph into a runnable app
app = workflow.compile()

# Optional: To visualize the graph, you can install graphviz and run:
# from langchain.utils.mermaid import mermaid_png
# mermaid_png(app.get_graph(), "rag_graph.png")
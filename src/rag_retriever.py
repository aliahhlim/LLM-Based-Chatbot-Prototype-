import os
import chromadb
from chromadb.utils import embedding_functions
from src.knowledge_base import KnowledgeBaseProcessor

class RAGRetriever:
    def __init__(self, chroma_db_path="./chroma_db"):
        self.chroma_db_path = chroma_db_path
        self.client = None
        self.collection = None
        
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        # self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        #     model_name="all-MiniLM-L3-v2"  # Smaller one
        # )
    
    def setup_vector_database(self):
        self.client = chromadb.PersistentClient(path=self.chroma_db_path)
        
        try:
            self.collection = self.client.get_collection("uitm_knowledge")
        except:
            self.collection = self.client.create_collection(
                name="uitm_knowledge",
                embedding_function=self.embedding_function
            )
    
    def index_documents(self):
        processor = KnowledgeBaseProcessor()
        documents = processor.load_documents()
        
        if not documents:
            print("No documents found to index")
            return
        
        chunks = processor.chunk_documents()
        
        if not chunks:
            print("No chunks created")
            return
        
        ids = []
        documents_text = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            ids.append(f"chunk_{i}")
            documents_text.append(chunk["text"])
            metadatas.append(chunk["metadata"])
        
        self.collection.add(
            documents=documents_text,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Successfully indexed {len(chunks)} document chunks")
    
    def retrieve_documents(self, query, n_results=3):
        if not self.collection:
            self.setup_vector_database()
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            context = ""
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    source = results["metadatas"][0][i].get("source", "Unknown")
                    context += f"Document {i+1} (Source: {source}):\n{doc}\n\n"
            
            return context.strip()
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return ""
    
    def is_initialized(self):
        if not self.client:
            self.setup_vector_database()
        
        try:
            collections = self.client.list_collections()
            return "uitm_knowledge" in [c.name for c in collections]
        except:
            return False
    
    def get_collection_count(self):
        if not self.collection:
            self.setup_vector_database()
        
        try:
            return self.collection.count()
        except:
            return 0
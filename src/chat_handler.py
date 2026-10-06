from src.llm_client import GeminiLLM
from src.rag_retriever import RAGRetriever

class ChatHandler:
    def __init__(self):
        self.llm = GeminiLLM()
        self.rag = RAGRetriever()
        self.chat_history = []
    
    def initialize_rag(self):
        self.rag.setup_vector_database()
        
        count = self.rag.get_collection_count()
        if count == 0:
            print("Indexing documents...")
            self.rag.index_documents()
    
    def send_message(self, message):
        context = self.rag.retrieve_documents(message)
        response = self.llm.send_message(message, context)
        
        self.chat_history.append({
            "user": message,
            "assistant": response
        })
        
        return response
    
    def get_chat_history(self):
        return self.chat_history
    
    def clear_history(self):
        self.chat_history = []
        self.llm.clear_history()
    
    def get_llm(self):
        return self.llm
    
    def get_rag(self):
        return self.rag
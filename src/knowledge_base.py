import os
import PyPDF2 #untuk baca pdf (extract text dari pdf file)
import re #use regular expression untuk split text
from pathlib import Path #handles folder n file punya path

class KnowledgeBaseProcessor:
    def __init__(self, knowledge_base_path="./knowledge_base"):
        self.knowledge_base_path = Path(knowledge_base_path) #init path dulu
        self.documents = [] #init current documents list
    
    def load_documents(self):
        self.documents = []
        
        categories = {
            "research": ["research", "grant", "funding"],
            "publication": ["publication", "journal", "publish", "paper"],
            "industry": ["industry", "collaboration", "mou", "community", "ican"],
            "alumni": ["alumni", "graduat", "network"]
        }
        
        for file_path in self.knowledge_base_path.rglob("*"): #rglob search for all files in the knowledge base path
            if file_path.is_file() and file_path.suffix.lower() in [".pdf", ".txt", ".docx"]:
                content = self.extract_text_from_file(file_path)
                if content:
                    file_name = file_path.name.lower()
                    category = "general"
                    for cat, keywords in categories.items():
                        if any(keyword in file_name for keyword in keywords):
                            category = cat
                            break
                    
                    parent_dir = file_path.parent.name.lower()
                    if parent_dir in categories:
                        category = parent_dir
                    
                    self.documents.append({
                        "file_path": str(file_path),
                        "file_name": file_path.name,
                        "category": category,
                        "content": content,
                        "metadata": {
                            "source": file_path.name,
                            "category": category
                        }
                    })
        
        return self.documents
    
    def extract_text_from_file(self, file_path):
        try:
            if file_path.suffix.lower() == ".pdf":
                return self._extract_pdf_text(file_path)
            elif file_path.suffix.lower() == ".txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return None
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return None
    
    def _extract_pdf_text(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return None
    
    def chunk_documents(self, chunk_size=1000, chunk_overlap=200):
        chunks = []
        
        for doc in self.documents:
            text = doc["content"]
            if not text:
                continue
            
            paragraphs = re.split(r'\n\s*\n', text)
            
            current_chunk = ""
            for paragraph in paragraphs:
                if len(current_chunk) + len(paragraph) <= chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append({
                            "text": current_chunk.strip(),
                            "metadata": doc["metadata"]
                        })
                    current_chunk = paragraph + "\n\n"
            
            if current_chunk.strip():
                chunks.append({
                    "text": current_chunk.strip(),
                    "metadata": doc["metadata"]
                })
        
        return chunks
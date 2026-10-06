import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiLLM:
    # def __init__(self, model_name="gemini-2.5-flash"): //old version not working
    def __init__(self, model_name="gemini-3.6-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Please check your .env file")
        
        genai.configure(api_key=self.api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=self._get_system_instruction()
        )
        self.chat_session = None
    
    def _get_system_instruction(self):
        return """You are a helpful Smart Digital Assistant for lecturers at UiTM Kuala Terengganu.
        
        Your role is to assist with Research and Industry Linkages (PJI) unit information.
        
        Provide accurate information about:
        1. Research Management Unit (RMU) - Research grants, funding, policies, procedures, forms
        2. Publication Unit - Journal guidelines, publication procedures, indexing, templates
        3. Industry, Community and Alumni Network (ICAN) - Industry collaboration, community engagement, MoU, programs
        4. Alumni - Alumni services, programs, networking, benefits, engagement activities
        
        Guidelines:
        - Always provide accurate information based on retrieved context
        - If unsure, say so and suggest contacting PJI
        - Use a professional, helpful tone
        - Keep responses clear and concise
        - Do not make up information
        """
    
    def create_chat_session(self):
        self.chat_session = self.model.start_chat(history=[])
        return self.chat_session
    
    def send_message(self, message, context=None):
        if not self.chat_session:
            self.create_chat_session()
        
        if context:
            enhanced_prompt = f"""
            Based on the following institutional documents, please answer the question.
            
            Context from UiTM Kuala Terengganu documents:
            {context}
            
            Lecturer's Question: {message}
            
            Provide a clear, accurate, and helpful response based on the context above.
            If the context doesn't contain the information, say so politely.
            """
        else:
            enhanced_prompt = message
        
        response = self.chat_session.send_message(enhanced_prompt)
        return response.text
    
    def clear_history(self):
        self.chat_session = None
import streamlit as st
import os
from dotenv import load_dotenv
from src.chat_handler import ChatHandler

load_dotenv()

# Page config
st.set_page_config(
    page_title="Smart Digital Assistant - UiTM Kuala Terengganu",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #800000 0%, #C41E3A 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .chat-message-user {
        background-color: #e3f2fd;
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .chat-message-assistant {
        background-color: #f5f5f5;
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_handler" not in st.session_state:
    st.session_state.chat_handler = ChatHandler()
    st.session_state.chat_handler.initialize_rag()
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Smart Digital Assistant")
    st.markdown("Your AI-powered assistant for Research and Industry Linkages")
    st.divider()
    
    if st.button("💬 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_handler.clear_history()
        st.rerun()
    
    st.divider()
    
    st.markdown("### 📚 Knowledge Sources")
    st.markdown("""
    - 📄 Research Management (RMU)
    - 📝 Publication Unit  
    - 🤝 Industry & Community (ICAN)
    - 🎓 Alumni Services
    """)
    
    st.divider()
    
    rag_count = st.session_state.chat_handler.rag.get_collection_count()
    if rag_count > 0:
        st.success(f"✅ {rag_count} document chunks indexed")
    else:
        st.warning("⚠️ No documents indexed yet")
    
    st.divider()
    
    st.markdown("### ❓ Need Help?")
    st.markdown("Contact Research & Industry Linkages Unit (PJI)")

# Main content
st.markdown("""
    <div class="main-header">
        <h1>🎓 UiTM Kuala Terengganu</h1>
        <h3>Smart Digital Assistant</h3>
        <p>Ask me about research grants, publications, industry collaboration, alumni, and more.</p>
    </div>
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message-user">
                <b>👤 You:</b><br>{message["content"]}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message-assistant">
                <b>🤖 Smart Assistant:</b><br>{message["content"]}
            </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base and generating response..."):
            try:
                response = st.session_state.chat_handler.send_message(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})

st.markdown("""
    <div class="footer">
        <p>⚠️ Smart Assistant can make mistakes. Please verify important information.</p>
        <p>© 2025 Research & Industry Linkages Unit (PJI) | UiTM Kuala Terengganu</p>
    </div>
""", unsafe_allow_html=True)
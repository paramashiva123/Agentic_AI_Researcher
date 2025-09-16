import streamlit as st
from ai_researcher_2 import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom CSS for a modern, creative, production-grade interface
st.markdown("""
    <style>
        /* General App Styling */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
        }
        /* Header */
        .header {
            background: #0f3460;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        .header h1 {
            color: #ffffff;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
        }
        .header p {
            color: #a0a0a0;
            margin: 0.5rem 0 0;
        }
        /* Sidebar */
        .stSidebar {
            background: #0f1c36;
            border-right: 1px solid #2e2e3e;
        }
        .stButton > button {
            background: #e94560;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: #ff6b81;
            transform: translateY(-2px);
        }
        /* Chat Input */
        .stTextInput > div > div > input {
            background: #2e2e3e;
            color: #e0e0e0;
            border-radius: 8px;
            border: 1px solid #4a4a6a;
            padding: 0.8rem;
        }
        /* Chat Messages */
        .stChatMessage.user {
            background: #3a3a5a;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            animation: slideIn 0.3s ease;
        }
        .stChatMessage.assistant {
            background: #0e3460;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Markdown and Text */
        [data-testid="stMarkdownContainer"] {
            color: #e0e0e0;
        }
        /* Tooltip */
        .tooltip {
            position: relative;
            display: inline-block;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 120px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -60px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄", layout="wide")

# Header
st.markdown("""
    <div class="header">
        <h1>Research AI Agent</h1>
        <p>Explore cutting-edge research with AI-powered insights</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    theme = st.selectbox("Theme", ["Dark", "Light"], index=0)
    if theme == "Light":
        st.markdown("""
            <style>
                .stApp { background: #ffffff; color: #333333; }
                .stSidebar { background: #f0f0f0; }
                .stTextInput > div > div > input { background: #ffffff; color: #333333; border: 1px solid #cccccc; }
                .stChatMessage.user { background: #e6e6fa; }
                .stChatMessage.assistant { background: #add8e6; }
                [data-testid="stMarkdownContainer"] { color: #333333; }
            </style>
        """, unsafe_allow_html=True)
    
    if st.button("Clear Chat History", key="clear_history"):
        st.session_state.chat_history = []
        st.session_state.pdf_path = None
        st.success("Chat history cleared!")
    
    st.markdown("""
        <div class="tooltip">
            <span>ℹ️ About</span>
            <span class="tooltiptext">AI-powered research assistant using Groq API</span>
        </div>
    """, unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# Main chat container
st.subheader("Chat with the Research Agent")
chat_container = st.container()

# Display chat history
with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input and processing
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    try:
        # Log and display user input
        logger.info(f"User input: {user_input}")
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)

        # Show loading spinner
        with st.spinner("Processing your request..."):
            # Prepare input for the agent
            chat_input = {"messages": [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history}
            logger.info("Starting agent processing...")

            # Stream agent response
            full_response = ""
            with chat_container:
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    for s in graph.stream(chat_input, config, stream_mode="values"):
                        message = s["messages"][-1]
                        
                        # Handle tool calls (log only)
                        if getattr(message, "tool_calls", None):
                            for tool_call in message.tool_calls:
                                logger.info(f"Tool call: {tool_call['name']}")
                        
                        # Handle assistant response
                        if isinstance(message, AIMessage) and message.content:
                            text_content = message.content if isinstance(message.content, str) else str(message.content)
                            full_response += text_content + " "
                            response_placeholder.write(full_response)
            
            # Add final response to history
            if full_response:
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            
            # Check for PDF output
            if st.session_state.pdf_path and Path(st.session_state.pdf_path).exists():
                with open(st.session_state.pdf_path, "rb") as file:
                    st.download_button(
                        label="Download Research Paper PDF",
                        data=file,
                        file_name="research_paper.pdf",
                        mime="application/pdf"
                    )
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Error during processing: {str(e)}")

# Footer
st.markdown("""
    <hr style="border: 1px solid #2e2e3e;">
    <p style="text-align: center; color: #a0a0a0;">Powered by Groq & Streamlit | © 2025 Research AI</p>
""", unsafe_allow_html=True)
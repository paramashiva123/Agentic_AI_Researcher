import streamlit as st
from ai_researcher_2 import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage, ToolMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)  # Note: This overrides the previous basicConfig; consider removing one

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄", layout="wide")

# Title with image beside it
col1, col2 = st.columns([1, 6])
with col1:
    st.image("robot.png", width=100)  # Assume the provided image is saved as 'robot.png' in the project root; adjust path if needed
with col2:
    st.title("Research AI Agent")

# Subheader for better visuals
st.subheader("Explore Cutting-Edge Research Topics with AI Assistance")
st.markdown("---")  # Horizontal separator for cleaner layout

# Sidebar for additional info
st.sidebar.title("About This App")
st.sidebar.info(
    "This AI agent helps you discover recent arXiv papers, analyze them, "
    "identify future research directions, and even generate new papers "
    "complete with LaTeX rendering."
)
st.sidebar.markdown("Powered by LangGraph and Gemini.")
st.sidebar.image("https://x.ai/_next/image?url=%2Fimages%2Fxai-logo.png&w=256&q=75", width=150)  # Optional xAI logo for branding

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # Append and display user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare input for the agent
    chat_input = {"messages": [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history}
    logger.info("Starting agent processing...")

    # Stream agent response
    full_response = ""
    with st.chat_message("assistant"):
        response_container = st.empty()
    pdf_path = None

    for s in graph.stream(chat_input, config, stream_mode="values"):
        message = s["messages"][-1]
        
        # Handle tool calls (log only)
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                logger.info(f"Tool call: {tool_call['name']}")
        
        # Handle tool outputs (e.g., detect PDF path)
        if isinstance(message, ToolMessage):
            logger.info(f"Tool output: {message.content[:200]}...")
            # Check if this is the PDF rendering output
            if Path(message.content).suffix.lower() == ".pdf":
                pdf_path = message.content
                st.session_state.pdf_path = pdf_path
        
        # Handle and stream assistant response
        if isinstance(message, AIMessage) and message.content:
            text_content = message.content if isinstance(message.content, str) else str(message.content)
            full_response += text_content + " "
            response_container.markdown(full_response + " ▌")  # Streaming cursor effect

    # Finalize response
    if full_response:
        response_container.markdown(full_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    # Display PDF download if generated
    if pdf_path:
        with st.chat_message("assistant"):
            st.success("Research paper PDF generated successfully!")
            pdf_data = open(pdf_path, "rb").read()
            st.download_button(
                label="📥 Download Research Paper PDF",
                data=pdf_data,
                file_name="research_paper.pdf",
                mime="application/pdf",
                key="pdf_download"  # Unique key to avoid conflicts
            )
Agentic AI Researcher
 
Overview
The Agentic AI Researcher is an advanced AI-powered application designed to function as an autonomous researcher. It engages with users to explore research topics, searches for recent papers on arXiv.org, analyzes them, proposes novel research ideas, and generates a complete research paper in LaTeX, rendered as a PDF with mathematical equations. The project includes a Streamlit-based web interface for seamless interaction, making it accessible for researchers, students, or anyone interested in exploring academic topics.
This project showcases expertise in AI agent development, large language model (LLM) orchestration, tool integration, PDF processing, and web app development, making it an excellent portfolio piece for demonstrating technical and research-oriented skills to recruiters.
Features

Conversational Research Assistant: Interactively refine research topics through a chat interface.
arXiv Integration: Search and retrieve recent papers from arXiv.org using a custom tool.
PDF Analysis: Extract and analyze text from PDF papers to understand research outcomes and future directions.
Idea Generation: Propose innovative research ideas based on analyzed papers.
Paper Generation: Write a complete research paper in LaTeX, including mathematical equations, and render it as a PDF.
Streamlit Web Interface: User-friendly frontend for engaging with the AI agent.
Modular Tool Architecture: Built with LangChain tools for extensibility.
State Management: Uses LangGraph for robust workflow and memory management.

Tech Stack

Programming Language: Python 3.12
AI Frameworks:
LangChain: For building tools and agents.
LangGraph: For managing graph-based workflows.


Large Language Model: Google Generative AI (Gemini 2.5 Pro) – requires a Google API key.
PDF Processing:
PyPDF2: For reading PDF content.
Tectonic: For rendering LaTeX to PDF (must be installed separately).


Web Framework: Streamlit for the interactive frontend.
Other Libraries:
Requests: For arXiv API calls.
xml.etree.ElementTree: For parsing arXiv XML responses.
python-dotenv: For managing environment variables.


Environment: Managed via .env file for API keys.

Prerequisites
Before running the project, ensure you have:

Python 3.12 installed (specified in .python-version).
Tectonic installed for LaTeX-to-PDF rendering:
Install via package manager (e.g., brew install tectonic on macOS) or download from https://tectonic-typesetting.github.io/.


A Google API Key for Gemini LLM (obtain from https://makersuite.google.com/).

Installation

Clone the Repository:
git clone https://github.com/paramashiva123/Agentic_AI_Researcher.git
cd Agentic_AI_Researcher


Set Up a Virtual Environment:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

Note: If requirements.txt is missing, install manually:
pip install langchain langgraph langchain-google-genai streamlit pypdf2 requests python-dotenv


Configure Environment Variables:

Create a .env file in the project root.
Add your Google API key:GOOGLE_API_KEY=your_google_api_key_here




Install Tectonic:Ensure Tectonic is installed for rendering LaTeX to PDF. Follow instructions at https://tectonic-typesetting.github.io/.


Usage
Option 1: Streamlit Web App (Recommended)

Run the Streamlit app:streamlit run frontend.py


Open your browser at http://localhost:8501.
Enter a research topic (e.g., "Quantum machine learning") in the chat input.
Follow the AI's prompts to:
Explore recent arXiv papers.
Select a paper for analysis.
Choose a research idea.
Generate and download a LaTeX-rendered PDF paper.


Generated PDFs are saved in the output/ directory.

Option 2: Command-Line Interface (CLI)
For development or testing, use the CLI scripts:

Basic Version (ai_researcher.py):python ai_researcher.py


Advanced Version (ai_researcher_2.py, with LangGraph):python ai_researcher_2.py


Interact via the terminal by entering research topics (e.g., "User: Explore recent papers on neural networks").

How It Works

Agent Workflow:

Built with LangGraph, the agent manages state and tool calls using a graph-based workflow.
A system prompt defines the AI's role as an expert researcher across multiple fields.
Conditional logic determines whether to invoke tools or respond directly.


Tools:

arxiv_search: Queries arXiv.org for recent papers, returning metadata (title, authors, summary, PDF link).
read_pdf: Downloads and extracts text from PDF papers using PyPDF2.
render_latex_pdf: Converts LaTeX content to a PDF using Tectonic, saved in the output/ directory.


Frontend:

Streamlit provides a chat-like interface with session state for maintaining conversation history.
Responses are streamed in real-time for a smooth user experience.


Example Interaction:

User: "Find papers on quantum computing."
Agent: Lists recent arXiv papers with titles, authors, and PDF links.
User: "Analyze paper X."
Agent: Reads the PDF, summarizes it, and suggests new research ideas.
User: "Write a paper on idea Y."
Agent: Generates a LaTeX paper and renders it as a PDF.



Project Structure

ai_researcher.py: Basic CLI implementation of the agent.
ai_researcher_2.py: Advanced CLI implementation using LangGraph for state management.
arxiv_tool.py: Custom tool for searching and parsing arXiv papers.
read_pdf.py: Tool for extracting text from PDF URLs.
write_pdf.py: Tool for rendering LaTeX content to PDF.
frontend.py: Streamlit web app for user interaction.
.gitignore: Excludes unnecessary files (e.g., .venv, .env, output/).
.python-version: Specifies Python 3.12.
output/: Directory for generated PDFs (created automatically).

Limitations and Future Improvements

Limitations:
Dependent on arXiv.org API, which may have rate limits or downtime.
PDF extraction may struggle with complex layouts (e.g., scanned documents).
LaTeX rendering requires error-free code to avoid Tectonic failures.


Potential Improvements:
Add support for additional research databases (e.g., PubMed, IEEE).
Improve PDF parsing for better text extraction.
Integrate citation management tools for accurate referencing.
Enhance the frontend with advanced UI features (e.g., paper previews).



Contributing
Contributions are welcome to improve functionality or fix issues! To contribute:

Fork the repository.
Create a feature branch: git checkout -b feature/your-feature-name.
Commit changes: git commit -m 'Add your feature'.
Push to the branch: git push origin feature/your-feature-name.
Open a pull request on GitHub.

Please ensure code follows PEP 8 style guidelines and includes appropriate documentation.
License
This project is licensed under the MIT License. See LICENSE for details.
Contact

GitHub: paramashiva123
Email: kambalaparamashiva123@gmail.com
LinkedIn: Paramashiva Kambala

If you find this project valuable, please give it a ⭐ on GitHub! For questions or collaboration, feel free to reach out.
# 🎥 Video Compliance System (VCS)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink)](https://www.langchain.com/)
[![LangSmith](https://img.shields.io/badge/LangSmith-FF4B4B?style=for-the-badge)](https://www.langchain.com/langsmith)

An automated **Video Compliance QA system** that leverages Agentic RAG and LLMs to audit video content against complex regulatory standards and YouTube ad guidelines.

## 🚀 The Problem & Solution

**The Challenge:** Manually auditing videos for advertising claims and regulatory compliance is slow, expensive, and prone to human error. Reviewers must cross-reference video transcripts and visual text (OCR) against hundreds of pages of YouTube guidelines and legal documents.

**The Solution:** This system automates the "Compliance Officer" role. It extracts multimodal data from videos, retrieves relevant policies using semantic search, and uses GPT-4o to generate structured violation reports—reducing human oversight requirements and accelerating content approval cycles.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **API Framework** | FastAPI (Python) |
| **Orchestration** | LangGraph & LangChain |
| **Intelligence** | Azure OpenAI Service (GPT-4o) |
| **Multimodal Extraction** | Azure Video Indexer (Transcript + OCR) |
| **Vector Database** | Azure AI Search |
| **Embeddings** | Azure OpenAI Embeddings |
| **Observability** | LangSmith & Azure Application Insights |

---

## 🧠 Key Features & Implementation

### 1. Agentic Workflow (LangGraph)
Unlike linear RAG pipelines, we use **LangGraph** to orchestrate a stateful auditing workflow. This allows the system to iteratively verify claims, backtrack if information is missing, and handle complex branching logic required for different types of ad guidelines.

### 2. Multimodal RAG Pipeline
* **Video Ingestion:** Uses **Azure Video Indexer** to perform deep analysis, extracting not just what is said (Transcript) but also what is shown (OCR/Visual text).
* **Semantic Retrieval:** Relevant YouTube guidelines and policy docs are indexed in **Azure AI Search**, enabling the model to "read" the rules before judging the video.

### 3. Deterministic Violation Detection
* **Prompt Engineering:** Fine-tuned prompts to minimize hallucinations and ensure the LLM cites specific policy sections for every violation.
* **Structured Output:** Enforces **JSON Schema** generation via GPT-4o, ensuring the output is ready for downstream consumption by UI dashboards or automated flagging systems.

### 4. Enterprise-Grade Observability
* **LangSmith:** Used for tracing individual LLM calls, debugging logic loops, and evaluating model performance.
* **Latency Analysis:** Integrated with **Azure Application Insights** to monitor pipeline bottlenecks and optimize token usage.

---

## 🏗️ System Architecture & Engineering

### 1. Agentic Orchestration (LangGraph)
Unlike standard linear chains, this system utilizes **LangGraph** to manage a stateful, cyclic workflow. The agent acts as a "Digital Compliance Officer," iteratively querying policy databases and cross-referencing visual/audio evidence before reaching a final verdict.

### 2. Multimodal Data Extraction (Azure Video Indexer)
To achieve a comprehensive audit, the pipeline processes two primary streams of data:
* **Temporal Transcripts:** Speech-to-text analysis for verbal claims and disclosures.
* **OCR (Optical Character Recognition):** Extraction of "fine print," on-screen text, and visual disclaimers to ensure legal compliance.

### 3. High-Fidelity Retrieval (Azure AI Search)
Policy documents (YouTube Ad Guidelines, FTC Regulations) are vectorized using **Azure OpenAI Embeddings** and stored in **Azure AI Search**. This enables **Hybrid Semantic Retrieval**, ensuring the LLM has the exact context required to validate specific industry claims (e.g., Finance, Healthcare).

### 4. Deterministic Compliance Reasoning (GPT-4o)
The core reasoning engine is built on **Azure OpenAI GPT-4o**, utilizing:
* **JSON Schema Constraints:** Ensures outputs are strictly structured for seamless integration with downstream ERP/CMS systems.
* **Chain-of-Thought Prompting:** Forces the model to cite specific policy paragraphs as evidence for every flagged violation.

---

## 📈 Impact
* **80% Reduction** in manual auditing time.
* **Consistent Standard:** Eliminates subjective bias in human reviews.
* **Scalability:** Process thousands of ad videos simultaneously.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/video-compliance-system.git](https://github.com/your-username/video-compliance-system.git)

2. **Create a .env file following the template.env structure:**
   ```bash
    #AZURE STORAGE
    AZURE_STORAGE_CONNECTION_STRING=""
    
    #AZURE OPENAI CONFIG
    AZURE_OPENAI_API_KEY=""
    AZURE_OPENAI_ENDPOINT=""
    AZURE_OPENAI_API_VERSION=""
    AZURE_OPENAI_CHAT_DEPLOYMENT=""
    
    #ADD THE EMBEDDING MODEL CONFIG
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT=""
    
    # AZURE AI SEARCH -- KNOWLEDGE BASE CONFIG
    AZURE_SEARCH_ENDPOINT=""
    AZURE_SEARCH_API_KEY=""
    AZURE_SEARCH_INDEX_NAME=""
    
    #AZURE VIDEO INDEXER CONFIG
    AZURE_VI_NAME=""
    AZURE_VI_LOCATION=""
    AZURE_VI_ACCOUNT_ID=""
    AZURE_SUBSCRIPTION_ID=""
    AZURE_RESOURCE_GROUP=""
    
    #AZURE MONITORING - OBSERVABILITY
    APPLICATIONINSIGHTS_CONNECTION_STRING=""
    
    # LANGSMITH TRACING
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=""
    LANGCHAIN_API_KEY=""
    LANGCHAIN_PROJECT=""

3. **Deploy with Uvicorn:**
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000

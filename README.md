<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/RAG-Powered-00C853?style=for-the-badge" alt="RAG"/>
  <img src="https://img.shields.io/badge/IBM-Internship-052FAD?style=for-the-badge&logo=ibm&logoColor=white" alt="IBM"/>
</p>

<h1 align="center">📚 Document Q&A System 🤖</h1>
<h3 align="center"><em>Generative AI Powered Multi-Document Conversational Assistant</em></h3>

<p align="center">
  <strong>Upload PDFs → Extract Knowledge → Ask Questions → Get Grounded Answers</strong>
</p>

<p align="center">
  Developed for the <strong>IBM Internship Program</strong> under the <strong>Generative AI Domain</strong>
</p>

---

## 📸 Application Preview

<p align="center">
  <img src="assets/main_interface.png" alt="Document Q&A System - Main Interface" width="800"/>
</p>

<p align="center"><em>Main chat interface with document upload sidebar and AI-powered Q&A</em></p>

---

## 🌟 Overview

The **Document Q&A System** is an intelligent, interactive web application that enables users to upload PDF documents and have natural, multi-turn conversations about their content. Built on **Retrieval-Augmented Generation (RAG)** principles using **Google Gemini AI**, the system provides accurate, context-grounded answers while preventing hallucinations.

### Why This Project?

| Problem | Solution |
|---------|----------|
| Reading long PDFs is time-consuming | Upload & ask questions in natural language |
| Traditional search returns keywords, not answers | AI generates human-readable, contextual answers |
| AI models can hallucinate facts | Strict RAG grounding ensures answers come **only** from your documents |
| Single-turn Q&A loses conversation context | Multi-turn memory recalls previous questions & answers |
| Generic AI interfaces look outdated | 4 premium, customizable visual themes |

---

## 🎓 IBM Internship Context

| Detail | Description |
|--------|-------------|
| **Domain** | Generative AI |
| **Project Type** | Internship / Capstone Project |
| **Objective** | Build a robust, scalable RAG-based conversational AI system for PDF document analysis |
| **Key Skills** | LLM Integration, RAG Architecture, Prompt Engineering, Python, Streamlit |

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph User Interface
        A[👤 User] -->|Uploads PDFs| B[📂 Streamlit File Uploader]
        A -->|Asks Questions| C[💬 Chat Input]
        A -->|Selects Theme| D[🎨 Theme Selector]
    end

    subgraph Backend Processing
        B -->|PDF Files| E[📄 PyPDF Text Extractor]
        E -->|Extracted Text| F[(📦 Session Memory<br/>Document Store)]
        
        C -->|User Query| G[🔧 RAG Prompt Builder]
        F -->|Document Context| G
        H[(💬 Chat History<br/>Last 12 Messages)] -->|Conversation Context| G
    end

    subgraph AI Engine
        G -->|Augmented Prompt| I[🤖 Google Gemini API]
        I -->|Grounded Response| J[✨ Response Renderer]
    end

    subgraph Output
        J -->|Display| K[📱 Chat Interface]
        K -->|Stores| H
        D -->|Apply CSS| L[🎨 Dynamic Theme Engine]
        L -->|Styled UI| K
    end

    style A fill:#4CAF50,stroke:#2E7D32,color:#fff
    style I fill:#4285F4,stroke:#1565C0,color:#fff
    style F fill:#FF9800,stroke:#E65100,color:#fff
    style H fill:#FF9800,stroke:#E65100,color:#fff
    style L fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## ⚙️ How It Works — RAG Pipeline

The system follows a **Retrieval-Augmented Generation (RAG)** workflow to ensure all answers are grounded in the actual document content:

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant S as 🖥️ Streamlit UI
    participant P as 📄 PyPDF Parser
    participant M as 📦 Session Memory
    participant R as 🔧 RAG Engine
    participant G as 🤖 Gemini AI

    Note over U,G: Phase 1 — Document Ingestion
    U->>S: Upload PDF document(s)
    S->>P: Send PDF file buffer
    P->>P: Extract text from all pages
    P->>M: Store extracted text with filename
    M-->>S: Confirm document indexed
    S-->>U: Show "✨ Added to memory!"

    Note over U,G: Phase 2 — Question Answering (RAG)
    U->>S: Type question in chat
    S->>R: Send query + document context + chat history
    R->>R: Build augmented prompt with<br/>strict RAG system instructions
    R->>G: Send full prompt to Gemini API
    G->>G: Generate grounded response
    G-->>R: Return AI response
    R-->>S: Display in chat
    S->>M: Save to chat history
    S-->>U: Show AI answer with context
```

### RAG Prompt Construction Detail

```mermaid
graph LR
    A[📋 System Prompt<br/>RAG Constraints] --> D[📝 Full Prompt]
    B[📄 Document Context<br/>Extracted PDF Text] --> D
    C[💬 Chat History<br/>Last 12 Messages] --> D
    E[❓ User Question] --> D
    D --> F[🤖 Gemini API]
    F --> G[✅ Grounded Answer]

    style A fill:#E3F2FD,stroke:#1565C0,color:#000
    style B fill:#E8F5E9,stroke:#2E7D32,color:#000
    style C fill:#FFF3E0,stroke:#E65100,color:#000
    style E fill:#FCE4EC,stroke:#C62828,color:#000
    style F fill:#4285F4,stroke:#1565C0,color:#fff
    style G fill:#4CAF50,stroke:#2E7D32,color:#fff
```

The RAG system prompt enforces **5 strict constraints**:
1. ✅ Answer **ONLY** using facts from the Document Context
2. 🚫 **NO** external knowledge or assumptions
3. 📢 Clearly state when an answer **cannot be found**
4. 🔄 Use conversation history for **follow-up context** (pronouns, references)
5. 📐 Keep answers **factual, structured, and professional**

---

## ✨ Key Features

### Core Capabilities

| Feature | Description | Implementation |
|---------|-------------|----------------|
| 📄 **Multi-Document Memory** | Upload and index multiple PDFs simultaneously | `st.session_state.documents` dictionary |
| 🔒 **Strict RAG Grounding** | Answers based only on document content | Custom system prompt with 5 constraints |
| 💬 **Multi-Turn Chat** | Maintains conversation history for context | Last 12 messages included in prompt |
| 🎯 **Query Scope Control** | Query all documents or a specific one | Dropdown selector in sidebar |
| 🔍 **Document Inspector** | Preview extracted text from uploaded PDFs | Expandable text area |
| 🗑️ **Document Management** | Remove individual documents or clear all | Per-document delete buttons |

### Security & Configuration

| Feature | Description |
|---------|-------------|
| 🔐 **Secure API Key** | Supports `.env` file — key never exposed in UI |
| ⌨️ **Manual Key Fallback** | Password-masked input if `.env` not configured |
| 🤖 **Model Selection** | Choose between Gemini Flash, Pro, and latest models |

### UI & Design

| Feature | Description |
|---------|-------------|
| 🎨 **4 Premium Themes** | Cyber Obsidian, Emerald Mint, Arctic Teal, Warm Sunset |
| ✏️ **Google Fonts** | Plus Jakarta Sans for modern typography |
| 🌊 **Dynamic Gradients** | Header and button gradient animations |
| 💫 **Micro-Animations** | Hover effects, button transforms, toast notifications |

---

## 🎨 Theme Gallery

The application features **4 distinct, hand-crafted visual themes** that can be switched instantly:

<p align="center">
  <img src="assets/theme_showcase.png" alt="Theme Showcase - 4 Visual Themes" width="800"/>
</p>

| Theme | Style | Best For |
|-------|-------|----------|
| 🌌 **Cyber Obsidian** | Pure black + neon cyan/green accents | Dark mode enthusiasts, night usage |
| 🌿 **Emerald Mint Luxe** | Light mint green + emerald accents | Default, professional presentations |
| ❄️ **Arctic Teal & Frost** | Icy blue-white + teal gradients | Clean, corporate environments |
| 🌅 **Warm Sunset & Amber** | Warm cream + orange/amber accents | Comfortable, extended reading sessions |

---

## 📂 Document Management

<p align="center">
  <img src="assets/document_management.png" alt="Document Management Sidebar" width="400"/>
</p>

<p align="center"><em>Sidebar showing uploaded documents with word counts, delete options, and query scope selection</em></p>

---

## 🛠️ Tech Stack

```mermaid
graph LR
    subgraph Frontend
        A[Streamlit] -->|Python Web UI| B[Custom CSS Engine]
        B --> C[4 Dynamic Themes]
    end

    subgraph AI / NLP
        D[Google Gemini API] -->|LLM Inference| E[RAG Pipeline]
        E --> F[Prompt Engineering]
    end

    subgraph Document Processing
        G[PyPDF] -->|Text Extraction| H[PDF Parser]
    end

    subgraph Configuration
        I[python-dotenv] -->|Env Variables| J[API Key Security]
    end

    style A fill:#FF4B4B,stroke:#CC3333,color:#fff
    style D fill:#4285F4,stroke:#1565C0,color:#fff
    style G fill:#43A047,stroke:#2E7D32,color:#fff
    style I fill:#FFA726,stroke:#E65100,color:#fff
```

| Technology | Purpose | Why Chosen |
|-----------|---------|------------|
| **[Streamlit](https://streamlit.io/)** | Web UI Framework | Rapid Python web app prototyping with built-in chat components |
| **[Google Gemini API](https://ai.google.dev/)** | LLM Engine | State-of-the-art generative AI with excellent context handling |
| **[PyPDF](https://pypdf.readthedocs.io/)** | PDF Processing | Lightweight, pure-Python PDF text extraction |
| **[python-dotenv](https://pypi.org/project/python-dotenv/)** | Environment Config | Secure API key management via `.env` files |
| **Python 3.9+** | Language | Modern Python features with type hints |

---

## 🚀 Quick Start Guide

### Prerequisites

- ✅ **Python 3.9+** installed ([Download](https://www.python.org/downloads/))
- ✅ **Google Gemini API Key** ([Get one free from Google AI Studio](https://aistudio.google.com/))
- ✅ **pip** package manager (comes with Python)

### Step-by-Step Setup

```mermaid
graph LR
    A[1️⃣ Clone Repo] --> B[2️⃣ Install Dependencies]
    B --> C[3️⃣ Configure API Key]
    C --> D[4️⃣ Launch App]
    D --> E[5️⃣ Upload & Chat!]

    style A fill:#E3F2FD,stroke:#1565C0,color:#000
    style B fill:#E8F5E9,stroke:#2E7D32,color:#000
    style C fill:#FFF3E0,stroke:#E65100,color:#000
    style D fill:#F3E5F5,stroke:#6A1B9A,color:#000
    style E fill:#E8F5E9,stroke:#2E7D32,color:#000
```

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Krati-orbit/Document-Q-A-system-.git
cd Document-Q-A-system-
```

#### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | Latest | Web UI framework |
| `pypdf` | Latest | PDF text extraction |
| `google-generativeai` | Latest | Gemini API client |
| `python-dotenv` | Latest | Environment variable loader |

#### 3️⃣ Configure API Key

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

> **💡 Tip:** You can also enter your API key directly in the app sidebar if you prefer not to use a `.env` file. The input field is password-masked for security.

#### 4️⃣ Launch the Application
```bash
streamlit run app.py
```

#### 5️⃣ Open & Use
Navigate to `http://localhost:8501` in your browser, then:
1. Upload one or more PDF documents via the sidebar
2. Wait for text extraction to complete
3. Type your question in the chat input
4. Get AI-powered, document-grounded answers!

---

## 📖 Usage Guide

### Workflow Overview

```mermaid
flowchart TD
    START([🚀 Launch App]) --> CONFIG{API Key<br/>Configured?}
    
    CONFIG -->|Yes, from .env| SECURE[🔒 Key Loaded Securely]
    CONFIG -->|No| MANUAL[⌨️ Enter Key in Sidebar]
    
    SECURE --> UPLOAD
    MANUAL --> UPLOAD
    
    UPLOAD[📄 Upload PDF Documents] --> EXTRACT[📝 Auto-Extract Text]
    EXTRACT --> MEMORY[📦 Store in Session Memory]
    
    MEMORY --> SCOPE{Select Query<br/>Scope}
    SCOPE -->|All Documents| COMBINED[📚 Combined Context]
    SCOPE -->|Single Document| SINGLE[📄 Single File Context]
    
    COMBINED --> ASK
    SINGLE --> ASK
    
    ASK[❓ Ask a Question] --> RAG[🔧 RAG Prompt Builder]
    RAG --> GEMINI[🤖 Gemini AI Processing]
    GEMINI --> ANSWER[✅ Grounded Answer Displayed]
    ANSWER --> HISTORY[💬 Saved to Chat History]
    
    HISTORY --> MORE{More<br/>Questions?}
    MORE -->|Yes| ASK
    MORE -->|No| END([✨ Done!])
    
    style START fill:#4CAF50,stroke:#2E7D32,color:#fff
    style GEMINI fill:#4285F4,stroke:#1565C0,color:#fff
    style ANSWER fill:#43A047,stroke:#2E7D32,color:#fff
    style END fill:#4CAF50,stroke:#2E7D32,color:#fff
```

### Example Interactions

| You Ask... | AI Responds With... |
|------------|-------------------|
| *"Summarize the key findings"* | Structured summary extracted from document content |
| *"What does section 3 say about revenue?"* | Specific information from that section |
| *"Explain that in simpler terms"* | Simplified version using conversation context |
| *"Compare this with what was mentioned earlier"* | Cross-reference using chat history + document content |
| *"What is the capital of France?"* | *"I cannot find the answer to this question in the provided document(s)."* (RAG grounding!) |

---

## 📁 Repository Structure

```
📦 Document-Q-A-system-
├── 📂 .streamlit/
│   └── config.toml              # Streamlit UI & Server configuration
├── 📂 assets/
│   ├── main_interface.png       # App screenshot for README
│   ├── theme_showcase.png       # Theme gallery image
│   └── document_management.png  # Sidebar screenshot
├── 📄 app.py                    # Main application (675 lines)
│   ├── THEMES dict              # 4 complete theme configurations
│   ├── apply_custom_theme()     # Dynamic CSS injection engine
│   ├── extract_text_from_pdf()  # PyPDF text extraction
│   ├── generate_rag_response()  # RAG prompt builder + Gemini API call
│   └── main()                   # Streamlit UI rendering & logic
├── 📄 requirements.txt          # Python dependencies (4 packages)
├── 📄 .env                      # API Key storage (git-ignored)
├── 📄 .gitignore                # Git ignore rules
└── 📄 README.md                 # This documentation
```

### Code Architecture Breakdown

```mermaid
graph TD
    subgraph "app.py (675 lines)"
        A["THEMES Dictionary<br/>(Lines 29-114)<br/>4 complete theme configs"] --> B["apply_custom_theme()<br/>(Lines 117-348)<br/>Dynamic CSS injection"]
        C["extract_text_from_pdf()<br/>(Lines 359-397)<br/>PyPDF text extraction"] --> E
        D["generate_rag_response()<br/>(Lines 400-472)<br/>RAG prompt + Gemini call"] --> E
        E["main()<br/>(Lines 479-674)<br/>Streamlit UI & logic"]
    end

    style A fill:#E1BEE7,stroke:#6A1B9A,color:#000
    style B fill:#E1BEE7,stroke:#6A1B9A,color:#000
    style C fill:#C8E6C9,stroke:#2E7D32,color:#000
    style D fill:#BBDEFB,stroke:#1565C0,color:#000
    style E fill:#FFE0B2,stroke:#E65100,color:#000
```

---

## 🔐 Security Design

```mermaid
graph TD
    A[API Key Required] --> B{Check .env File}
    B -->|Found| C[✅ Load Securely<br/>Key never shown in UI]
    B -->|Not Found| D[⚠️ Show Password Input]
    D --> E[User enters key]
    E --> F[🔒 Stored in session_state<br/>Password-masked input]
    C --> G[🤖 Configure Gemini API]
    F --> G

    H[.gitignore] -->|Excludes| I[.env file]
    I -->|Never committed to| J[Git Repository]

    style C fill:#4CAF50,stroke:#2E7D32,color:#fff
    style F fill:#FFA726,stroke:#E65100,color:#fff
    style H fill:#F44336,stroke:#C62828,color:#fff
```

- 🔒 API keys loaded from `.env` are **never displayed** in the UI
- 🔐 Manual key input uses **password-masked** fields
- 📁 `.env` is in `.gitignore` — **never committed** to version control
- 🧠 Keys are stored only in **Streamlit session state** (ephemeral, in-memory)

---

## 🔮 Future Enhancements

| Enhancement | Description | Priority |
|-------------|-------------|----------|
| 📊 **Analytics Dashboard** | Document statistics, word clouds, topic modeling | Medium |
| 🔍 **Semantic Search** | Vector embeddings for better retrieval accuracy | High |
| 📎 **Multi-Format Support** | DOCX, TXT, CSV file support alongside PDF | Medium |
| ☁️ **Cloud Deployment** | Deploy on Streamlit Cloud or Google Cloud Run | High |
| 🧪 **Unit Tests** | Comprehensive test suite for all functions | Medium |
| 📱 **Mobile Optimization** | Responsive design for mobile devices | Low |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project was developed as part of the **IBM Generative AI Internship Program**.

---

## 👤 Author

<table>
  <tr>
    <td><strong>Developer</strong></td>
    <td>Krati</td>
  </tr>
  <tr>
    <td><strong>Program</strong></td>
    <td>IBM Generative AI Internship</td>
  </tr>
  <tr>
    <td><strong>Repository</strong></td>
    <td><a href="https://github.com/Krati-orbit/Document-Q-A-system-">GitHub</a></td>
  </tr>
</table>

---

<p align="center">
  <strong>⭐ If you found this project useful, please consider giving it a star! ⭐</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge" alt="Made with Love"/>
  <img src="https://img.shields.io/badge/Powered%20by-Gemini%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Powered by Gemini"/>
</p>

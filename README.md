# Document Q&A System 📚🤖
*(Generative AI Powered Multi-Document Assistant)*

> Developed for the **IBM Internship Program** under the **Generative AI Domain**.

---

## 🌟 Overview
The **Document Q&A System** is an intelligent, interactive web application built to analyze, process, and answer user queries based on uploaded PDF documents. Utilizing **Google Gemini AI (LLM)** and Retrieval-Augmented Generation (RAG) principles, the application provides grounded, context-aware answers with multi-turn conversational memory while ensuring API key security and offering dynamic, customizable UI themes.

---

## 🎓 IBM Internship Context
* **Domain:** Generative AI
* **Project Type:** Internship / Capstone Project
* **Objective:** Build a robust, scalable RAG-based conversational AI system that enables users to upload PDF documents, extract intelligent insights, and hold multi-turn Q&A sessions.

---

## ✨ Key Features
- **Multi-Document Session Memory:** Upload and index multiple PDF files simultaneously.
- **Strict RAG Grounding:** Answers are generated based directly on document content with hallucination safeguards.
- **Conversational Chat Interface:** Maintains multi-turn conversation history for seamless context recall.
- **Dynamic Multi-Theme Engine:** Switch between custom themes (*Cyber Obsidian*, *Emerald Mint Luxe*, *Arctic Teal & Frost*, and *Warm Sunset*).
- **Secure API Key Management:** Supports environment variables via `.env` file to prevent API key exposure.
- **Fast PDF Processing:** Efficient extraction and parsing powered by `pypdf`.

---

## 🛠️ Tech Stack
- **Frontend / Framework:** Streamlit (Python Web UI)
- **Generative AI Model:** Google Gemini API (`google-generativeai`)
- **PDF Extraction:** `pypdf`
- **Environment Management:** `python-dotenv`
- **Language:** Python 3.9+

---

## ⚙️ How It Works
1. **Document Ingestion:** Upload one or more PDF files through the sidebar interface.
2. **Text Extraction:** `pypdf` parses and extracts textual content from all pages across the uploaded PDFs.
3. **Prompt Construction (RAG):** User queries are enriched with extracted document context and recent conversational memory.
4. **LLM Inference:** The augmented prompt is processed by Google's Gemini API to produce accurate, context-grounded responses.
5. **Interactive UI:** Responses are rendered dynamically in a sleek, customizable chat interface.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ installed on your machine.
- A Google Gemini API Key (Obtain one from [Google AI Studio](https://aistudio.google.com/)).

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/Krati-orbit/Document-Q-A-system-.git
cd Document-Q-A-system-
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Launch Application
Run the Streamlit application:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📁 Repository Structure
```
├── .streamlit/
│   └── config.toml          # Streamlit UI & Server config
├── app.py                  # Main application script & UI engine
├── requirements.txt        # Python dependencies
├── .env                    # API Key storage (ignored in git)
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## 👤 Author
Developed for the **IBM Generative AI Internship**.

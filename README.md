# 🤖 ExcelBot Pro

**A RAG-powered support chatbot that reads from Excel files and provides intelligent answers using DeepSeek API.**

---

## 👨‍💻 Creator
**Amir Askari (امیر عسکری)**  
© 2026 Amir Askari. All Rights Reserved.

---

## 📌 Table of Contents
1. [What is ExcelBot Pro?](#-what-is-excelbot-pro)
2. [Features](#-features)
3. [How It Works](#%EF%B8%8F-how-it-works)
4. [Installation & Setup](#-installation--setup)
5. [Deploy on a Real Website](#-deploy-on-a-real-website)
6. [API Endpoints](#-api-endpoints)
7. [Future Development](#-future-development--extensibility)
8. [License & Copyright](#-license--copyright)

---

## 🧠 What is ExcelBot Pro?

**ExcelBot Pro** is an intelligent, RAG-powered (Retrieval-Augmented Generation) support chatbot that reads data directly from Excel files and answers user questions based on that data. It combines:

- **FAISS** (Facebook AI Similarity Search) for fast vector-based retrieval
- **Sentence-Transformers** for generating text embeddings
- **DeepSeek API** (or OpenAI compatible) for natural language understanding
- **FastAPI** for the backend server
- A **lightweight JavaScript widget** for easy integration into any website

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Excel-based Knowledge Base** | Simply add your Q&A pairs to an Excel file |
| **Semantic Search** | Uses AI embeddings to find the most relevant answers |
| **Conversational AI** | Generates natural, context-aware responses |
| **Real-time Chat Widget** | A floating chat button for any website |
| **Fully Offline Capable** | Works without any API key (simulation mode) |
| **Zero Maintenance** | Update Excel file → system auto-reloads |



## ⚙️ How It Works
User Query → Widget → FastAPI Server → FAISS Vector Search → DeepSeek → Response
↓
Excel File (Knowledge Base)

1. **User asks a question** through the chat widget.
2. **Backend converts** the question into a numerical vector (embedding).
3. **FAISS searches** for the most similar questions/answers from the Excel file.
4. **DeepSeek API** generates a natural, context-aware response.
5. **Answer is sent back** to the user in real-time.

---

## 🛠️ Installation & Setup

### Step 1: Clone the Repository

bash
git clone https://github.com/YourUsername/excelbot-pro.git
cd excelbot-pro/backend

Step 2: Install Dependencies

pip install -r requirements.txt

Step 3: Set Up Environment Variables
Create a .env file inside the backend/ folder:
# For DeepSeek (recommended - FREE)
OPENAI_API_KEY=your_deepseek_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat

# OR for OpenAI (paid)
# OPENAI_API_KEY=sk-...
# MODEL_NAME=gpt-3.5-turbo

Step 4: Prepare Your Excel File
Place your Excel file at backend/data/data.xlsx with this structure:

سوال (Question)	پاسخ (Answer)	دسته‌بندی (Category - optional)
What is the return policy?	You can return items within 7 days	Support
How do I place an order?	Go to the shop section	Guide

Step 5: Run the Server

uvicorn app.main:app --reload
The server will start at: http://127.0.0.1:8000


🌐 Deploy on a Real Website
Option 1: Use the Widget (Quick & Easy)
Copy the chat widget code from frontend/widget.html and add it to your website before the closing </body> tag:

html
<!-- Chat Widget -->
<div id="chat-widget"></div>
<script>
    const API_URL = 'https://your-domain.com/api/chat';  // ← Change to your server URL
    // ... rest of widget code
</script>
Option 2: Deploy on a VPS (Professional)
Set up a Linux VPS (Ubuntu 22.04 recommended)

Install Python, Git, and Nginx

Clone your repository and set up the environment

Run with Gunicorn for production:

bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
Set up Nginx as a reverse proxy:

nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
Option 3: Deploy with Docker (Easiest)
Create a Dockerfile in the project root:

dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY backend/ /app/
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Build and run:

bash
docker build -t excelbot-pro .
docker run -p 8000:8000 excelbot-pro
📁 Project Structure
text
excelbot-pro/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── models/              # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # RAG, Embedding, LLM services
│   │   └── utils/               # Excel loader
│   ├── data/
│   │   └── data.xlsx            # Your knowledge base
│   ├── chroma_db/               # Vector database (auto-generated)
│   ├── .env                     # Environment variables
│   └── requirements.txt
├── frontend/
│   └── widget.html              # Chat widget
└── README.md
📊 API Endpoints
Endpoint	Method	Description
/api/chat	POST	Send a question and get an AI response
/api/health	GET	Check server status
/api/reload	POST	Reload data from Excel
🚀 Future Development & Extensibility
This project is 100% extensible and open for contributions, with the condition that Amir Askari remains the original creator and lead developer.

🧩 Extensions You Can Add
Extension	Description
Multi-language support	Add more languages beyond Persian/English
User authentication	Add login system for personalized support
Analytics dashboard	Track user queries and satisfaction
Slack/Discord integration	Connect to team communication platforms
Custom fine-tuning	Train the model on your specific domain
Voice support	Add speech-to-text and text-to-speech
WhatsApp/Telegram bot	Deploy as a messaging bot
Knowledge graph	Build relationships between data points
📦 New Data Sources
You can easily extend the system to read from:

Google Sheets

SQL Databases (PostgreSQL, MySQL)

MongoDB

JSON/CSV files

PDF documents

Web scraping pipelines

🤖 Model Enhancements
Switch to GPT-4 or Claude when needed

Use multilingual embedding models

Implement hybrid search (BM25 + Vector)

Add Reranking models for better precision

🔒 License & Copyright
© 2026 Amir Askari (امیر عسکری). All Rights Reserved.

This project and its source code are the exclusive intellectual property of Amir Askari. You may:

✅ Use this software for personal or commercial purposes

✅ Modify the code for your own use

✅ Distribute the original or modified versions, provided that:

Credit is clearly given to Amir Askari as the original creator

The copyright notice remains visible in all copies or substantial portions

No claim is made that you are the original author

Commercial use: If you are using this software for a commercial product or service, you must include the following attribution:

"This product includes software developed by Amir Askari (https://github.com/YourUsername/excelbot-pro)"

📞 Contact & Support
Creator: Amir Askari 

For support, feature requests, or commercial licensing:

Email: your-email@example.com

GitHub: github.com/YourUsername

Website: your-website.com

🙏 Acknowledgments
DeepSeek for providing free, high-quality AI APIs

FAISS for fast vector search

Sentence-Transformers for embedding models

FastAPI for the excellent web framework

Built with ❤️ by Amir Askari 🇮🇷

© 2026 Amir Askari - All Rights Reserved

# 🎤 AI Interview Coach

An AI-powered mock interview platform that simulates real technical interviews with voice interaction, automated evaluation, and personalized feedback.

## 🚀 Features

* AI-powered technical interview simulation
* Voice-based answering using Speech Recognition
* Text-to-Speech question delivery
* Automated answer evaluation using Gemini API
* Dynamic interview flow using LangGraph
* Session-based interview memory
* Performance report generation
* Role-based interview questions

## 🛠️ Tech Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* FastAPI
* Python
* LangGraph
* Gemini API

## 📂 Project Structure

```bash
AI_voice_Agent/
│
├── frontend/
│   ├── app/
│   ├── public/
│   └── components/
│
├── agent.py
├── graph.py
├── memory.py
├── state.py
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Technical-Prachi/Langgraph-Interview-Assistant.git
cd AI_voice_Agent
```

### Backend Setup

```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run Backend:

```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000
```

## 🎯 Supported Roles

* Python Developer
* Backend Developer
* Frontend Developer

## 🔄 Interview Workflow

Start Interview → Ask Question → Capture Voice Answer → Evaluate Answer → Generate Feedback → Next Question → Final Report

## ⚠️ Challenges Faced

* Gemini API rate limits (429 RESOURCE_EXHAUSTED)
* Gemini service unavailability during peak load (503 UNAVAILABLE)
* Managing state transitions using LangGraph
* Integrating speech recognition with interview flow
* Handling session persistence and evaluation latency

## 📈 Future Improvements

* AI-generated questions instead of static question bank
* More technical roles
* Adaptive difficulty levels
* Detailed skill-wise analytics
* Database integration
* Authentication and user profiles

## 👨‍💻 Author

Built as an AI Engineering project focused on Agentic AI workflows, LangGraph orchestration, and voice-based interview simulation.

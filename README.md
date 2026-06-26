# MediAssist — Healthcare Chatbot
**OptimusAutomate AI Internship — Task 2**

A domain-specific healthcare assistant chatbot with intent recognition and multi-turn conversation.

## Tech Stack
- Python, Streamlit, Groq API (LLaMA 3.3 70B)

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Groq API key in config.py

# 3. Run
streamlit run app.py
```

## Features
- Intent recognition (symptoms, medication, mental health, emergency, first aid)
- Emergency detection with immediate hardcoded safety response
- Multi-turn conversation with full history context
- Chat history sidebar (ChatGPT-style)
- Healthcare-only domain restriction

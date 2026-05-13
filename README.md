# CodeMind AI

An AI-powered coding assistant built with Streamlit and Groq API — specialized for Python, SQL, debugging, and coding interview preparation.

---

## Live Demo

https://codemind-ai-5vulumiu7uskzdjzogazrq.streamlit.app/
---

## Features

- ChatGPT-style chat interface
- Python programming help
- SQL query solving
- Coding interview preparation
- Code debugging support
- Concept explanations
- Powered by Llama 3.3 70B via Groq
- Professional dark theme
- Download chat history (.txt / .json)
- Multiple AI model selection

---

## Run Locally

### Clone the Repository

```bash
git clone https://github.com/Meghana-22-11/codemind-ai.git
cd codemind-ai
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Add API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_api_key_here
```

Get your free API key from:

 https://console.groq.com

---

### Run the App

```bash
streamlit run app.py
```

---

## Deploy on Streamlit Cloud

1. Push project to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Add your API key in:

```text
Settings → Secrets
```

Add:

```toml
GROQ_API_KEY="gsk_your_key_here"
```

5. Click Deploy 

---

## Project Structure

```bash
codemind-ai/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│── .env
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | Frontend UI |
| Groq API | AI Responses |
| Llama 3.3 70B | Language Model |
| Python | Backend |

---

## Requirements

- Python 3.10+
- Streamlit
- Groq
- python-dotenv

---

## Security

- API keys are stored locally using `.env`
- `.env` is excluded using `.gitignore`
- Streamlit Cloud stores secrets securely

---

## Built By

**Meghana Talapaneni**

GitHub:  
https://github.com/Meghana-22-11

---

## Support

If you found this project useful, consider giving it a ⭐ on GitHub!

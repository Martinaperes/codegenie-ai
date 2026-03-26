# CodeGenie AI 🚀
License: MIT
Python 3.9+
Flask

AI-Powered Coding Assistant - Generate code from prompts, explain complex code, debug errors. Built with Python/Flask + React + OpenAI/Groq.

✨ Features
🎯 Code Generation - "Write a REST API in FastAPI" → Complete working code
💡 Code Explanation - Paste code → Plain English breakdown
🐛 Debug Assistant - Error messages → Root cause + fixes
⚡ Fast & Private - Self-hosted, supports free Groq API
🎨 Modern UI - Responsive TailwindCSS design
🎯 Quick Demo

Prompt: "Create a Python function to validate emails"

Generated:
```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Test
print(validate_email("test@example.com"))  # True
```

## 📋 Table of Contents

- [System Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Minimal Working Example](#example)
- [AI Prompts Used](#ai-prompts)
- [Common Issues](#issues)
- [References](#references)

## 🤔 Why CodeGenie AI?

**Technology**: Python + Flask + Generative AI APIs  
**Why**: Lightweight, production-ready, real-world dev tool  
**Goal**: Your personal GitHub Copilot - self-hosted & customizable

## <a name="requirements"></a>🛠️ System Requirements
| Category | Requirements |
|---|---|
| OS | Linux/macOS/Windows 10+ |
| Python | 3.9+ |
| Node.js | 18+ |
| Editor | VS Code |
| Memory | 4GB+ RAM |

<a name="installation"></a>🚀 Installation & Setup
1. Clone & Environment
```bash
git clone https://github.com/yourusername/codegenie-ai.git
cd codegenie-ai
```

2. Python Backend
```bash
# Create virtual environment
python -m venv venv

# Activate (choose your OS)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. Frontend
```bash
cd frontend
npm install
cd ..
```

4. Configuration
```bash
cp .env.example .env
```
Edit .env:

```env
# Get free keys from:
# OpenAI: https://platform.openai.com/api-keys
# Groq (FREE): https://console.groq.com/keys
OPENAI_API_KEY=sk-your-openai-key-here
GROQ_API_KEY=gsk-your-groq-key-here
```

<a name="quick-start"></a>⚡ Quick Start (One Command)
```bash
# Clone, setup, and run (Mac/Linux)
bash <(curl -s https://raw.githubusercontent.com/yourusername/codegenie-ai/main/setup.sh)

# Or manual:
git clone https://github.com/yourusername/codegenie-ai.git && cd codegenie-ai && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && echo "OPENAI_API_KEY=your_key" >> .env && flask run & cd frontend && npm install && npm run dev
```
Live at:

Frontend: http://localhost:3000
Backend API: http://localhost:5000

<a name="example"></a>💻 Minimal Working Example
Backend API (app.py)
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for React
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    prompt = request.json.get('prompt', '')
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Generate complete working code: {prompt}"}]
    )
    
    return jsonify({"code": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
```

Test API
```bash
curl -X POST http://localhost:5000/api/generate-code \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Python function to reverse string"}'
```

<a name="ai-prompts"></a>🧠 AI Prompt Journal
| Prompt | Helpfulness | Key Learning |
|---|---|---|
| 1 | "Flask API + OpenAI code generator" | ⭐⭐⭐⭐⭐ | Perfect CORS + error handling |
| 2 | "React Tailwind code generator UI" | ⭐⭐⭐⭐⭐ | Modern component structure |
| 3 | "Fix CORS between Flask/React" | ⭐⭐⭐⭐⭐ | flask-cors = instant fix |

Pro Tip: Always specify "complete working code" in prompts!

<a name="issues"></a>🐛 Common Issues & Fixes
| ❌ Problem | ✅ Solution |
|---|---|
| CORS Error | `pip install flask-cors`<br>`CORS(app)` |
| No module 'openai' | `pip install -r requirements.txt` |
| Port 5000 busy | `flask run --port 5001` |
| Rate limited | Use Groq API (FREE) |
| Frontend 404 | `npm run dev` in `/frontend` |

<a name="references"></a>📚 References
Official Docs
- [Flask](https://flask.palletsprojects.com/)
- [OpenAI Python](https://github.com/openai/openai-python)
- [React](https://react.dev/)
- [TailwindCSS](https://tailwindcss.com/)

Videos
- [Flask + React Tutorial](https://www.youtube.com/results?search_query=flask+react+tutorial)
- [OpenAI API Crash Course](https://www.youtube.com/results?search_query=openai+api+crash+course)

Free AI APIs
- [Groq (200k tokens/min FREE)](https://groq.com/)
- [OpenAI Playground](https://platform.openai.com/playground)

🛠️ Project Structure
```text
codegenie-ai/
├── app.py                 # Flask backend
├── requirements.txt       # Python deps
├── .env.example          # API keys template
├── frontend/             # React + Vite + Tailwind
│   ├── src/
│   │   └── components/
│   └── package.json
└── README.md
```

🤝 Contributing
1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open Pull Request

📄 License
MIT License - see LICENSE file.



<p align="center"> <img src="https://img.shields.io/badge/Deploy-Heroku-brightgreen.svg" alt="Deploy"> <img src="https://img.shields.io/badge/Deploy-Vercel-blue.svg" alt="Deploy"> <img src="https://img.shields.io/badge/Deploy-Railway-orange.svg" alt="Deploy"> </p>

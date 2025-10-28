# Research Assistant 🔍

A powerful, open-source AI research assistant with a Claude/Gemini-inspired interface. Built with FastAPI, Next.js, and powered by open-source LLMs (Ollama or OpenRouter).

![Demo](https://img.shields.io/badge/Status-Ready-green)

## ✨ Features

- **🎨 Multiple Conversation Styles**: Choose from different response styles (Balanced, Concise, Explanatory, Formal, Creative, Research)
- **🔍 Deep Research Mode**: Multi-step web search with automatic follow-up questions and comprehensive synthesis
- **🌐 Web Search Integration**: Powered by Tavily API for current information
- **💬 Streaming Responses**: Real-time streaming for smooth user experience
- **🔓 Open Source LLMs**: Use local models via Ollama or cloud models via OpenRouter
- **🎯 Claude-Inspired UI**: Clean, modern interface similar to Claude and Gemini
- **⚡ Fast & Responsive**: Built with Next.js and FastAPI for optimal performance

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Next.js UI    │ ◄─────► │  FastAPI Server  │ ◄─────► │   Ollama    │
│  (Port 3000)    │         │   (Port 8000)    │         │ (Local LLM) │
└─────────────────┘         └──────────────────┘         └─────────────┘
                                     │
                                     │
                            ┌────────┴────────┐
                            │                 │
                       ┌────▼────┐      ┌────▼────────┐
                       │ Tavily  │      │ OpenRouter  │
                       │   API   │      │ (Optional)  │
                       └─────────┘      └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.ai) (for local LLM) OR [OpenRouter API Key](https://openrouter.ai) (for cloud models)
- [Tavily API Key](https://tavily.com) (for web search)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd research-assistant
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

#### Configure `.env`:

```env
# Choose LLM provider
LLM_PROVIDER=ollama  # or "openrouter"

# For Ollama (recommended for local/privacy)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b  # or any model you have

# For OpenRouter (access to many open-source models)
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=mistralai/mistral-7b-instruct

# Tavily API (required for web search)
TAVILY_API_KEY=your_tavily_api_key_here
```

#### If using Ollama:

```bash
# Install Ollama: https://ollama.ai

# Pull a model
ollama pull llama3.1:8b

# Start Ollama server
ollama serve
```

#### Start the backend:

```bash
python main.py
# Server runs on http://localhost:8000
```

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Default API_URL is http://localhost:8000

# Start development server
npm run dev
# UI runs on http://localhost:3000
```

### 4. Open Your Browser

Navigate to **http://localhost:3000** and start chatting!

## 🎯 Usage

### Basic Chat

1. Type your question in the input box
2. Select a conversation style (Balanced, Concise, etc.)
3. Press Enter or click Send

### Deep Research Mode

1. Toggle "Deep Research" in the header
2. Ask a research question
3. The assistant will:
   - Perform initial web search
   - Generate follow-up questions
   - Conduct additional searches
   - Synthesize comprehensive answer with sources

### Conversation Styles

- **Balanced**: General-purpose responses
- **Concise**: Brief, direct answers
- **Explanatory**: Detailed with examples
- **Formal**: Professional, academic tone
- **Creative**: Engaging and imaginative
- **Research**: Evidence-based with citations

## 🔧 Configuration

### Supported LLM Providers

#### Ollama (Local)
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

**Recommended models:**
- `llama3.1:8b` - Good balance of quality and speed
- `mistral:7b` - Fast and efficient
- `mixtral:8x7b` - High quality, slower
- `qwen2.5:14b` - Excellent for research

#### OpenRouter (Cloud)
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
```

**Available models:** See [OpenRouter docs](https://openrouter.ai/docs#models)

### Customizing Conversation Styles

Edit `backend/styles.py` to add or modify styles:

```python
"custom": StyleConfig(
    name="custom",
    display_name="Custom Style",
    system_prompt="Your custom system prompt here...",
    description="Description of your style"
)
```

## 📁 Project Structure

```
research-assistant/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   ├── styles.py            # Conversation styles
│   ├── llm_service.py       # LLM integration
│   ├── search_service.py    # Tavily search
│   ├── research_service.py  # Deep research logic
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main chat interface
│   │   ├── layout.tsx       # App layout
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── ChatMessage.tsx
│   │   ├── ChatInput.tsx
│   │   ├── StyleSelector.tsx
│   │   └── DeepResearchToggle.tsx
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   └── types.ts         # TypeScript types
│   └── package.json
│
└── README.md
```

## 🛠️ Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Model Not Found

```bash
# List available models
ollama list

# Pull required model
ollama pull llama3.1:8b
```

### Port Already in Use

```bash
# Backend (change port in .env)
PORT=8001 python main.py

# Frontend (Next.js auto-increments)
npm run dev -- -p 3001
```

### CORS Issues

If you're running frontend on a different port, update the CORS settings in `backend/main.py`:

```python
allow_origins=["http://localhost:3000", "http://localhost:3001"]
```

## 🔐 API Keys

### Tavily API
1. Sign up at https://tavily.com
2. Get your API key from the dashboard
3. Add to `.env`: `TAVILY_API_KEY=tvly-xxxxx`

### OpenRouter (Optional)
1. Sign up at https://openrouter.ai
2. Get your API key
3. Add to `.env`: `OPENROUTER_API_KEY=sk-or-xxxxx`

## 📝 License

MIT License - feel free to use this project for any purpose.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 🙏 Acknowledgments

- Inspired by Claude and Gemini interfaces
- Powered by open-source LLMs
- Built with FastAPI and Next.js
- Search powered by Tavily

## 📮 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub

---

**Built with ❤️ for the open-source community**

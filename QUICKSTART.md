# Quick Start Guide

Get your Research Assistant running in 5 minutes!

## Option 1: Using the Startup Script (Easiest)

```bash
# 1. Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull a model
ollama pull llama3.1:8b

# 3. Start Ollama
ollama serve

# 4. Get Tavily API key (free tier available)
# Sign up at https://tavily.com

# 5. Configure backend
cd backend
cp .env.example .env
# Edit .env and add your TAVILY_API_KEY

# 6. Run the startup script
cd ..
./start.sh
```

That's it! Visit http://localhost:3000

## Option 2: Manual Setup

### Terminal 1 - Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python main.py
```

### Terminal 2 - Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

### Terminal 3 - Ollama (if using local LLM)

```bash
ollama serve
```

## Option 3: Docker

```bash
# Copy .env files
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Start services
docker-compose up
```

## ⚙️ Minimum Configuration

Edit `backend/.env`:

```env
# Required
TAVILY_API_KEY=your_tavily_key_here

# Optional (defaults work)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## 🎯 First Steps

1. Open http://localhost:3000
2. Try a basic question: "What is quantum computing?"
3. Toggle "Deep Research" and ask: "What are the latest developments in AI?"
4. Try different styles from the dropdown

## 🔍 Testing Deep Research

Example questions that work well with deep research:
- "What are the latest developments in renewable energy?"
- "Compare the top 5 programming languages in 2024"
- "What is the current state of quantum computing?"
- "Explain the recent advances in fusion energy"

## ⚠️ Troubleshooting

**Backend won't start?**
- Check if port 8000 is free: `lsof -i :8000`
- Verify Ollama is running: `curl http://localhost:11434/api/tags`

**Frontend won't start?**
- Check if port 3000 is free: `lsof -i :3000`
- Clear cache: `cd frontend && rm -rf .next && npm run dev`

**No search results?**
- Verify your Tavily API key is correct
- Check you have internet connection
- Try with deep research disabled first

**Ollama errors?**
- Verify model is pulled: `ollama list`
- Try pulling again: `ollama pull llama3.1:8b`
- Restart Ollama: `killall ollama && ollama serve`

## 📚 Next Steps

- Read the full [README.md](README.md)
- Customize conversation styles in `backend/styles.py`
- Explore API docs at http://localhost:8000/docs
- Try different LLM models with Ollama

## 🚀 Alternative LLM Options

### Use OpenRouter instead of Ollama

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-xxxxx
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
```

### Try different Ollama models

```bash
# Fast and efficient
ollama pull mistral:7b

# High quality
ollama pull mixtral:8x7b

# Great for coding
ollama pull codellama:13b

# Excellent reasoning
ollama pull qwen2.5:14b
```

Update `backend/.env`:
```env
OLLAMA_MODEL=mistral:7b
```

## 🎉 You're Ready!

Start chatting with your research assistant!

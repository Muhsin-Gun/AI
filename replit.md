# TradePackage AI

## Overview
TradePackage AI is a powerful, intelligent coding assistant that features both a beautiful web dashboard and an interactive Telegram bot. It's powered by free, open-source LLM models (LLaMA, Mixtral, Gemma) through the Groq API.

## Features
- **Code Generation** - Generate code in any programming language (Python, JavaScript, TypeScript, Flutter/Dart, PHP/Laravel, React, Go, Rust, C++, Java, and more)
- **Code Analysis** - Find bugs, security issues, and improvement suggestions
- **Website Creation** - Generate complete HTML/CSS/JS websites
- **Deep Research** - Research any topic comprehensively
- **Conversation Memory** - Remembers context within sessions
- **Multiple AI Models** - Switch between LLaMA 3.3 70B, LLaMA 3.1 8B, Mixtral 8x7B, and Gemma 2 9B

## Architecture

### Backend (FastAPI)
- **Location**: `backend/`
- **Main file**: `backend/app.py`
- **AI Client**: `backend/ai_client.py`
- **Static files**: `backend/static/`
- **Port**: 5000

### Telegram Bot
- **Location**: `telegram_bot.py`
- **Bot Token**: Stored in environment variables
- **Features**: Interactive inline keyboards, multiple modes, model selection

### AI Integration
- **Provider**: Groq (Free tier)
- **Models Available**:
  - `llama-3.3-70b-versatile` - Best quality
  - `llama-3.1-8b-instant` - Fast responses
  - `mixtral-8x7b-32768` - Balanced
  - `gemma2-9b-it` - Efficient

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve web dashboard |
| `/api/health` | GET | Health check |
| `/api/chat` | POST | General chat with AI |
| `/api/generate` | POST | Generate code |
| `/api/analyze` | POST | Analyze code |
| `/api/research` | POST | Deep research on topic |
| `/api/website` | POST | Create website |
| `/api/models` | GET | List available models |
| `/api/set-model` | POST | Change AI model |
| `/api/clear-history` | POST | Clear conversation history |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key (required) |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |

## Running the Project

### Web Dashboard
The web dashboard runs automatically on port 5000 when you start the "TradePackage AI" workflow.

### Telegram Bot
The Telegram bot runs as a separate workflow and connects to @TradepackageBot.

## Recent Changes
- Migrated from OpenAI to Groq (free LLaMA/Mistral models)
- Added beautiful web dashboard with animated UI
- Implemented interactive Telegram bot with inline keyboards
- Added model selection for both web and Telegram
- Created comprehensive API endpoints

## User Preferences
- Uses free, open-source AI models (no API costs)
- Modern, dark-themed UI
- Interactive telegram bot experience

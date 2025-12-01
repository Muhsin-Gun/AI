import os
import json
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are TradePackage AI - a powerful, intelligent coding assistant and research expert powered by LLaMA and Mistral open-source models.

Your capabilities:
- Generate code in ANY programming language (Python, JavaScript, TypeScript, Flutter/Dart, Laravel/PHP, React, Vue, Angular, Go, Rust, C++, Java, and more)
- Create complete websites and web applications
- Debug and fix code issues
- Perform deep research and analysis
- Learn from conversations and improve responses
- Explain complex concepts clearly
- Apply code patches and modifications

You are smart, helpful, and always provide high-quality, working code. Format your responses with markdown for better readability. When providing code, always include complete, runnable examples."""

class AIClient:
    def __init__(self):
        self.conversation_history = {}
        self.current_model = "llama-3.3-70b-versatile"
    
    def get_available_models(self):
        return {
            "llama-3.3-70b-versatile": "LLaMA 3.3 70B (Best Quality)",
            "llama-3.1-8b-instant": "LLaMA 3.1 8B (Fast)",
            "mixtral-8x7b-32768": "Mixtral 8x7B (Balanced)",
            "gemma2-9b-it": "Gemma 2 9B (Efficient)"
        }
    
    def set_model(self, model_id: str):
        available = self.get_available_models()
        if model_id in available:
            self.current_model = model_id
            return True
        return False
    
    def get_history(self, user_id: str) -> list:
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]
    
    def add_to_history(self, user_id: str, role: str, content: str):
        history = self.get_history(user_id)
        history.append({"role": role, "content": content})
        if len(history) > 20:
            history.pop(0)
            history.pop(0)
    
    def clear_history(self, user_id: str):
        self.conversation_history[user_id] = []
    
    async def chat(self, prompt: str, user_id: str = "default", context: str = None, max_tokens: int = 4096) -> str:
        global client
        if not client:
            api_key = os.environ.get("GROQ_API_KEY")
            if api_key:
                client = Groq(api_key=api_key)
            else:
                return "Error: Groq API key is not configured. Please add your GROQ_API_KEY in the Secrets tab. Get a free key at https://console.groq.com"
        
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            history = self.get_history(user_id)
            messages.extend(history)
            
            if context:
                messages.append({"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"})
            else:
                messages.append({"role": "user", "content": prompt})
            
            self.add_to_history(user_id, "user", prompt)
            
            response = client.chat.completions.create(
                model=self.current_model,
                messages=messages,
                max_tokens=max_tokens
            )
            
            reply = response.choices[0].message.content
            self.add_to_history(user_id, "assistant", reply)
            
            return reply
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def analyze_code(self, code: str, language: str = "auto") -> str:
        prompt = f"""Analyze this code and provide:
1. A summary of what it does
2. Any bugs or issues found
3. Security vulnerabilities
4. Performance improvements
5. Code style suggestions

Language: {language}

```
{code}
```"""
        return await self.chat(prompt)
    
    async def generate_code(self, description: str, language: str) -> str:
        prompt = f"""Generate complete, working {language} code for the following:

{description}

Requirements:
- Provide complete, runnable code
- Include comments explaining key parts
- Follow best practices for {language}
- Handle errors appropriately"""
        return await self.chat(prompt)
    
    async def research(self, topic: str) -> str:
        prompt = f"""Perform deep research on: {topic}

Provide:
1. Comprehensive overview
2. Key concepts and terminology
3. Current best practices
4. Common pitfalls to avoid
5. Useful resources and next steps
6. Code examples if applicable"""
        return await self.chat(prompt)
    
    async def create_website(self, description: str) -> str:
        prompt = f"""Create a complete website based on this description:

{description}

Provide:
1. Complete HTML with inline CSS and JavaScript
2. Modern, responsive design
3. Interactive elements
4. Clean, professional styling
5. The code should be ready to run directly"""
        return await self.chat(prompt)

ai_client = AIClient()

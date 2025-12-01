import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode, ChatAction
import aiohttp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API_BASE = "http://localhost:5000/api"

WELCOME_MESSAGE = """
🤖 *Welcome to TradePackage AI!*

I'm your intelligent coding assistant powered by advanced AI. I can help you with:

✨ *Code Generation* - Create code in any language
🔍 *Code Analysis* - Find bugs and improvements  
🌐 *Website Creation* - Build complete websites
📚 *Deep Research* - Research any topic thoroughly
💡 *Problem Solving* - Debug and fix issues

Use the buttons below or just type your message!
"""

def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("💻 Generate Code", callback_data="mode_code"),
            InlineKeyboardButton("🔍 Analyze Code", callback_data="mode_analyze")
        ],
        [
            InlineKeyboardButton("🌐 Create Website", callback_data="mode_website"),
            InlineKeyboardButton("📚 Deep Research", callback_data="mode_research")
        ],
        [
            InlineKeyboardButton("💬 Chat Mode", callback_data="mode_chat"),
            InlineKeyboardButton("🗑️ Clear History", callback_data="clear_history")
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ],
        [
            InlineKeyboardButton("🤖 Change AI Model", callback_data="models")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_language_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🐍 Python", callback_data="lang_python"),
            InlineKeyboardButton("📜 JavaScript", callback_data="lang_javascript")
        ],
        [
            InlineKeyboardButton("⚛️ React", callback_data="lang_react"),
            InlineKeyboardButton("🎯 TypeScript", callback_data="lang_typescript")
        ],
        [
            InlineKeyboardButton("🐘 PHP/Laravel", callback_data="lang_php"),
            InlineKeyboardButton("📱 Flutter/Dart", callback_data="lang_dart")
        ],
        [
            InlineKeyboardButton("🦀 Rust", callback_data="lang_rust"),
            InlineKeyboardButton("🐹 Go", callback_data="lang_go")
        ],
        [
            InlineKeyboardButton("☕ Java", callback_data="lang_java"),
            InlineKeyboardButton("💎 C++", callback_data="lang_cpp")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]])

def get_model_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🦙 LLaMA 3.3 70B", callback_data="model_llama-3.3-70b-versatile")
        ],
        [
            InlineKeyboardButton("⚡ LLaMA 3.1 8B (Fast)", callback_data="model_llama-3.1-8b-instant")
        ],
        [
            InlineKeyboardButton("🔮 Mixtral 8x7B", callback_data="model_mixtral-8x7b-32768")
        ],
        [
            InlineKeyboardButton("💎 Gemma 2 9B", callback_data="model_gemma2-9b-it")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def api_request(endpoint: str, data: dict) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_BASE}/{endpoint}", json=data, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"error": f"API error: {resp.status}"}
    except Exception as e:
        return {"error": str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'chat'
    context.user_data['language'] = None
    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 *TradePackage AI Help*

*Commands:*
/start - Start the bot
/help - Show this help
/menu - Show main menu
/clear - Clear chat history

*Modes:*
💻 *Generate Code* - Describe what you need, I'll write the code
🔍 *Analyze Code* - Paste code for bug detection and improvements
🌐 *Create Website* - Describe your website, I'll build it
📚 *Deep Research* - Ask about any topic for comprehensive research
💬 *Chat Mode* - Free conversation about anything

*Tips:*
• Be specific in your requests
• Include context when needed
• Ask follow-up questions for more detail
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_keyboard())

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("*Main Menu*\nChoose an action:", parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_keyboard())

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await api_request("clear-history", {"user_id": user_id})
    await update.message.reply_text("✅ Chat history cleared!", reply_markup=get_main_keyboard())

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "menu":
        context.user_data['mode'] = 'chat'
        context.user_data['language'] = None
        await query.edit_message_text("*Main Menu*\nChoose an action:", parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_keyboard())
    
    elif data == "mode_code":
        context.user_data['mode'] = 'code'
        await query.edit_message_text("*💻 Code Generation*\n\nSelect a programming language:", parse_mode=ParseMode.MARKDOWN, reply_markup=get_language_keyboard())
    
    elif data == "mode_analyze":
        context.user_data['mode'] = 'analyze'
        await query.edit_message_text("*🔍 Code Analysis*\n\nPaste your code and I'll analyze it for bugs, improvements, and best practices.", parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    elif data == "mode_website":
        context.user_data['mode'] = 'website'
        await query.edit_message_text("*🌐 Website Creation*\n\nDescribe the website you want to create. Include:\n• Purpose/type of website\n• Features needed\n• Design preferences\n• Any specific requirements", parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    elif data == "mode_research":
        context.user_data['mode'] = 'research'
        await query.edit_message_text("*📚 Deep Research Mode*\n\nWhat topic would you like me to research? I'll provide comprehensive information, best practices, and examples.", parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    elif data == "mode_chat":
        context.user_data['mode'] = 'chat'
        await query.edit_message_text("*💬 Chat Mode*\n\nJust type your message! I can help with coding, debugging, explanations, or anything else.", parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    elif data.startswith("lang_"):
        lang = data.replace("lang_", "")
        context.user_data['language'] = lang
        lang_names = {
            "python": "Python 🐍",
            "javascript": "JavaScript 📜",
            "react": "React ⚛️",
            "typescript": "TypeScript 🎯",
            "php": "PHP/Laravel 🐘",
            "dart": "Flutter/Dart 📱",
            "rust": "Rust 🦀",
            "go": "Go 🐹",
            "java": "Java ☕",
            "cpp": "C++ 💎"
        }
        await query.edit_message_text(f"*💻 {lang_names.get(lang, lang)} Code Generation*\n\nDescribe what code you need. Be as specific as possible!", parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    elif data == "clear_history":
        user_id = str(update.effective_user.id)
        await api_request("clear-history", {"user_id": user_id})
        await query.edit_message_text("✅ Chat history cleared!\n\nYour conversation memory has been reset.", reply_markup=get_main_keyboard())
    
    elif data == "help":
        help_text = """*🤖 TradePackage AI Help*

*Available Modes:*
💻 Generate Code - Create code in any language
🔍 Analyze Code - Find bugs and improvements
🌐 Create Website - Build complete websites
📚 Deep Research - Research any topic
💬 Chat Mode - Free conversation

*Tips:*
• Be specific in your requests
• Include context when needed
• Ask follow-up questions"""
        await query.edit_message_text(help_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    elif data == "settings":
        settings_text = """*⚙️ Settings*

Current configuration:
• Model: LLaMA 3.3 70B (Free)
• Max Response: 4096 tokens
• Memory: Last 20 messages

_Tap "Change AI Model" to switch models!_"""
        await query.edit_message_text(settings_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    elif data == "models":
        models_text = """*🤖 Select AI Model*

Choose from these FREE open-source models:

🦙 *LLaMA 3.3 70B* - Best quality, most capable
⚡ *LLaMA 3.1 8B* - Fast responses
🔮 *Mixtral 8x7B* - Great balance
💎 *Gemma 2 9B* - Efficient & smart"""
        await query.edit_message_text(models_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_model_keyboard())
    
    elif data.startswith("model_"):
        model_id = data.replace("model_", "")
        model_names = {
            "llama-3.3-70b-versatile": "LLaMA 3.3 70B 🦙",
            "llama-3.1-8b-instant": "LLaMA 3.1 8B ⚡",
            "mixtral-8x7b-32768": "Mixtral 8x7B 🔮",
            "gemma2-9b-it": "Gemma 2 9B 💎"
        }
        await api_request("set-model", {"model_id": model_id})
        await query.edit_message_text(f"✅ *Model Changed!*\n\nNow using: *{model_names.get(model_id, model_id)}*\n\nThis model is completely FREE!", parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message = update.message.text
    mode = context.user_data.get('mode', 'chat')
    language = context.user_data.get('language')
    
    await update.message.chat.send_action(ChatAction.TYPING)
    
    thinking_msg = await update.message.reply_text("🤔 *Thinking...*", parse_mode=ParseMode.MARKDOWN)
    
    try:
        if mode == 'code' and language:
            result = await api_request("generate", {"description": message, "language": language, "user_id": user_id})
            response = result.get("code", result.get("error", "Error generating code"))
        elif mode == 'analyze':
            result = await api_request("analyze", {"code": message, "user_id": user_id})
            response = result.get("analysis", result.get("error", "Error analyzing code"))
        elif mode == 'website':
            result = await api_request("website", {"description": message, "user_id": user_id})
            response = result.get("website", result.get("error", "Error creating website"))
        elif mode == 'research':
            result = await api_request("research", {"topic": message, "user_id": user_id})
            response = result.get("research", result.get("error", "Error researching topic"))
        else:
            result = await api_request("chat", {"text": message, "user_id": user_id})
            response = result.get("response", result.get("error", "Error processing request"))
        
        await thinking_msg.delete()
        
        if len(response) > 4000:
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for i, chunk in enumerate(chunks):
                if i == len(chunks) - 1:
                    await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
                else:
                    await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN, reply_markup=get_back_keyboard())
    
    except Exception as e:
        await thinking_msg.delete()
        await update.message.reply_text(f"❌ Error: {str(e)}\n\nPlease try again.", reply_markup=get_main_keyboard())

async def set_commands(application: Application):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("menu", "Show main menu"),
        BotCommand("help", "Get help"),
        BotCommand("clear", "Clear chat history")
    ]
    await application.bot.set_my_commands(commands)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.post_init = set_commands
    
    logger.info("Starting TradePackage AI Telegram Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

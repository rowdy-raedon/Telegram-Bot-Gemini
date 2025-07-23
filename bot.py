import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from config import TELEGRAM_BOT_TOKEN, GOOGLE_API_KEY
import google.generativeai as genai

# Gemini AI setup
model = genai.GenerativeModel("gemini-2.0-flash")
genai.configure(api_key=GOOGLE_API_KEY)

# Inline keyboard for Gemini chat
inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💬 Chat with Gemini", callback_data="chat_gemini")],
    ]
)

# Clean architecture: Service for Gemini
class GeminiService:
    def __init__(self, model):
        self.model = model

    async def ask(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip() if hasattr(response, 'text') else str(response)
        except Exception as e:
            return f"[Gemini Error] {e}"

gemini_service = GeminiService(model)

# Bot setup
bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# /start handler
@dp.message(Command("start"))
async def start_handler(message: types.Message, bot: Bot):
    await message.answer("<b>Welcome to Gemini-Powered Bot!</b>\nChoose an option:", reply_markup=inline_kb)

# /ask handler
@dp.message(Command("ask"))
async def ask_handler(message: types.Message, command: CommandObject):
    prompt = command.args or "What can you do?"
    await message.answer("<i>Thinking...</i>")
    reply = await gemini_service.ask(prompt)
    await message.answer(reply)

# Inline button handler
@dp.callback_query(F.data == "chat_gemini")
async def inline_chat_handler(callback: types.CallbackQuery):
    await callback.message.answer("<b>Ask me anything!</b>")
    await callback.answer()

# Auto-reply for any other message
@dp.message()
async def fallback_handler(message: types.Message):
    await message.answer("<i>Thinking...</i>")
    reply = await gemini_service.ask(message.text)
    await message.answer(reply)

# Entry point
def main():
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    main() 
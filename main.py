import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from config import BOT_TOKEN
import asyncio
import re
from datetime import datetime

# Create bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Store user data (in production, use a database)
user_sessions = {}

# ==================== KEYBOARD BUILDERS ====================

def get_main_menu_keyboard():
    """Main menu with reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Interactive Menu")],
            [KeyboardButton(text="🧮 Calculator"), KeyboardButton(text="📊 Text Analysis")],
            [KeyboardButton(text="🧩 Quiz Game"), KeyboardButton(text="📞 Contact")],
            [KeyboardButton(text="❌ Remove Keyboard")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_interactive_menu_keyboard():
    """Inline keyboard for interactive menu"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🕐 Current Time", callback_data="time"),
            InlineKeyboardButton(text="📅 Current Date", callback_data="date")
        ],
        [
            InlineKeyboardButton(text="🎲 Random Number", callback_data="random"),
            InlineKeyboardButton(text="🔄 Echo Mode", callback_data="echo_mode")
        ],
        [
            InlineKeyboardButton(text="🔙 Back to Main", callback_data="back_main")
        ]
    ])
    return keyboard

def get_calculator_keyboard():
    """Calculator keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="calc_1"),
            InlineKeyboardButton(text="2", callback_data="calc_2"),
            InlineKeyboardButton(text="3", callback_data="calc_3"),
            InlineKeyboardButton(text="+", callback_data="calc_add")
        ],
        [
            InlineKeyboardButton(text="4", callback_data="calc_4"),
            InlineKeyboardButton(text="5", callback_data="calc_5"),
            InlineKeyboardButton(text="6", callback_data="calc_6"),
            InlineKeyboardButton(text="-", callback_data="calc_sub")
        ],
        [
            InlineKeyboardButton(text="7", callback_data="calc_7"),
            InlineKeyboardButton(text="8", callback_data="calc_8"),
            InlineKeyboardButton(text="9", callback_data="calc_9"),
            InlineKeyboardButton(text="×", callback_data="calc_mul")
        ],
        [
            InlineKeyboardButton(text="C", callback_data="calc_clear"),
            InlineKeyboardButton(text="0", callback_data="calc_0"),
            InlineKeyboardButton(text="=", callback_data="calc_equals"),
            InlineKeyboardButton(text="÷", callback_data="calc_div")
        ]
    ])
    return keyboard

def get_quiz_keyboard():
    """Quiz game keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🐱 Cat", callback_data="quiz_cat"),
            InlineKeyboardButton(text="🐶 Dog", callback_data="quiz_dog")
        ],
        [
            InlineKeyboardButton(text="🐘 Elephant", callback_data="quiz_elephant"),
            InlineKeyboardButton(text="🦁 Lion", callback_data="quiz_lion")
        ],
        [
            InlineKeyboardButton(text="🔙 Back to Main", callback_data="back_main")
        ]
    ])
    return keyboard

def get_text_analysis_keyboard():
    """Text analysis options keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Count Words", callback_data="analyze_words"),
            InlineKeyboardButton(text="🔤 Count Chars", callback_data="analyze_chars")
        ],
        [
            InlineKeyboardButton(text="🔄 Reverse Text", callback_data="analyze_reverse"),
            InlineKeyboardButton(text="🔤 Case Convert", callback_data="analyze_case")
        ],
        [
            InlineKeyboardButton(text="🔙 Back to Main", callback_data="back_main")
        ]
    ])
    return keyboard

# ==================== COMMAND HANDLERS ====================

@dp.message(CommandStart())
async def start_bot(message: Message):
    """Welcome message with main menu"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Initialize user session
    user_sessions[user_id] = {
        "calculator": "",
        "echo_mode": False,
        "analysis_mode": None
    }
    
    welcome_text = (
        f"👋 Hello {user_name}!\n\n"
        "🤖 I'm your advanced Telegram bot with multiple features:\n\n"
        "🎮 **Interactive Menu** - Time, date, random numbers\n"
        "🧮 **Calculator** - Basic calculations\n"
        "📊 **Text Analysis** - Word count, character count, etc.\n"
        "🧩 **Quiz Game** - Test your knowledge\n"
        "📞 **Contact** - Get in touch\n\n"
        "Choose an option from the menu below:"
    )
    
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())

@dp.message(Command("help"))
async def help_command(message: Message):
    """Help command"""
    help_text = (
        "📚 **Bot Commands & Features:**\n\n"
        "🔸 **Main Menu** - Use the keyboard buttons\n"
        "🔸 **Interactive Menu** - Time, date, random numbers\n"
        "🔸 **Calculator** - Basic math operations\n"
        "🔸 **Text Analysis** - Analyze your text\n"
        "🔸 **Quiz Game** - Test your knowledge\n\n"
        "💡 **Tips:**\n"
        "• Send any text to test echo mode\n"
        "• Use /help for this message\n"
        "• Use /start to reset the bot"
    )
    await message.answer(help_text, parse_mode="Markdown")

# ==================== REPLY KEYBOARD HANDLERS ====================

@dp.message(F.text == "🎮 Interactive Menu")
async def show_interactive_menu(message: Message):
    """Show interactive menu with inline buttons"""
    await message.answer(
        "🎮 **Interactive Menu**\n\n"
        "Choose an option:",
        reply_markup=get_interactive_menu_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "🧮 Calculator")
async def show_calculator(message: Message):
    """Show calculator interface"""
    user_id = message.from_user.id
    user_sessions[user_id]["calculator"] = ""
    
    await message.answer(
        "🧮 **Calculator**\n\n"
        "Current: 0\n\n"
        "Click buttons to calculate:",
        reply_markup=get_calculator_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "📊 Text Analysis")
async def show_text_analysis(message: Message):
    """Show text analysis options"""
    await message.answer(
        "📊 **Text Analysis**\n\n"
        "Choose what you want to analyze:",
        reply_markup=get_text_analysis_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "🧩 Quiz Game")
async def show_quiz(message: Message):
    """Show quiz game"""
    await message.answer(
        "🧩 **Quiz Game**\n\n"
        "Which animal is the largest land mammal?",
        reply_markup=get_quiz_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "📞 Contact")
async def show_contact(message: Message):
    """Show contact information"""
    contact_text = (
        "📞 **Contact Information**\n\n"
        "🤖 **Bot Name:** Advanced Telegram Bot\n"
        "👨‍💻 **Developer:** AI Assistant\n"
        "📧 **Email:** ramizmatlabov923@gmail.com\n"
        "📱 **Phone:** +998334334404\n"
        "💬 Feel free to ask questions!"
    )
    await message.answer(contact_text, parse_mode="Markdown")

@dp.message(F.text == "❌ Remove Keyboard")
async def remove_keyboard(message: Message):
    """Remove the reply keyboard"""
    await message.answer(
        "⌨️ Keyboard removed!\n\n"
        "Send /start to get it back.",
        reply_markup=ReplyKeyboardRemove()
    )

# ==================== INLINE KEYBOARD HANDLERS ====================

@dp.callback_query(F.data == "time")
async def show_time(callback: CallbackQuery):
    """Show current time"""
    current_time = datetime.now().strftime("%H:%M:%S")
    await callback.message.answer(f"🕐 Current time: **{current_time}**", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "date")
async def show_date(callback: CallbackQuery):
    """Show current date"""
    current_date = datetime.now().strftime("%B %d, %Y")
    await callback.message.answer(f"📅 Current date: **{current_date}**", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "random")
async def show_random_number(callback: CallbackQuery):
    """Show random number"""
    import random
    random_num = random.randint(1, 100)
    await callback.message.answer(f"🎲 Random number: **{random_num}**", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "echo_mode")
async def toggle_echo_mode(callback: CallbackQuery):
    """Toggle echo mode"""
    user_id = callback.from_user.id
    user_sessions[user_id]["echo_mode"] = not user_sessions[user_id]["echo_mode"]
    
    status = "ON" if user_sessions[user_id]["echo_mode"] else "OFF"
    await callback.message.answer(f"🔄 Echo mode: **{status}**\n\nSend any message to test!", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    """Go back to main menu"""
    await callback.message.answer(
        "🏠 **Main Menu**\n\n"
        "Choose an option from the keyboard below:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# ==================== CALCULATOR HANDLERS ====================

@dp.callback_query(F.data.startswith("calc_"))
async def handle_calculator(callback: CallbackQuery):
    """Handle calculator button clicks"""
    user_id = callback.from_user.id
    action = callback.data.split("_")[1]
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {"calculator": ""}
    
    if action == "clear":
        user_sessions[user_id]["calculator"] = ""
        display_text = "0"
    elif action == "equals":
        try:
            expression = user_sessions[user_id]["calculator"].replace("×", "*").replace("÷", "/")
            result = eval(expression)
            display_text = f"{expression} = {result}"
            user_sessions[user_id]["calculator"] = str(result)
        except:
            display_text = "Error in calculation!"
            user_sessions[user_id]["calculator"] = ""
    else:
        if action in ["add", "sub", "mul", "div"]:
            operators = {"add": "+", "sub": "-", "mul": "×", "div": "÷"}
            user_sessions[user_id]["calculator"] += f" {operators[action]} "
        else:
            user_sessions[user_id]["calculator"] += action
        display_text = user_sessions[user_id]["calculator"]
    
    await callback.message.edit_text(
        f"🧮 **Calculator**\n\n"
        f"Current: {display_text}\n\n"
        f"Click buttons to calculate:",
        reply_markup=get_calculator_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# ==================== QUIZ HANDLERS ====================

@dp.callback_query(F.data == "quiz_elephant")
async def correct_quiz_answer(callback: CallbackQuery):
    """Handle correct quiz answer"""
    await callback.message.answer("🎉 **Correct!** Elephants are the largest land mammals!", parse_mode="Markdown")
    await callback.answer("Correct! 🎉")

@dp.callback_query(F.data.startswith("quiz_") & (F.data != "quiz_elephant"))
async def wrong_quiz_answer(callback: CallbackQuery):
    """Handle wrong quiz answer"""
    await callback.message.answer("❌ **Wrong answer!** Try again.", parse_mode="Markdown")
    await callback.answer("Try again! ❌")

# ==================== TEXT ANALYSIS HANDLERS ====================

@dp.callback_query(F.data == "analyze_words")
async def analyze_words_mode(callback: CallbackQuery):
    """Set word count analysis mode"""
    user_id = callback.from_user.id
    user_sessions[user_id]["analysis_mode"] = "words"
    await callback.message.answer("📝 **Word Count Mode Activated!**\n\nSend me any text and I'll count the words for you.")
    await callback.answer()

@dp.callback_query(F.data == "analyze_chars")
async def analyze_chars_mode(callback: CallbackQuery):
    """Set character count analysis mode"""
    user_id = callback.from_user.id
    user_sessions[user_id]["analysis_mode"] = "chars"
    await callback.message.answer("🔤 **Character Count Mode Activated!**\n\nSend me any text and I'll count the characters for you.")
    await callback.answer()

@dp.callback_query(F.data == "analyze_reverse")
async def analyze_reverse_mode(callback: CallbackQuery):
    """Set reverse text mode"""
    user_id = callback.from_user.id
    user_sessions[user_id]["analysis_mode"] = "reverse"
    await callback.message.answer("🔄 **Text Reverse Mode Activated!**\n\nSend me any text and I'll reverse it for you.")
    await callback.answer()

@dp.callback_query(F.data == "analyze_case")
async def analyze_case_mode(callback: CallbackQuery):
    """Set case conversion mode"""
    user_id = callback.from_user.id
    user_sessions[user_id]["analysis_mode"] = "case"
    await callback.message.answer("🔤 **Case Conversion Mode Activated!**\n\nSend me any text and I'll show you both uppercase and lowercase versions.")
    await callback.answer()

# ==================== TEXT MESSAGE HANDLERS ====================

@dp.message(F.text & F.reply_to_message)
async def handle_replied_text(message: Message):
    """Handle text that's a reply to bot messages"""
    user_id = message.from_user.id
    
    if user_id in user_sessions and user_sessions[user_id].get("analysis_mode"):
        mode = user_sessions[user_id]["analysis_mode"]
        text = message.text
        
        if mode == "words":
            word_count = len(text.split())
            await message.answer(f"📝 **Word Count:** {word_count} words")
        elif mode == "chars":
            char_count = len(text)
            char_no_spaces = len(text.replace(" ", ""))
            await message.answer(
                f"🔤 **Character Analysis:**\n"
                f"• Total characters: {char_count}\n"
                f"• Characters (no spaces): {char_no_spaces}"
            )
        elif mode == "reverse":
            reversed_text = text[::-1]
            await message.answer(f"🔄 **Reversed:** {reversed_text}")
        elif mode == "case":
            upper_text = text.upper()
            lower_text = text.lower()
            await message.answer(
                f"🔤 **Case Conversion:**\n"
                f"• UPPERCASE: {upper_text}\n"
                f"• lowercase: {lower_text}"
            )
        
        user_sessions[user_id]["analysis_mode"] = None

@dp.message(F.text)
async def handle_regular_text(message: Message):
    """Handle regular text messages"""
    user_id = message.from_user.id
    text = message.text
    
    # Check if user is in analysis mode
    if user_id in user_sessions and user_sessions[user_id].get("analysis_mode"):
        mode = user_sessions[user_id]["analysis_mode"]
        
        if mode == "words":
            word_count = len(text.split())
            await message.answer(f"📝 **Word Count:** {word_count} words")
        elif mode == "chars":
            char_count = len(text)
            char_no_spaces = len(text.replace(" ", ""))
            await message.answer(
                f"🔤 **Character Analysis:**\n"
                f"• Total characters: {char_count}\n"
                f"• Characters (no spaces): {char_no_spaces}"
            )
        elif mode == "reverse":
            reversed_text = text[::-1]
            await message.answer(f"🔄 **Reversed:** {reversed_text}")
        elif mode == "case":
            upper_text = text.upper()
            lower_text = text.lower()
            await message.answer(
                f"🔤 **Case Conversion:**\n"
                f"• UPPERCASE: {upper_text}\n"
                f"• lowercase: {lower_text}"
            )
        
        user_sessions[user_id]["analysis_mode"] = None
        return
    
    # Check if echo mode is enabled
    if user_id in user_sessions and user_sessions[user_id].get("echo_mode"):
        await message.answer(f"🔄 **Echo:** {text}")
        return
    
    # Handle greetings
    if any(word in text.lower() for word in ['hello', 'hi', 'hey', 'привет']):
        await message.answer("👋 **Hello there!** How can I help you today?")
        return
    
    # Handle long messages
    if len(text) > 100:
        await message.answer("📝 **Long message received!** That's quite a lot of text!")
        return
    
    # Handle short messages
    if len(text) < 10:
        await message.answer("💬 **Short message!** Feel free to send longer text for analysis.")
        return
    
    # Default response
    await message.answer(
        "💬 **Message received!**\n\n"
        "💡 **Tips:**\n"
        "• Use the keyboard buttons for features\n"
        "• Send /help for commands\n"
        "• Try the Interactive Menu for fun features"
    )

@dp.message(F.text.regexp(r'\b\d+\b'))
async def handle_numbers_in_text(message: Message):
    """Handle text containing numbers"""
    numbers = re.findall(r'\b\d+\b', message.text)
    total = sum(int(num) for num in numbers)
    await message.answer(f"🔢 **Numbers found:** {', '.join(numbers)}\n**Sum:** {total}")

@dp.message(F.text.regexp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'))
async def handle_email_in_text(message: Message):
    """Handle text containing email addresses"""
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message.text)
    await message.answer(f"📧 **Email(s) found:** {', '.join(emails)}")

@dp.message(F.text.regexp(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'))
async def handle_url_in_text(message: Message):
    """Handle text containing URLs"""
    await message.answer("🔗 **URL detected!** I found a link in your message.")



# ==================== ERROR HANDLER ====================

@dp.errors()
async def errors_handler(update, exception):
    """Handle errors gracefully"""
    print(f"Error occurred: {exception}")
    try:
        await update.message.answer("❌ **An error occurred.** Please try again or use /start to reset.")
    except:
        pass

# ==================== MAIN FUNCTION ====================

async def main():
    """Main function to start the bot"""
    print("🤖 Advanced Telegram Bot is starting...")
    print("📱 Bot features:")
    print("   • Interactive menus with keyboards")
    print("   • Calculator functionality")
    print("   • Text analysis tools")
    print("   • Quiz game")
    print("   • Pattern matching for emails, URLs, numbers")
    print("   • Echo mode")
    print("   • Error handling")
    print("✅ Bot is ready!")
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
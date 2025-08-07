from aiogram import Router, types
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "menu")
async def show_menu(callback: CallbackQuery):
    menu_text = """
🍽️ <b>Our Menu</b>

<b>🍕 Pizza</b>
• Margherita - $12
• Pepperoni - $14
• Hawaiian - $15

<b>🍔 Burgers</b>
• Classic Burger - $10
• Cheese Burger - $11
• Veggie Burger - $9

<b>🥗 Salads</b>
• Caesar Salad - $8
• Greek Salad - $9
• Garden Salad - $7

<b>🥤 Drinks</b>
• Soft Drinks - $3
• Coffee - $4
• Fresh Juice - $5
    """
    
    await callback.message.edit_text(
        menu_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "contact")
async def show_contact(callback: CallbackQuery):
    contact_text = """
📞 <b>Contact Information</b>

📱 Phone: +1 (555) 123-4567
📧 Email: info@restaurant.com
🌐 Website: www.restaurant.com

<b>Follow us:</b>
📘 Facebook: @restaurant
📷 Instagram: @restaurant
🐦 Twitter: @restaurant
    """
    
    await callback.message.edit_text(
        contact_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "location")
async def show_location(callback: CallbackQuery):
    await callback.message.edit_text(
        "📍 <b>Our Location</b>\n\n"
        "123 Main Street\n"
        "City Center, State 12345\n\n"
        "We're located in the heart of downtown!",
        reply_markup=get_back_keyboard()
    )
    # You can also send actual location
    await callback.message.answer_location(
        latitude=40.7128,  # Replace with actual coordinates
        longitude=-74.0060
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "hours")
async def show_hours(callback: CallbackQuery):
    hours_text = """
⏰ <b>Opening Hours</b>

<b>Monday - Thursday:</b> 11:00 AM - 10:00 PM
<b>Friday - Saturday:</b> 11:00 AM - 11:00 PM
<b>Sunday:</b> 12:00 PM - 9:00 PM

<b>Kitchen closes 30 minutes before closing time</b>
    """
    
    await callback.message.edit_text(
        hours_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "back")
async def go_back(callback: CallbackQuery):
    from keyboards.main_keyboard import get_main_keyboard
    
    await callback.message.edit_text(
        f"👋 Welcome back!\n\n"
        f"What would you like to do?",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


# Обработчик для кнопки "My Cart"
@router.callback_query(lambda c: c.data == "cart")
async def show_cart(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛒 <b>Your cart is empty</b>\n\nAdd items from the menu",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

def get_back_keyboard():
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="back")]
    ])
    return keyboard
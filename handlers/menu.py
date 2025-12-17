from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.main_keyboard import get_main_keyboard

router = Router()

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])

def get_add_to_cart_keyboard(product_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить в корзину", callback_data=f"add_to_cart_{product_id}")],
        [InlineKeyboardButton(text="◀️ Назад к каталогу", callback_data="catalog")]
    ])

@router.callback_query(lambda c: c.data == "water_5l")
async def show_water_5l(callback: CallbackQuery):
    product_text = """
💧 <b>Питьевая вода 5л</b>

<b>Описание:</b>
Чистая питьевая вода высшего качества в удобной таре объемом 5 литров.

<b>Характеристики:</b>
• Объем: 5 литров
• Минерализация: низкая
• Срок хранения: 12 месяцев

<b>Цена:</b> 7 000 сум
"""
    
    await callback.message.edit_text(
        product_text,
        reply_markup=get_add_to_cart_keyboard("water_5l")
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "water_10l")
async def show_water_10l(callback: CallbackQuery):
    product_text = """
💧 <b>Питьевая вода 10л</b>

<b>Описание:</b>
Чистая питьевая вода высшего качества в удобной таре объемом 10 литров.

<b>Характеристики:</b>
• Объем: 10 литров
• Минерализация: низкая
• Срок хранения: 12 месяцев

<b>Цена:</b> 13 000 сум
"""
    
    await callback.message.edit_text(
        product_text,
        reply_markup=get_add_to_cart_keyboard("water_10l")
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "water_19l")
async def show_water_19l(callback: CallbackQuery):
    product_text = """
💧 <b>Питьевая вода 19л</b>

<b>Описание:</b>
Чистая питьевая вода высшего качества в многоразовой таре объемом 19 литров.
Идеально подходит для кулеров и диспенсеров.

<b>Характеристики:</b>
• Объем: 19 литров
• Минерализация: низкая
• Срок хранения: 6 месяцев

<b>Цена:</b> 20 000 сум
"""
    
    await callback.message.edit_text(
        product_text,
        reply_markup=get_add_to_cart_keyboard("water_19l")
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "contact")
async def show_contact(callback: CallbackQuery):
    contact_text = """
📞 <b>Контактная информация</b>

📱 Телефон: +998 (33) 433-44-04
📧 Email: ramizmatlabov923@gmail.com
🌐 Сайт: https://my-project-56ug.onrender.com

<b>Мы в соцсетях:</b>
📘 Instagram: ramiz_matlabov
📷 Telegram: @ramiz_matlabov
"""
    
    await callback.message.edit_text(
        contact_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "delivery")
async def show_delivery(callback: CallbackQuery):
    delivery_text = """
🚚 <b>Доставка</b>

<b>Условия доставки:</b>
• Бесплатная доставка при заказе от 2 бутылей
• Доставка в течение 24 часов
• Возможен самовывоз со скидкой 5%

<b>График доставки:</b>
• Понедельник-Пятница: с 9:00 до 21:00
• Суббота-Воскресенье: с 10:00 до 18:00
"""
    
    await callback.message.edit_text(
        delivery_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "prices")
async def show_prices(callback: CallbackQuery):
    prices_text = """
💰 <b>Цены на воду</b>

<b>Питьевая вода:</b>
• 5 литров - 7 000 сум
• 10 литров - 13 000 сум
• 19 литров - 20 000 сум

<b>Оборудование:</b>
• Помпа механическая - 45 000 сум
• Помпа электрическая - 120 000 сум
• Кулер напольный - от 420 000 сум

<b>Скидки:</b>
• При заказе от 5 бутылей - скидка 5%
• При заказе от 10 бутылей - скидка 10%
"""
    
    await callback.message.edit_text(
        prices_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "about")
async def show_about(callback: CallbackQuery):
    about_text = """
❓ <b>О компании Ice Water🧊</b>

Компания Ice Water🧊 занимается доставкой чистой питьевой воды с 2010 года.

<b>Наши преимущества:</b>
• Собственное производство
• Многоступенчатая система очистки
• Регулярный контроль качества
• Быстрая доставка
• Удобная тара

Мы заботимся о вашем здоровье и комфорте!
"""
    
    await callback.message.edit_text(
        about_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "equipment")
async def show_equipment(callback: CallbackQuery):
    equipment_text = """
🔄 <b>Оборудование для воды</b>

<b>Помпы:</b>
• Механическая помпа - 45 000 сум
• Электрическая помпа - 120 000 сум

<b>Кулеры:</b>
• Настольный кулер - 420 000 сум
• Напольный кулер с охлаждением - 700 000 сум
• Напольный кулер с нагревом и охлаждением - 920 000 сум

<b>Аксессуары:</b>
• Подставка для бутыли - 30 000 сум
• Держатель стаканов - 7 000 сум
"""
    
    await callback.message.edit_text(
        equipment_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

# Обработчик для кнопки "Корзина"
@router.callback_query(lambda c: c.data == "cart")
async def show_cart(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛒 <b>Ваша корзина пуста</b>\n\nДобавьте товары из каталога",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()
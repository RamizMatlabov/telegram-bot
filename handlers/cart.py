from aiogram import Router, types, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_keyboard import get_main_keyboard, get_cart_keyboard

router = Router()

# Простое хранилище для корзин пользователей (в реальном боте лучше использовать БД)
user_carts = {}

# Информация о товарах
products = {
    "water_5l": {"name": "Питьевая вода 5л", "price": 7000},
    "water_10l": {"name": "Питьевая вода 10л", "price": 13000},
    "water_19l": {"name": "Питьевая вода 19л", "price": 20000},
}

# Состояния для оформления заказа
class OrderStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()
    waiting_for_confirmation = State()

# Добавление товара в корзину
@router.callback_query(lambda c: c.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    product_id = callback.data.replace("add_to_cart_", "")
    
    if user_id not in user_carts:
        user_carts[user_id] = {}
    
    if product_id in user_carts[user_id]:
        user_carts[user_id][product_id] = user_carts[user_id][product_id] + 1
    else:
        user_carts[user_id][product_id] = 1
    
    await callback.answer(f"{products[product_id]['name']} добавлен в корзину!")
    
    # Показываем обновленную корзину
    await show_cart(callback)

# Показать корзину
@router.callback_query(lambda c: c.data == "cart")
async def show_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id not in user_carts or not user_carts[user_id]:
        await callback.message.edit_text(
            "🛒 Ваша корзина\n\n"
            "Корзина пуста. Добавьте товары из каталога.",
            reply_markup=get_main_keyboard()
        )
    else:
        cart_text = "🛒 <b>Ваша корзина</b>\n\n"
        total = 0
        
        for product_id, quantity in user_carts[user_id].items():
            product_name = products[product_id]["name"]
            product_price = products[product_id]["price"]
            item_total = product_price * quantity
            total += item_total
            
            cart_text += f"• {product_name} x {quantity} = {item_total} сум\n"
        
        cart_text += f"\n<b>Итого:</b> {total} сум"
        
        await callback.message.edit_text(
            cart_text,
            reply_markup=get_cart_keyboard()
        )
    
    await callback.answer()

# Очистить корзину
@router.callback_query(lambda c: c.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id in user_carts:
        user_carts[user_id] = {}
    
    await callback.message.edit_text(
        "🛒 Ваша корзина\n\n"
        "Корзина очищена.",
        reply_markup=get_main_keyboard()
    )
    
    await callback.answer("Корзина очищена!")

# Начало оформления заказа
@router.callback_query(lambda c: c.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 <b>Оформление заказа</b>\n\n"
        "Пожалуйста, введите ваше имя:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_order")]
        ])
    )
    
    await state.set_state(OrderStates.waiting_for_name)
    await callback.answer()

# Отмена оформления заказа
@router.callback_query(lambda c: c.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    await callback.message.edit_text(
        "❌ Оформление заказа отменено.",
        reply_markup=get_main_keyboard()
    )
    
    await callback.answer()

# Получение имени
@router.message(OrderStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    await message.answer(
        "📱 Пожалуйста, введите ваш номер телефона:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_order")]
        ])
    )
    
    await state.set_state(OrderStates.waiting_for_phone)

# Получение телефона
@router.message(OrderStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    
    await message.answer(
        "🏠 Пожалуйста, введите адрес доставки:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_order")]
        ])
    )
    
    await state.set_state(OrderStates.waiting_for_address)

# Получение адреса и подтверждение заказа
@router.message(OrderStates.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    await state.update_data(address=message.text)
    user_data = await state.get_data()
    
    if user_id in user_carts and user_carts[user_id]:
        order_text = "📋 <b>Подтверждение заказа</b>\n\n"
        order_text += f"<b>Имя:</b> {user_data['name']}\n"
        order_text += f"<b>Телефон:</b> {user_data['phone']}\n"
        order_text += f"<b>Адрес:</b> {user_data['address']}\n\n"
        
        order_text += "<b>Товары:</b>\n"
        total = 0
        
        for product_id, quantity in user_carts[user_id].items():
            product_name = products[product_id]["name"]
            product_price = products[product_id]["price"]
            item_total = product_price * quantity
            total += item_total
            
            order_text += f"• {product_name} x {quantity} = {item_total} ₽\n"
        
        order_text += f"\n<b>Итого:</b> {total} ₽"
        
        await message.answer(
            order_text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data="confirm_order")],
                [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_order")]
            ])
        )
        
        await state.set_state(OrderStates.waiting_for_confirmation)
    else:
        await message.answer(
            "❌ Ваша корзина пуста. Невозможно оформить заказ.",
            reply_markup=get_main_keyboard()
        )
        await state.clear()

# Подтверждение заказа
@router.callback_query(lambda c: c.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_data = await state.get_data()
    
    # В реальном боте здесь был бы код для сохранения заказа в базу данных
    # и отправки уведомления администратору
    
    # Очищаем корзину пользователя
    if user_id in user_carts:
        user_carts[user_id] = {}
    
    await callback.message.edit_text(
        "✅ <b>Заказ успешно оформлен!</b>\n\n"
        f"Спасибо за заказ, {user_data['name']}!\n"
        "Наш менеджер свяжется с вами в ближайшее время для подтверждения заказа.\n\n"
        "Номер заказа: #" + str(user_id)[-4:] + str(hash(user_data['phone']))[-4:],
        reply_markup=get_main_keyboard()
    )
    
    await state.clear()
    await callback.answer("Заказ оформлен!")
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💧 Каталог воды", callback_data="catalog"),
            InlineKeyboardButton(text="🛒 Моя корзина", callback_data="cart")
        ],
        [
            InlineKeyboardButton(text="🚚 Доставка", callback_data="delivery"),
            InlineKeyboardButton(text="💰 Цены", callback_data="prices")
        ],
        [
            InlineKeyboardButton(text="📞 Контакты", callback_data="contact"),
            InlineKeyboardButton(text="❓ О нас", callback_data="about")
        ]
    ])
    return keyboard

def get_catalog_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧊 Питьевая вода 5л", callback_data="water_5l")
        ],
        [
            InlineKeyboardButton(text="🧊 Питьевая вода 10л", callback_data="water_10l")
        ],
        [
            InlineKeyboardButton(text="🧊 Питьевая вода 19л", callback_data="water_19l")
        ],
        [
            InlineKeyboardButton(text="🔄 Оборудование", callback_data="equipment")
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")
        ]
    ])
    return keyboard

def get_cart_keyboard(show_actions: bool = True):
    inline_keyboard = []

    if show_actions:
        inline_keyboard.extend(
            [
                [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")],
                [InlineKeyboardButton(text="🗑️ Очистить корзину", callback_data="clear_cart")],
            ]
        )

    inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from keyboards.main_keyboard import get_main_keyboard, get_catalog_keyboard, get_cart_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"👋 Здравствуйте, {message.from_user.full_name}!\n"
        f"Добро пожаловать в бот доставки чистой воды «Ice Water🧊»!\n\n"
        f"Я могу помочь вам:\n"
        f"💧 Выбрать и заказать питьевую воду\n"
        f"🚚 Узнать условия доставки\n"
        f"💰 Ознакомиться с ценами\n"
        f"📞 Получить контактную информацию",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(lambda c: c.data == "catalog")
async def show_catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        "💧 Каталог питьевой воды\n\n"
        "Выберите объем или оборудование:",
        reply_markup=get_catalog_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "cart")
async def show_cart(callback: CallbackQuery):
    # В реальном боте здесь был бы код для получения содержимого корзины
    await callback.message.edit_text(
        "🛒 Ваша корзина\n\n"
        "Корзина пуста. Добавьте товары из каталога.",
        reply_markup=get_cart_keyboard(show_actions=False)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        f"👋 Здравствуйте, {callback.from_user.full_name}!\n"
        f"Добро пожаловать в бот доставки чистой воды «Ice Water🧊»!\n\n"
        f"Я могу помочь вам:\n"
        f"💧 Выбрать и заказать питьевую воду\n"
        f"🚚 Узнать условия доставки\n"
        f"💰 Ознакомиться с ценами\n"
        f"📞 Получить контактную информацию",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

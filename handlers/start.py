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
    try:
        await callback.answer()  # Отвечаем сразу, чтобы избежать timeout
        await callback.message.edit_text(
            "💧 Каталог питьевой воды\n\n"
            "Выберите объем или оборудование:",
            reply_markup=get_catalog_keyboard()
        )
    except Exception as e:
        # Если callback уже обработан или устарел, просто игнорируем
        pass

@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    try:
        await callback.answer()  # Отвечаем сразу, чтобы избежать timeout
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
    except Exception as e:
        # Если callback уже обработан или устарел, просто игнорируем
        pass

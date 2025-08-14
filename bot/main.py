import asyncio
from datetime import datetime, timezone
from enum import Enum, auto

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from .config import load_settings


class States(Enum):
    MENU = auto()
    ORDER_DETAILS = auto()
    SUPPORT_DETAILS = auto()


MENU_BUTTON_ORDER = "🛒 Оформить заказ"
MENU_BUTTON_SUPPORT = "🛠️ Вызов техподдержки"
MENU_BUTTON_CANCEL = "❌ Отмена"


def build_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[MENU_BUTTON_ORDER], [MENU_BUTTON_SUPPORT]], resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = build_main_menu_keyboard()
    greeting = (
        "Здравствуйте! Я бот для приёма заявок на покупку товаров.\n\n"
        "Выберите действие из меню ниже или отправьте цифру:\n"
        "1 — вызов техподдержки\n"
        "2 — оформить заказ\n\n"
        "В любой момент вы можете отправить /cancel, чтобы отменить действие."
    )
    await update.effective_chat.send_message(greeting, reply_markup=keyboard)
    return States.MENU.value


def _normalize_choice(text: str) -> str:
    value = (text or "").strip().casefold()
    if value in {"1", "1.", "1 -", "вызов техподдержки", "вызов тех. поддержки", "техподдержка"}:
        return MENU_BUTTON_SUPPORT
    if value in {"2", "2.", "2 -", "оформить заказ", "заказ"}:
        return MENU_BUTTON_ORDER
    return text


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = _normalize_choice(update.message.text or "")

    if text == MENU_BUTTON_ORDER:
        prompt = (
            "Опишите заказ одним сообщением: что необходимо купить, количество, желаемые сроки и ваши контакты (телефон/ник).\n\n"
            "Пример: \"iPhone 15, 2 шт, нужен до 25 числа, +7 999 123-45-67\""
        )
        await update.effective_chat.send_message(prompt, reply_markup=ReplyKeyboardMarkup([[MENU_BUTTON_CANCEL]], resize_keyboard=True))
        return States.ORDER_DETAILS.value

    if text == MENU_BUTTON_SUPPORT:
        prompt = (
            "Кратко опишите вашу проблему одним сообщением. Наши специалисты свяжутся с вами."
        )
        await update.effective_chat.send_message(prompt, reply_markup=ReplyKeyboardMarkup([[MENU_BUTTON_CANCEL]], resize_keyboard=True))
        return States.SUPPORT_DETAILS.value

    await update.effective_chat.send_message(
        "Пожалуйста, выберите пункт меню: 1 — техподдержка, 2 — оформить заказ.",
        reply_markup=build_main_menu_keyboard(),
    )
    return States.MENU.value


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_chat.send_message(
        "Действие отменено.", reply_markup=ReplyKeyboardRemove()
    )
    # Return to the menu for convenience
    await asyncio.sleep(0)  # Yield control to keep loop responsive
    await start(update, context)
    return States.MENU.value


def _format_user_block(update: Update) -> str:
    user = update.effective_user
    full_name = (user.full_name or "").strip()
    username = f"@{user.username}" if user and user.username else "—"
    return (
        f"Имя: {full_name}\n"
        f"Username: {username}\n"
        f"User ID: {user.id}"
    )


async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    settings = context.application.bot_data.get("settings")
    assert settings is not None

    order_text = (update.message.text or "").strip()
    created_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    message_for_group = (
        "🆕 Новая заявка на покупку\n\n"
        f"{_format_user_block(update)}\n"
        f"Создано: {created_at}\n\n"
        f"Содержание заявки:\n{order_text}"
    )

    try:
        await context.bot.send_message(
            chat_id=settings.orders_group_id,
            text=message_for_group,
            parse_mode=ParseMode.HTML,
        )
    except Exception as exc:  # noqa: BLE001
        await update.effective_chat.send_message(
            "Не удалось отправить заявку в группу. Сообщите администратору."
        )
        # Log locally to server stderr
        print(f"Failed to send order to group: {exc}")
    else:
        await update.effective_chat.send_message(
            "Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.",
            reply_markup=build_main_menu_keyboard(),
        )

    return States.MENU.value


async def receive_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    settings = context.application.bot_data.get("settings")
    assert settings is not None

    support_text = (update.message.text or "").strip()
    created_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    maybe_sent_to_group = False
    if settings.support_group_id is not None:
        try:
            await context.bot.send_message(
                chat_id=settings.support_group_id,
                text=(
                    "🛠️ Запрос в техподдержку\n\n"
                    f"{_format_user_block(update)}\n"
                    f"Создано: {created_at}\n\n"
                    f"Описание:\n{support_text}"
                ),
                parse_mode=ParseMode.HTML,
            )
            maybe_sent_to_group = True
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to send support request to group: {exc}")

    if maybe_sent_to_group:
        reply_text = "Спасибо! Ваше обращение передано техподдержке. Мы скоро ответим."
    else:
        reply_text = (
            "Спасибо! Мы получили ваше обращение и скоро свяжемся с вами."
        )

    await update.effective_chat.send_message(reply_text, reply_markup=build_main_menu_keyboard())
    return States.MENU.value


async def fallback_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_chat.send_message(
        "Пожалуйста, используйте пункты меню или введите /start для начала.",
        reply_markup=build_main_menu_keyboard(),
    )
    return States.MENU.value


def build_application() -> Application:
    settings = load_settings()

    app = Application.builder().token(settings.telegram_bot_token).build()
    # Stash settings for handlers
    app.bot_data["settings"] = settings

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.MENU.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu),
            ],
            States.ORDER_DETAILS.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_order),
            ],
            States.SUPPORT_DETAILS.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_support),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
        allow_reentry=True,
    )

    app.add_handler(conv)

    # Optional: simple /help
    async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.effective_chat.send_message(
            "Команды:\n/start — начать\n/cancel — отменить текущее действие\n/help — справка",
            reply_markup=build_main_menu_keyboard(),
        )

    app.add_handler(CommandHandler("help", help_cmd))

    # Catch-all fallback so users who write arbitrary text in private chat get a hint
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_text))

    return app


async def main() -> None:
    app = build_application()
    print("Bot is starting... Press Ctrl+C to stop.")
    await app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
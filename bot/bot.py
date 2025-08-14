import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
	Application,
	ApplicationBuilder,
	CommandHandler,
	ContextTypes,
	MessageHandler,
	ConversationHandler,
	filters,
)

# States
SUPPORT_WAITING, ORDER_WAITING = range(2)


def build_main_menu() -> ReplyKeyboardMarkup:
	keyboard = [
		[KeyboardButton(text="1 — Вызов техподдержки")],
		[KeyboardButton(text="2 — Оформить заказ")],
	]
	return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Выберите действие")


def format_user_ref(update: Update) -> str:
	user = update.effective_user
	if not user:
		return "Неизвестный пользователь"
	name = (user.full_name or "Пользователь").strip()
	username = f"@{user.username}" if user.username else None
	uid = user.id
	parts = [name]
	if username:
		parts.append(f"({username})")
	parts.append(f"id: {uid}")
	return " ".join(parts)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.conversation_data.clear()
	instructions = (
		"Добро пожаловать!\n\n"
		"Выберите действие в меню ниже:\n"
		"1 — Вызов техподдержки\n"
		"2 — Оформить заказ\n\n"
		"В любой момент вы можете отправить /start чтобы начать заново."
	)
	await update.effective_message.reply_text(instructions, reply_markup=build_main_menu())
	return ConversationHandler.END


async def goto_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.effective_message.reply_text(
		"Опишите, пожалуйста, проблему одним сообщением.\n"
		"Мы постараемся ответить как можно скорее."
	)
	return SUPPORT_WAITING


async def support_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
	load_dotenv(override=False)
	support_chat_id = os.getenv("SUPPORT_CHAT_ID")
	text = update.effective_message.text or "(пустое сообщение)"
	user_ref = format_user_ref(update)
	formatted = (
		"📞 Запрос в техподдержку\n\n"
		f"От: {user_ref}\n"
		f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
		f"Сообщение:\n{text}"
	)
	if support_chat_id:
		try:
			await context.bot.send_message(chat_id=int(support_chat_id), text=formatted)
			await update.effective_message.reply_text("Ваше обращение отправлено в техподдержку. Мы свяжемся с вами здесь.")
		except Exception as exc:  # noqa: BLE001
			logging.exception("Ошибка отправки в техподдержку: %s", exc)
			await update.effective_message.reply_text("Не удалось отправить обращение. Попробуйте позже или напишите администратору.")
	else:
		await update.effective_message.reply_text("Спасибо! Ваше обращение принято. Ожидайте ответ в этом чате.")

	await update.effective_message.reply_text("Что бы вы хотели сделать дальше?", reply_markup=build_main_menu())
	return ConversationHandler.END


async def goto_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.effective_message.reply_text(
		"Пожалуйста, одним сообщением укажите детали заказа:\n"
		"— Товар (модель/ссылка)\n"
		"— Количество\n"
		"— Контакты для связи (телефон/ник)\n\n"
		"Например: 'Наушники XYZ, 2 шт, +7 900 000-00-00'"
	)
	return ORDER_WAITING


async def order_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
	load_dotenv(override=False)
	orders_chat_id = os.getenv("ORDERS_CHAT_ID")
	if not orders_chat_id:
		await update.effective_message.reply_text("ORDERS_CHAT_ID не задан. Обратитесь к администратору.")
		return ConversationHandler.END

	text = update.effective_message.text or "(пустое сообщение)"
	user_ref = format_user_ref(update)
	formatted = (
		"📝 Новая заявка на заказ\n\n"
		f"От: {user_ref}\n"
		f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
		f"Детали заказа:\n{text}"
	)
	try:
		await context.bot.send_message(chat_id=int(orders_chat_id), text=formatted, parse_mode=ParseMode.HTML)
		await update.effective_message.reply_text("Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.")
	except Exception as exc:  # noqa: BLE001
		logging.exception("Ошибка отправки заявки: %s", exc)
		await update.effective_message.reply_text("Не удалось отправить заявку. Попробуйте позже или напишите администратору.")

	await update.effective_message.reply_text("Что бы вы хотели сделать дальше?", reply_markup=build_main_menu())
	return ConversationHandler.END


async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
	text = (update.effective_message.text or "").strip()
	if text == "1 — Вызов техподдержки":
		return await goto_support(update, context)
	if text == "2 — Оформить заказ":
		return await goto_order(update, context)
	# default: ignore
	return ConversationHandler.END


def main() -> None:
	logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
	load_dotenv()
	bot_token = os.getenv("BOT_TOKEN")
	if not bot_token:
		raise RuntimeError("Не задан BOT_TOKEN (см. .env)")

	application: Application = ApplicationBuilder().token(bot_token).build()

	conv = ConversationHandler(
		entry_points=[CommandHandler("start", cmd_start)],
		states={
			SUPPORT_WAITING: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_received)],
			ORDER_WAITING: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_received)],
		},
		fallbacks=[CommandHandler("start", cmd_start)],
		per_message=False,
	)

	application.add_handler(conv)
	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

	application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
	main()
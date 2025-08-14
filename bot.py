import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен бота и ID группы из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

if not BOT_TOKEN:
    raise ValueError("Не установлен BOT_TOKEN в переменных окружения")

if not GROUP_ID:
    raise ValueError("Не установлен GROUP_ID в переменных окружения")

# Состояния пользователей
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Сбрасываем состояние пользователя
    user_states[user.id] = None
    
    # Создаем клавиатуру с меню
    keyboard = [
        [InlineKeyboardButton("1️⃣ Вызов тех. поддержки", callback_data="support")],
        [InlineKeyboardButton("2️⃣ Оформить заказ", callback_data="order")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🤖 Добро пожаловать в бот для заказов!

👋 Привет, {user.first_name}!

Здесь вы можете:
• Вызвать техническую поддержку
• Оформить заказ на покупку товаров

Выберите нужный пункт из меню ниже:
"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "support":
        await handle_support(query, context)
    elif query.data == "order":
        await handle_order_start(query, context)
    elif query.data == "back_to_menu":
        await back_to_main_menu(query, context)

async def handle_support(query: CallbackQueryHandler, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка вызова тех. поддержки"""
    support_text = """
🆘 Техническая поддержка

Для связи с технической поддержкой:
• Email: support@example.com
• Телефон: +7 (999) 123-45-67
• Время работы: Пн-Пт 9:00-18:00

Опишите вашу проблему, и мы свяжемся с вами в ближайшее время.
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=support_text, reply_markup=reply_markup)

async def handle_order_start(query: CallbackQueryHandler, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начало оформления заказа"""
    user_id = query.from_user.id
    user_states[user_id] = "waiting_for_name"
    
    order_text = """
🛒 Оформление заказа

Для оформления заказа мне нужна следующая информация:

1️⃣ Ваше имя:
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=order_text, reply_markup=reply_markup)

async def back_to_main_menu(query: CallbackQueryHandler, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возврат в главное меню"""
    user = query.from_user
    user_states[user.id] = None
    
    keyboard = [
        [InlineKeyboardButton("1️⃣ Вызов тех. поддержки", callback_data="support")],
        [InlineKeyboardButton("2️⃣ Оформить заказ", callback_data="order")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    menu_text = f"""
🏠 Главное меню

Выберите нужный пункт:
"""
    
    await query.edit_message_text(text=menu_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений для сбора информации о заказе"""
    user_id = update.effective_user.id
    
    if user_id not in user_states or user_states[user_id] is None:
        return
    
    current_state = user_states[user_id]
    message_text = update.message.text
    
    if current_state == "waiting_for_name":
        # Сохраняем имя и переходим к следующему шагу
        context.user_data['customer_name'] = message_text
        user_states[user_id] = "waiting_for_phone"
        
        await update.message.reply_text("2️⃣ Ваш номер телефона:")
        
    elif current_state == "waiting_for_phone":
        # Сохраняем телефон и переходим к следующему шагу
        context.user_data['customer_phone'] = message_text
        user_states[user_id] = "waiting_for_address"
        
        await update.message.reply_text("3️⃣ Адрес доставки:")
        
    elif current_state == "waiting_for_address":
        # Сохраняем адрес и переходим к следующему шагу
        context.user_data['customer_address'] = message_text
        user_states[user_id] = "waiting_for_items"
        
        await update.message.reply_text("4️⃣ Список товаров для заказа (опишите что хотите купить):")
        
    elif current_state == "waiting_for_items":
        # Сохраняем список товаров и завершаем заказ
        context.user_data['order_items'] = message_text
        user_states[user_id] = None
        
        # Отправляем заказ в группу
        await send_order_to_group(update.effective_user, context.user_data)
        
        # Подтверждаем пользователю
        confirmation_text = f"""
✅ Заказ успешно оформлен!

📋 Детали заказа:
👤 Имя: {context.user_data['customer_name']}
📱 Телефон: {context.user_data['customer_phone']}
📍 Адрес: {context.user_data['customer_address']}
🛍️ Товары: {context.user_data['order_items']}

Наш менеджер свяжется с вами в ближайшее время для подтверждения заказа.
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text=confirmation_text, reply_markup=reply_markup)
        
        # Очищаем данные пользователя
        context.user_data.clear()

async def send_order_to_group(user, order_data):
    """Отправка заказа в группу"""
    try:
        order_message = f"""
🆕 НОВЫЙ ЗАКАЗ!

👤 Клиент: {order_data['customer_name']}
📱 Телефон: {order_data['customer_phone']}
📍 Адрес: {order_data['customer_address']}
🛍️ Товары: {order_data['order_items']}
⏰ Время заказа: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
🆔 ID пользователя: {user.id}
👤 Username: @{user.username if user.username else 'Не указан'}
"""
        
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=order_message,
            parse_mode='HTML'
        )
        
        logger.info(f"Заказ от пользователя {user.id} отправлен в группу")
        
    except Exception as e:
        logger.error(f"Ошибка при отправке заказа в группу: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
❓ Справка по использованию бота

📋 Доступные команды:
/start - Запуск бота и главное меню
/help - Показать эту справку

🔄 Как оформить заказ:
1. Нажмите "Оформить заказ"
2. Введите ваше имя
3. Введите номер телефона
4. Введите адрес доставки
5. Опишите товары для заказа

📞 Техническая поддержка:
• Email: support@example.com
• Телефон: +7 (999) 123-45-67
"""
    
    await update.message.reply_text(help_text)

def main() -> None:
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
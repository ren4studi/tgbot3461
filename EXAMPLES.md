# 📚 Примеры использования Telegram бота заказов

## 🎯 Основные сценарии

### 1. Пользователь заходит в бота

```
Пользователь: /start

Бот отвечает:
🤖 Добро пожаловать в бот для заказов!

👋 Привет, [Имя пользователя]!

Здесь вы можете:
• Вызвать техническую поддержку
• Оформить заказ на покупку товаров

Выберите нужный пункт из меню ниже:

[1️⃣ Вызов тех. поддержки] [2️⃣ Оформить заказ]
```

### 2. Вызов технической поддержки

```
Пользователь нажимает: 1️⃣ Вызов тех. поддержки

Бот отвечает:
🆘 Техническая поддержка

Для связи с технической поддержкой:
• Email: support@example.com
• Телефон: +7 (999) 123-45-67
• Время работы: Пн-Пт 9:00-18:00

Опишите вашу проблему, и мы свяжемся с вами в ближайшее время.

[🔙 Вернуться в меню]
```

### 3. Оформление заказа

#### Шаг 1: Имя
```
Пользователь нажимает: 2️⃣ Оформить заказ

Бот отвечает:
🛒 Оформление заказа

Для оформления заказа мне нужна следующая информация:

1️⃣ Ваше имя:

[🔙 Вернуться в меню]

Пользователь: Иван Иванов
```

#### Шаг 2: Телефон
```
Бот отвечает:
2️⃣ Ваш номер телефона:

Пользователь: +7 (999) 123-45-67
```

#### Шаг 3: Адрес
```
Бот отвечает:
3️⃣ Адрес доставки:

Пользователь: г. Москва, ул. Примерная, д. 1, кв. 5
```

#### Шаг 4: Товары
```
Бот отвечает:
4️⃣ Список товаров для заказа (опишите что хотите купить):

Пользователь: Хочу заказать ноутбук Dell Inspiron 15, черный цвет
```

#### Шаг 5: Подтверждение
```
Бот отвечает:
✅ Заказ успешно оформлен!

📋 Детали заказа:
👤 Имя: Иван Иванов
📱 Телефон: +7 (999) 123-45-67
📍 Адрес: г. Москва, ул. Примерная, д. 1, кв. 5
🛍️ Товары: Хочу заказать ноутбук Dell Inspiron 15, черный цвет

Наш менеджер свяжется с вами в ближайшее время для подтверждения заказа.

[🔙 Вернуться в меню]
```

### 4. Сообщение в группе

```
В группе появляется:
🆕 НОВЫЙ ЗАКАЗ!

👤 Клиент: Иван Иванов
📱 Телефон: +7 (999) 123-45-67
📍 Адрес: г. Москва, ул. Примерная, д. 1, кв. 5
🛍️ Товары: Хочу заказать ноутбук Dell Inspiron 15, черный цвет
⏰ Время заказа: 15.12.2024 14:30:25
🆔 ID пользователя: 123456789
👤 Username: @ivan_ivanov
```

## 🔧 Настройка для разных сценариев

### Настройка для интернет-магазина

```python
# В config.py измените:
SUPPORT_CONFIG = {
    'email': 'orders@yourstore.com',
    'phone': '+7 (800) 555-35-35',
    'working_hours': 'Ежедневно 8:00-22:00',
    'website': 'https://yourstore.com'
}

MESSAGES['order_success'] = """
✅ Заказ успешно оформлен!

📋 Детали заказа:
👤 Имя: {name}
📱 Телефон: {phone}
📍 Адрес: {address}
🛍️ Товары: {items}

💰 Стоимость будет рассчитана менеджером
🚚 Доставка: 1-3 рабочих дня
💳 Оплата: при получении или онлайн

Наш менеджер свяжется с вами в течение 30 минут!
"""
```

### Настройка для ресторана

```python
# В config.py измените:
MESSAGES['order_start'] = """
🍕 Оформление заказа

Для оформления заказа мне нужна следующая информация:

1️⃣ Ваше имя:
"""

MESSAGES['order_address'] = "3️⃣ Адрес доставки (или 'самовывоз'):"
MESSAGES['order_items'] = "4️⃣ Что хотите заказать (блюда, напитки):"

# Добавьте новые поля
ORDER_CONFIG['additional_fields'] = ['delivery_time', 'payment_method']
```

### Настройка для автосервиса

```python
# В config.py измените:
MESSAGES['order_start'] = """
🔧 Запись на обслуживание

Для записи мне нужна следующая информация:

1️⃣ Ваше имя:
"""

MESSAGES['order_items'] = "4️⃣ Какие работы нужны (ТО, ремонт, диагностика):"

# Добавьте поле для марки и модели авто
ORDER_CONFIG['additional_fields'] = ['car_brand', 'car_model', 'car_year']
```

## 🎨 Кастомизация интерфейса

### Изменение эмодзи

```python
# В config.py измените:
KEYBOARDS = {
    'main_menu': [
        ['🆘 Тех. поддержка', 'support'],
        ['🛒 Заказать', 'order']
    ],
    
    'back_menu': [
        ['⬅️ Назад', 'back_to_menu']
    ]
}
```

### Изменение цветов (для веб-версии)

```css
/* Если используете веб-интерфейс */
.bot-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
}

.bot-button:hover {
    background-color: #0056b3;
}
```

## 📱 Интеграция с другими сервисами

### Отправка в CRM

```python
# В bot.py добавьте:
async def send_to_crm(order_data):
    """Отправка заказа в CRM систему"""
    import requests
    
    crm_data = {
        'customer_name': order_data['customer_name'],
        'customer_phone': order_data['customer_phone'],
        'customer_address': order_data['customer_address'],
        'order_items': order_data['order_items'],
        'source': 'telegram_bot',
        'timestamp': datetime.now().isoformat()
    }
    
    response = requests.post(
        'https://your-crm.com/api/orders',
        json=crm_data,
        headers={'Authorization': 'Bearer YOUR_API_KEY'}
    )
    
    return response.status_code == 200
```

### Отправка в Excel

```python
# В bot.py добавьте:
async def save_to_excel(order_data):
    """Сохранение заказа в Excel файл"""
    import pandas as pd
    from datetime import datetime
    
    # Создаем DataFrame
    df = pd.DataFrame([{
        'Дата': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        'Имя': order_data['customer_name'],
        'Телефон': order_data['customer_phone'],
        'Адрес': order_data['customer_address'],
        'Товары': order_data['order_items']
    }])
    
    # Сохраняем в Excel
    filename = f'orders_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    try:
        # Пытаемся добавить к существующему файлу
        existing_df = pd.read_excel(filename)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(filename, index=False)
    except FileNotFoundError:
        # Создаем новый файл
        df.to_excel(filename, index=False)
    
    return filename
```

## 🚀 Расширенные возможности

### Многоязычность

```python
# В config.py добавьте:
LANGUAGES = {
    'ru': {
        'welcome': 'Добро пожаловать в бот для заказов!',
        'support': 'Техническая поддержка',
        'order': 'Оформить заказ'
    },
    'en': {
        'welcome': 'Welcome to the order bot!',
        'support': 'Technical Support',
        'order': 'Place Order'
    }
}

# В bot.py добавьте:
async def detect_language(user):
    """Определение языка пользователя"""
    if user.language_code in LANGUAGES:
        return user.language_code
    return 'ru'  # По умолчанию русский
```

### Статистика заказов

```python
# В bot.py добавьте:
from collections import defaultdict
import json

# Глобальная статистика
order_stats = defaultdict(int)

async def update_stats(order_data):
    """Обновление статистики заказов"""
    order_stats['total_orders'] += 1
    order_stats['today_orders'] += 1
    
    # Сохраняем в файл
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(dict(order_stats), f, ensure_ascii=False, indent=2)

async def get_stats():
    """Получение статистики"""
    return dict(order_stats)
```

## 🔒 Безопасность

### Валидация данных

```python
# В bot.py добавьте:
import re

def validate_phone(phone):
    """Валидация номера телефона"""
    pattern = r'^[\+]?[0-9\s\-\(\)]{10,20}$'
    return re.match(pattern, phone) is not None

def validate_name(name):
    """Валидация имени"""
    return 2 <= len(name) <= 100 and name.replace(' ', '').isalpha()

# Используйте в handle_message:
if current_state == "waiting_for_phone":
    if not validate_phone(message_text):
        await update.message.reply_text(
            "❌ Неверный формат номера телефона. Попробуйте еще раз:"
        )
        return
```

### Антиспам защита

```python
# В bot.py добавьте:
from datetime import datetime, timedelta

# Словарь для отслеживания активности пользователей
user_activity = {}

def is_spam(user_id):
    """Проверка на спам"""
    now = datetime.now()
    
    if user_id not in user_activity:
        user_activity[user_id] = []
    
    # Удаляем старые записи (старше 1 минуты)
    user_activity[user_id] = [
        time for time in user_activity[user_id] 
        if now - time < timedelta(minutes=1)
    ]
    
    # Добавляем текущее время
    user_activity[user_id].append(now)
    
    # Если больше 5 сообщений в минуту - это спам
    return len(user_activity[user_id]) > 5

# Используйте в handle_message:
if is_spam(user_id):
    await update.message.reply_text(
        "⚠️ Слишком много сообщений. Подождите немного."
    )
    return
```

## 📊 Мониторинг и аналитика

### Логирование действий

```python
# В bot.py добавьте:
import logging.handlers

# Настройка ротации логов
handler = logging.handlers.RotatingFileHandler(
    'logs/bot.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(handler)

# Логируем все действия
async def log_user_action(user_id, action, details=None):
    """Логирование действий пользователя"""
    log_message = f"User {user_id}: {action}"
    if details:
        log_message += f" - {details}"
    logger.info(log_message)

# Используйте в функциях:
await log_user_action(user_id, "started_order")
await log_user_action(user_id, "completed_order", f"Items: {order_items}")
```

### Уведомления администраторам

```python
# В bot.py добавьте:
async def notify_admins(message, order_data=None):
    """Уведомление администраторов"""
    admin_ids = [123456789, 987654321]  # ID администраторов
    
    for admin_id in admin_ids:
        try:
            if order_data:
                # Форматируем сообщение с данными заказа
                formatted_message = message.format(**order_data)
            else:
                formatted_message = message
                
            await context.bot.send_message(
                chat_id=admin_id,
                text=formatted_message
            )
        except Exception as e:
            logger.error(f"Не удалось уведомить админа {admin_id}: {e}")

# Используйте для важных событий:
await notify_admins("🚨 Новый заказ от пользователя {customer_name}!")
await notify_admins("⚠️ Бот перезапущен")
```

Эти примеры помогут вам настроить бота под ваши конкретные потребности и расширить его функциональность!
#!/usr/bin/env python3
"""
Скрипт для получения ID группы в Telegram.
Добавьте бота в группу и запустите этот скрипт.
"""

import os
from dotenv import load_dotenv
from telegram import Bot

# Загружаем переменные окружения
load_dotenv()

async def get_group_id():
    """Получает ID группы, где находится бот"""
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ Ошибка: BOT_TOKEN не найден в .env файле")
        return
    
    bot = Bot(token=bot_token)
    
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"🤖 Бот: @{bot_info.username}")
        print(f"📝 Имя: {bot_info.first_name}")
        print()
        print("📋 Инструкция:")
        print("1. Добавьте бота в группу")
        print("2. Отправьте любое сообщение в группу")
        print("3. Запустите бота командой /start")
        print("4. Скопируйте ID группы из сообщения бота")
        print()
        print("💡 Альтернативный способ:")
        print("1. Добавьте бота в группу")
        print("2. Отправьте сообщение в группу")
        print("3. Перейдите по ссылке:")
        print(f"   https://api.telegram.org/bot{bot_token}/getUpdates")
        print("4. Найдите 'chat' -> 'id' в ответе")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_group_id())
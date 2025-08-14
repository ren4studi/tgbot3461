#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности бота.
Запускает бота в тестовом режиме.
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Загружаем переменные окружения
load_dotenv()

async def test_bot():
    """Тестирует основные функции бота"""
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ Ошибка: BOT_TOKEN не найден в .env файле")
        print("Создайте .env файл на основе .env.example")
        return False
    
    try:
        bot = Bot(token=bot_token)
        
        # Тестируем подключение к API
        print("🔍 Тестирование подключения к Telegram API...")
        bot_info = await bot.get_me()
        print(f"✅ Бот подключен: @{bot_info.username}")
        print(f"📝 Имя: {bot_info.first_name}")
        print(f"🆔 ID: {bot_info.id}")
        
        # Проверяем переменные окружения
        print("\n🔧 Проверка настроек...")
        group_id = os.getenv('GROUP_ID')
        if group_id:
            print(f"✅ GROUP_ID: {group_id}")
        else:
            print("❌ GROUP_ID не найден в .env файле")
            print("Добавьте GROUP_ID для отправки заказов в группу")
        
        print("\n🎯 Тестирование завершено!")
        print("Теперь вы можете запустить бота командой: python bot.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\n🔧 Возможные решения:")
        print("1. Проверьте правильность токена")
        print("2. Убедитесь, что у вас есть доступ к интернету")
        print("3. Проверьте, что бот не заблокирован")
        return False
        
    finally:
        await bot.close()

def check_dependencies():
    """Проверяет установленные зависимости"""
    print("📦 Проверка зависимостей...")
    
    try:
        import telegram
        print(f"✅ python-telegram-bot: {telegram.__version__}")
    except ImportError:
        print("❌ python-telegram-bot не установлен")
        print("Установите: pip install -r requirements.txt")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv установлен")
    except ImportError:
        print("❌ python-dotenv не установлен")
        print("Установите: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование Telegram бота для заказов")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        return
    
    print()
    
    # Тестируем бота
    success = asyncio.run(test_bot())
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Все тесты пройдены! Бот готов к запуску.")
        print("\n📱 Следующие шаги:")
        print("1. Создайте группу в Telegram")
        print("2. Добавьте бота в группу")
        print("3. Получите ID группы")
        print("4. Обновите GROUP_ID в .env файле")
        print("5. Запустите бота: python bot.py")
    else:
        print("❌ Тесты не пройдены. Исправьте ошибки и попробуйте снова.")

if __name__ == "__main__":
    main()
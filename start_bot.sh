#!/bin/bash

# Скрипт для запуска Telegram бота в фоновом режиме

echo "🤖 Запуск Telegram бота для заказов..."

# Проверяем существование .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте .env файл на основе .env.example"
    echo "cp .env.example .env"
    exit 1
fi

# Проверяем установку Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен!"
    exit 1
fi

# Проверяем установку зависимостей
echo "📦 Проверка зависимостей..."
if ! python3 -c "import telegram" &> /dev/null; then
    echo "❌ Зависимости не установлены!"
    echo "Установите: pip install -r requirements.txt"
    exit 1
fi

# Создаем директорию для логов если её нет
mkdir -p logs

# Запускаем бота в фоновом режиме
echo "🚀 Запуск бота..."
nohup python3 bot.py > logs/bot.log 2>&1 &

# Получаем PID процесса
BOT_PID=$!
echo "✅ Бот запущен с PID: $BOT_PID"

# Сохраняем PID в файл для остановки
echo $BOT_PID > bot.pid

echo "📝 Логи сохраняются в logs/bot.log"
echo "🛑 Для остановки бота выполните: ./stop_bot.sh"
echo "📊 Для просмотра статуса: ps aux | grep bot.py"

# Ждем немного и проверяем статус
sleep 2
if ps -p $BOT_PID > /dev/null; then
    echo "🎉 Бот успешно запущен и работает!"
else
    echo "❌ Ошибка запуска бота. Проверьте логи: logs/bot.log"
    exit 1
fi
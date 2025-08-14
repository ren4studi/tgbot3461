#!/bin/bash

# Скрипт для остановки Telegram бота

echo "🛑 Остановка Telegram бота..."

# Проверяем существование файла с PID
if [ ! -f bot.pid ]; then
    echo "❌ Файл bot.pid не найден!"
    echo "Бот может быть не запущен или запущен другим способом"
    
    # Пытаемся найти процесс по имени
    BOT_PROCESSES=$(ps aux | grep "python3 bot.py" | grep -v grep)
    if [ -n "$BOT_PROCESSES" ]; then
        echo "🔍 Найдены процессы бота:"
        echo "$BOT_PROCESSES"
        echo ""
        echo "Для принудительной остановки выполните:"
        echo "pkill -f 'python3 bot.py'"
    else
        echo "✅ Бот не запущен"
    fi
    exit 1
fi

# Читаем PID из файла
BOT_PID=$(cat bot.pid)

# Проверяем существование процесса
if ! ps -p $BOT_PID > /dev/null; then
    echo "❌ Процесс с PID $BOT_PID не найден"
    echo "Удаляю файл bot.pid..."
    rm -f bot.pid
    exit 1
fi

# Останавливаем процесс
echo "🔄 Остановка процесса с PID: $BOT_PID..."
kill $BOT_PID

# Ждем завершения процесса
sleep 2

# Проверяем статус
if ps -p $BOT_PID > /dev/null; then
    echo "⚠️ Процесс не остановился, принудительно завершаю..."
    kill -9 $BOT_PID
    sleep 1
fi

# Проверяем финальный статус
if ps -p $BOT_PID > /dev/null; then
    echo "❌ Не удалось остановить процесс"
    exit 1
else
    echo "✅ Бот успешно остановлен"
    # Удаляем файл с PID
    rm -f bot.pid
    echo "🗑️ Файл bot.pid удален"
fi

echo "🎯 Бот остановлен. Для запуска выполните: ./start_bot.sh"
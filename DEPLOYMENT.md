# 🚀 Развертывание Telegram бота на сервере

## 📋 Требования к серверу

### Минимальные требования
- **ОС**: Ubuntu 18.04+ / CentOS 7+ / Debian 9+
- **RAM**: 512 MB
- **CPU**: 1 ядро
- **Диск**: 10 GB
- **Python**: 3.7+

### Рекомендуемые требования
- **ОС**: Ubuntu 20.04 LTS
- **RAM**: 1 GB
- **CPU**: 2 ядра
- **Диск**: 20 GB
- **Python**: 3.9+

## 🔧 Подготовка сервера

### 1. Обновление системы

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. Установка Python и pip

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv -y

# CentOS/RHEL
sudo yum install python3 python3-pip -y
```

### 3. Создание пользователя для бота

```bash
# Создаем пользователя
sudo useradd -m -s /bin/bash botuser
sudo passwd botuser

# Добавляем в группу sudo (Ubuntu/Debian)
sudo usermod -aG sudo botuser

# Или в группу wheel (CentOS/RHEL)
sudo usermod -aG wheel botuser

# Переключаемся на пользователя
su - botuser
```

## 📥 Установка бота

### 1. Клонирование репозитория

```bash
# Переходим в домашнюю директорию
cd ~

# Клонируем репозиторий (замените на ваш URL)
git clone https://github.com/yourusername/telegram-order-bot.git
cd telegram-order-bot

# Или загружаем файлы вручную
wget https://github.com/yourusername/telegram-order-bot/archive/main.zip
unzip main.zip
cd telegram-order-bot-main
```

### 2. Создание виртуального окружения

```bash
# Создаем виртуальное окружение
python3 -m venv venv

# Активируем его
source venv/bin/activate

# Обновляем pip
pip install --upgrade pip
```

### 3. Установка зависимостей

```bash
# Устанавливаем зависимости
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

```bash
# Копируем пример файла
cp .env.example .env

# Редактируем файл
nano .env
```

Содержимое `.env` файла:
```env
BOT_TOKEN=ваш_токен_бота
GROUP_ID=-1001234567890
```

## 🏃‍♂️ Запуск бота

### 1. Тестовый запуск

```bash
# Активируем виртуальное окружение
source venv/bin/activate

# Тестируем бота
python test_bot.py

# Если все хорошо, запускаем
python bot.py
```

### 2. Запуск в фоновом режиме

```bash
# Делаем скрипты исполняемыми
chmod +x start_bot.sh stop_bot.sh

# Запускаем бота
./start_bot.sh

# Проверяем статус
ps aux | grep bot.py
```

## 🔄 Настройка автозапуска

### 1. Создание systemd сервиса

```bash
# Создаем файл сервиса
sudo nano /etc/systemd/system/telegram-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=Telegram Order Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/telegram-order-bot
Environment=PATH=/home/botuser/telegram-order-bot/venv/bin
ExecStart=/home/botuser/telegram-order-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Активация сервиса

```bash
# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable telegram-bot

# Запускаем сервис
sudo systemctl start telegram-bot

# Проверяем статус
sudo systemctl status telegram-bot
```

### 3. Управление сервисом

```bash
# Запуск
sudo systemctl start telegram-bot

# Остановка
sudo systemctl stop telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Просмотр логов
sudo journalctl -u telegram-bot -f
```

## 🌐 Настройка веб-хуков (опционально)

### 1. Установка Nginx

```bash
# Ubuntu/Debian
sudo apt install nginx -y

# CentOS/RHEL
sudo yum install nginx -y
```

### 2. Настройка SSL сертификата

```bash
# Устанавливаем Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получаем сертификат
sudo certbot --nginx -d yourdomain.com
```

### 3. Настройка Nginx

```bash
# Создаем конфигурацию
sudo nano /etc/nginx/sites-available/telegram-bot
```

Содержимое:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /webhook {
        proxy_pass http://127.0.0.1:8443;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Активация конфигурации

```bash
# Создаем символическую ссылку
sudo ln -s /etc/nginx/sites-available/telegram-bot /etc/nginx/sites-enabled/

# Проверяем конфигурацию
sudo nginx -t

# Перезапускаем Nginx
sudo systemctl restart nginx
```

### 5. Изменение бота для веб-хуков

В `bot.py` замените:
```python
# Вместо application.run_polling()
application.run_webhook(
    listen="127.0.0.1",
    port=8443,
    webhook_url="https://yourdomain.com/webhook"
)
```

## 📊 Мониторинг и логирование

### 1. Настройка ротации логов

```bash
# Создаем директорию для логов
mkdir -p logs

# Настраиваем logrotate
sudo nano /etc/logrotate.d/telegram-bot
```

Содержимое:
```
/home/botuser/telegram-order-bot/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 botuser botuser
    postrotate
        systemctl reload telegram-bot
    endscript
}
```

### 2. Мониторинг ресурсов

```bash
# Устанавливаем htop
sudo apt install htop -y

# Мониторим в реальном времени
htop

# Или используем встроенные команды
top
free -h
df -h
```

### 3. Настройка алертов

```bash
# Создаем скрипт для проверки
nano ~/check_bot.sh
```

Содержимое:
```bash
#!/bin/bash
if ! systemctl is-active --quiet telegram-bot; then
    echo "Бот не работает!" | mail -s "Алерт: Telegram бот упал" admin@yourdomain.com
    systemctl restart telegram-bot
fi
```

```bash
# Делаем исполняемым
chmod +x ~/check_bot.sh

# Добавляем в cron
crontab -e
# Добавляем строку:
*/5 * * * * ~/check_bot.sh
```

## 🔒 Безопасность

### 1. Настройка файрвола

```bash
# Ubuntu/Debian
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 2. Ограничение доступа к SSH

```bash
# Редактируем конфигурацию SSH
sudo nano /etc/ssh/sshd_config

# Изменяем порт (опционально)
Port 2222

# Отключаем root доступ
PermitRootLogin no

# Ограничиваем пользователей
AllowUsers botuser

# Перезапускаем SSH
sudo systemctl restart sshd
```

### 3. Регулярные обновления

```bash
# Создаем скрипт для обновлений
nano ~/update_system.sh
```

Содержимое:
```bash
#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

```bash
# Делаем исполняемым
chmod +x ~/update_system.sh

# Добавляем в cron (еженедельно)
crontab -e
# Добавляем строку:
0 2 * * 0 ~/update_system.sh
```

## 📱 Тестирование развертывания

### 1. Проверка работы бота

```bash
# Проверяем статус сервиса
sudo systemctl status telegram-bot

# Смотрим логи
sudo journalctl -u telegram-bot -n 50

# Проверяем процессы
ps aux | grep bot.py
```

### 2. Тестирование в Telegram

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Проверьте все функции
4. Убедитесь, что заказы приходят в группу

### 3. Проверка логов

```bash
# Смотрим логи бота
tail -f logs/bot.log

# Смотрим системные логи
sudo journalctl -u telegram-bot -f
```

## 🚨 Устранение неполадок

### Бот не запускается

```bash
# Проверяем статус
sudo systemctl status telegram-bot

# Смотрим логи
sudo journalctl -u telegram-bot -n 100

# Проверяем права доступа
ls -la /home/botuser/telegram-order-bot/

# Проверяем виртуальное окружение
source /home/botuser/telegram-order-bot/venv/bin/activate
python -c "import telegram; print('OK')"
```

### Проблемы с сетью

```bash
# Проверяем подключение к интернету
ping 8.8.8.8

# Проверяем DNS
nslookup api.telegram.org

# Проверяем порты
netstat -tlnp | grep :8443
```

### Проблемы с правами доступа

```bash
# Проверяем владельца файлов
sudo chown -R botuser:botuser /home/botuser/telegram-order-bot/

# Проверяем права
chmod +x /home/botuser/telegram-order-bot/*.sh
```

## 📈 Масштабирование

### 1. Балансировка нагрузки

Если у вас много пользователей, рассмотрите:
- Использование нескольких экземпляров бота
- Балансировщик нагрузки (HAProxy, Nginx)
- Кластер Redis для состояния

### 2. Мониторинг производительности

```bash
# Устанавливаем Prometheus и Grafana
# Или используйте простые инструменты:
sudo apt install sysstat -y
iostat -x 1
```

### 3. Автоматическое масштабирование

```bash
# Создаем скрипт для автоматического масштабирования
nano ~/scale_bot.sh
```

## 🎯 Готово!

После выполнения всех шагов у вас будет:
- ✅ Работающий Telegram бот
- ✅ Автозапуск при перезагрузке сервера
- ✅ Мониторинг и логирование
- ✅ Безопасность и обновления
- ✅ Возможность масштабирования

Бот будет автоматически принимать заказы и отправлять их в указанную группу!
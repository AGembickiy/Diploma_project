#!/bin/bash

echo "🚀 Запуск проекта MMORPG Board..."

# Функция для остановки всех процессов при выходе
cleanup() {
    echo "🛑 Останавливаю серверы..."
    pkill -f "python manage.py runserver"
    pkill -f "vite"
    exit 0
}

# Устанавливаем обработчик сигналов
trap cleanup SIGINT SIGTERM

# Запускаем backend
echo "📡 Запускаю Django backend..."
cd "Diploma_project/backend"
./run_server.sh &
BACKEND_PID=$!

# Ждем немного
sleep 2

# Запускаем frontend
echo "🎨 Запускаю Vue frontend..."
cd "../frontend"
./run_dev.sh &
FRONTEND_PID=$!

echo "✅ Проект запущен!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📧 Email ссылки теперь будут вести на правильный порт"
echo ""
echo "Нажмите Ctrl+C для остановки"

# Ждем завершения процессов
wait $BACKEND_PID $FRONTEND_PID

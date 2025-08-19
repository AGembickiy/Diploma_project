#!/bin/bash

# Активируем виртуальное окружение
source .venv/bin/activate

# Устанавливаем переменные окружения
export FRONTEND_URL=http://localhost:5173

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000

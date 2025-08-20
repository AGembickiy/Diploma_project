#!/bin/bash

# Скрипт для автоматического обновления портов во всех файлах проекта
# Загружаем конфигурацию из файла ports.env

if [ ! -f "config/ports.env" ]; then
    echo "❌ Файл config/ports.env не найден!"
    exit 1
fi

# Загружаем переменные из файла
source config/ports.env

echo "🔄 Обновляю порты в проекте..."
echo "📡 Backend: $HOST:$BACKEND_PORT"
echo "🎨 Frontend: $HOST:$FRONTEND_PORT"
echo "🔧 Frontend Alt: $HOST:$FRONTEND_PORT_ALT"

# Обновляем backend/run_server.sh
echo "📝 Обновляю backend/run_server.sh..."
sed -i "s/export FRONTEND_URL=http:\/\/localhost:[0-9]*/export FRONTEND_URL=http:\/\/$HOST:$FRONTEND_PORT/" backend/run_server.sh
sed -i "s/python manage.py runserver 0.0.0.0:[0-9]*/python manage.py runserver 0.0.0.0:$BACKEND_PORT/" backend/run_server.sh

# Обновляем frontend/run_dev.sh
echo "📝 Обновляю frontend/run_dev.sh..."
sed -i "s/--port [0-9]*/--port $FRONTEND_PORT_ALT/" frontend/run_dev.sh

# Обновляем frontend/vite.config.ts
echo "📝 Обновляю frontend/vite.config.ts..."
sed -i "s/port: [0-9]*/port: $FRONTEND_PORT/" frontend/vite.config.ts

# Обновляем backend/mmorpg_backend/settings.py
echo "📝 Обновляю backend/mmorpg_backend/settings.py..."
sed -i "s/http:\/\/localhost:[0-9]*/http:\/\/$HOST:$FRONTEND_PORT/g" backend/mmorpg_backend/settings.py
sed -i "s/http:\/\/127.0.0.1:[0-9]*/http:\/\/127.0.0.1:$FRONTEND_PORT/g" backend/mmorpg_backend/settings.py
sed -i "s/http:\/\/localhost:[0-9]*/http:\/\/$HOST:$FRONTEND_PORT_ALT/g" backend/mmorpg_backend/settings.py
sed -i "s/http:\/\/127.0.0.1:[0-9]*/http:\/\/127.0.0.1:$FRONTEND_PORT_ALT/g" backend/mmorpg_backend/settings.py

# Обновляем start_project.sh
echo "📝 Обновляю start_project.sh..."
sed -i "s/🌐 Frontend: http:\/\/localhost:[0-9]*/🌐 Frontend: http:\/\/$HOST:$FRONTEND_PORT/" start_project.sh
sed -i "s/🔧 Backend API: http:\/\/localhost:[0-9]*/🔧 Backend API: http:\/\/$HOST:$BACKEND_PORT/" start_project.sh

# Обновляем frontend файлы с хардкодом портов
echo "📝 Обновляю frontend файлы..."

# Создаем временный файл для замены
cat > temp_replace.py << 'EOF'
import os
import re

def replace_ports_in_file(file_path, backend_port, frontend_port):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем backend порты (любой порт)
    content = re.sub(r'http://localhost:[0-9]+/api', f'http://localhost:{backend_port}/api', content)
    content = re.sub(r'http://127.0.0.1:[0-9]+/api', f'http://127.0.0.1:{backend_port}/api', content)
    
    # Заменяем frontend порты (любой порт) - только если это не API
    content = re.sub(r'http://localhost:[0-9]+(?!.*api)', f'http://localhost:{frontend_port}', content)
    content = re.sub(r'http://127.0.0.1:[0-9]+(?!.*api)', f'http://127.0.0.1:{frontend_port}', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Список файлов для обновления
files_to_update = [
    'frontend/src/pages/TestAuth.vue',
    'frontend/src/pages/VerifyEmail.vue',
    'frontend/src/pages/Board.vue',
    'frontend/src/pages/Main.vue',
    'frontend/src/components/advertisement/AdvertisementCard.vue',
    'frontend/src/services/responses.ts',
    'frontend/src/stores/user.ts',
    'frontend/src/App.vue'
]

for file_path in files_to_update:
    replace_ports_in_file(file_path, os.environ.get('BACKEND_PORT', '8000'), os.environ.get('FRONTEND_PORT', '3001'))
EOF

# Запускаем Python скрипт для обновления frontend файлов
source config/ports.env
BACKEND_PORT=$BACKEND_PORT FRONTEND_PORT=$FRONTEND_PORT python3 temp_replace.py

# Удаляем временный файл
rm temp_replace.py

echo "✅ Портты обновлены во всех файлах!"
echo ""
echo "📋 Сводка изменений:"
echo "   Backend: $HOST:$BACKEND_PORT"
echo "   Frontend: $HOST:$FRONTEND_PORT"
echo "   Frontend Alt: $HOST:$FRONTEND_PORT_ALT"
echo ""
echo "🔄 Теперь можно перезапустить проект!"

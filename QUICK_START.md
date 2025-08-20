# 🚀 Быстрый запуск MMORPG Board

## ⚡ За 30 секунд

```bash
# 1. Клонировать проект
git clone <your-repo-url>
cd Diploma_project

# 2. Установить права на скрипты
chmod +x start_project.sh update_ports.sh

# 3. Запустить проект
./start_project.sh
```

**Готово!** 🎉

## 🌐 Доступ
- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000

## 🔧 Если что-то пошло не так

### Проблемы с портами
```bash
./update_ports.sh
```

### Перезапуск
```bash
# Остановить
pkill -f "python manage.py runserver"
pkill -f "vite"

# Запустить заново
./start_project.sh
```

### Проверка статуса
```bash
ps aux | grep -E "(python|vite)" | grep -v grep
```

## 📋 Что происходит при запуске

1. ✅ **Обновление портов** - автоматическая синхронизация всех файлов
2. ✅ **Запуск Django** - backend API сервер
3. ✅ **Запуск Vue** - frontend dev сервер
4. ✅ **Открытие браузера** - готово к работе!

## 💡 Полезные команды

```bash
# Просмотр логов backend
tail -f backend/logs/django.log

# Просмотр логов frontend
# Логи отображаются в терминале при запуске

# Проверка API
curl http://localhost:8000/api/advertisements/public_advertisements/

# Проверка frontend
curl http://localhost:5173
```

---

**Нужна подробная документация?** Смотрите [README.md](README.md)

# Medusa E-commerce AQA Framework

Автоматизированное тестирование API для [Medusa](https://medusajs.com/) e-commerce платформы.

## 🚀 Возможности

- ✅ API тесты с использованием Playwright
- 📊 Allure отчёты с автоматической публикацией на GitHub Pages
- 🤖 Уведомления в Telegram о результатах тестов
- ⚙️ CI/CD через GitHub Actions (запуск по расписанию и при пуше)

## 📋 Требования

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15

## 🛠️ Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/ВАШ_USERNAME/ВАШ_РЕПО.git
cd ВАШ_РЕПО
pip install -r requirements.txt
playwright install chromium
BASE_API_URL=http://localhost:9000
BASE_ADMIN_URL=http://localhost:9000/app
BASE_STOREFRONT_URL=http://localhost:8000

ADMIN_EMAIL=admin@medusa-test.com
ADMIN_PASSWORD=supersecret

# Клонируй Medusa backend
git clone https://github.com/medusajs/medusa-starter-default backend
cd backend

# Установи зависимости
npm install

# Подними PostgreSQL и Redis через Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15
docker run -d -p 6379:6379 redis:alpine

# Настрой переменные
export DATABASE_URL=postgres://postgres:postgres@localhost:5432/medusa
export REDIS_URL=redis://localhost:6379

# Миграции и создание админа
npx medusa db:migrate
npx medusa user -e admin@medusa-test.com -p supersecret

# Запусти Medusa
npx medusa develop

# Все API тесты
pytest tests/api/ -v

# С Allure отчётом
pytest tests/api/ -v --alluredir=allure-results
allure serve allure-results

📊 Отчёты
Allure отчёты публикуются автоматически на GitHub Pages:
https://ВАШ_USERNAME.github.io/ВАШ_РЕПО/

🔔 Настройка Telegram уведомлений
Создай бота через @BotFather
Получи chat_id через @userinfobot
Добавь в GitHub Secrets:
TELEGRAM_TOKEN — токен бота
TELEGRAM_TO — твой chat_id
Settings → Secrets and variables → Actions → New repository secret

🏗️ Технологии
Python 3.11 — язык тестов
Pytest — фреймворк тестирования
Playwright — API клиент
Allure — отчёты
GitHub Actions — CI/CD
Medusa v2 — тестируемая платформа


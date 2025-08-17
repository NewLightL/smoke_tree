# "SMOKE TREE" BOT

## Возможности

- Каталог товаров
- Добавление товаров через админку
- Создание заказов

## Установка

1. Клонируйте репрозиторий

   ```bash
   git clone https://github.com/NewLightL/smooke_tree_bot
   ```

2. Установите зависимости

   ```python
   pip install -r requirements.txt
   ```

3. Создайте файл .env и добавьте все необходимые переменные, записаные в app/core/config.py

4. Запустите FastAPI командой, предварительно создав и активировав окружение

   - **Для разработки**

     ```bash
     uvicorn app.main:fastapi_app
     ```

   - **Для продакшена** (только на unix-подобных)

     ```bash
     gunicorn app.main:fastapi_app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --timeout 120
     ```

   - **Пример использования с docker**

     ```dockerfile
     CMD [ "gunicorn", "app.main:fastapi_app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000", "--timeout", "120" ]
     ```

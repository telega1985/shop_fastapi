Интернет-магазин на FastAPI

<h1>Доступный функционал</h1>

1. SQLadmin + fastapi_storages для загрузки фотографий через admin-панель
2. Разработка корзины. Для временного хранения товаров используется Redis
3. Разработка купонной системы (скидка на общую стоимость товаров в корзине)
4. Реализация создания заказов после добавления товаров в корзину
5. Отправка письма на почту о подтверждении заказа перед оплатой
6. Реализация системы управления пользователями в административной панели, включая создание новых пользователей и их аутентификацию
7. Реализация фильтров для самих продуктов по категориям
8. Разработка рекомендуемых товаров (после добавления товара в корзину, появляются дополнительные товары, которые можно купить)
9. Реализация отзывов для каждого товара с загрузкой фотографии пользователя (любой пользователь может оставить отзыв, также есть возможность отвечать этому пользователю)
10. Реализация front-end части на Jinja2Templates
11. Для надежного хранения данных в проекте используется PostgreSQL, обеспечивающая высокую производительность и расширяемость. Все запросы к базе данных выполняются асинхронно

<h2>Локальный запуск проекта</h2>

Предварительно необходимо установить Docker и Redis для вашей системы

Склонировать репозиторий:

    git clone <название репозитория>

Cоздать и активировать виртуальное окружение:

Команды для установки виртуального окружения на Mac или Linux:

    python3 -m venv env
    source env/bin/activate
    
Команды для Windows:

    python -m venv venv
    source venv/Scripts/activate

Создать файл .env по образцу:

    cp .env-docker-example
    
Установить зависимости из файла requirements.txt:

    cd ..
    pip install -r requirements.txt
    
Для создания миграций выполнить команду:

    alembic init migrations

В папку migrations в env файл вставьте следующий код:

    import sys
    from logging.config import fileConfig
    from os.path import abspath, dirname
    
    from sqlalchemy import engine_from_config
    from sqlalchemy import pool
    
    from alembic import context
    
    sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
    
    from app.database import Base, DATABASE_URL
    from app.products.models import Categories, Products
    from app.orders.models import Order, OrderItem
    from app.coupons.models import Coupon
    from app.users.models import User
    from app.reviews.models import Review, ImageReview
    
    config = context.config
    
    config.set_main_option("sqlalchemy.url", f"{DATABASE_URL}?async_fallback=True")
    
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)
    
    target_metadata = Base.metadata

Инициализировать БД:

    alembic revision --autogenerate -m "comment"   
    
Применить миграцию:

    alembic upgrade head 
    
Запустить проект:

    uvicorn app.main:app --reload
    
<h2>Запуск в контейнерах Docker</h2>

Находясь в главной директории проекта:

Запустить проект:

    docker-compose up -d --build  
    
Перед тем, как зайти в admin-панель, нужно зарегистрировать пользователя:

    POST /auth/register

<h2>Документация:</h2>

    Frontend: http://localhost:7777/api/v1/pages
    Backend: http://localhost:7777/api/v1/docs/

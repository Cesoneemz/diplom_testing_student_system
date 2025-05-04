from app.models import User
from app.security import hash_password
from app.database import db_helper
from app.utils import generate_username
import uuid

# Создаём сессию для работы с базой данных
async def create_super_user():
    async for session in db_helper.session_getter():
        # Примерные данные для нового пользователя
        user_data = {
            "email": "admin@admin.com",
            "first_name": "Данила",
            "middle_name": "Витальевич",
            "last_name": "Гусаков",
            "password": "securePassword123",
            "role": "admin",  # role = teacher
        }

        # Генерация username
        username = generate_username(user_data['first_name'], user_data['middle_name'], user_data['last_name'])

        # Создание нового пользователя
        new_user = User(
            id=str(uuid.uuid4()),  # Используем UUID для уникального ID
            email=user_data["email"],
            username=username,
            first_name=user_data["first_name"],
            middle_name=user_data["middle_name"],
            last_name=user_data["last_name"],
            password_hash=hash_password(user_data["password"]),
            role=user_data["role"]
        )

        # Добавление пользователя в сессию и коммит в базу данных
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        print(f"Пользователь {new_user.username} успешно создан с ID: {new_user.id}")

# Запуск асинхронной функции
import asyncio
asyncio.run(create_super_user())

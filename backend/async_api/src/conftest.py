"""
Используется для выполнения кода перед запуском тестов, в этом
случае мы хотим использовать тестовую базу данных.

Поместителюбой код, связанный с Pytest (он будет выполнен перед `src/tests/...`)
"""

import os

os.environ[
    "URL_DATABASE"
] = "postgresql+asyncpg://postgres:postgres@192.168.1.3:5432/test_handbook"

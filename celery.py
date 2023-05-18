# import os
# from celery import Celery

# # Установка переменной окружения для настроек Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# # Создание экземпляра Celery
# app = Celery('main')

# # Загрузка настроек Celery из настроек Django
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Автоматическое обнаружение и регистрация задач из файлов tasks.py
# app.autodiscover_tasks()
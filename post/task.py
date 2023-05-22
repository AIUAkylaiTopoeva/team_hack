from celery import shared_task

@shared_task
def some_func():
    print("Это функция, которую будет выполнять celery")
# Проект "Судебный процесс"




Небольшой проект бекэнд django фронт html. Создание карточек по делам разных категорий, добавление сторон по делу, движения дела, ходатайств. Проект всего лишь скелет карточки по судебному делу любой категории.



## Установка/запуск проекта



```sh
pip install -r requirements.txt
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py loading_csv
python manage.py runserver
```

```sh
127.0.0.1:8000
```


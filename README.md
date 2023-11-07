# Проект "Судебный процесс"




Небольшой проект бекэнд django фронт html. Создание карточек по делам разных категорий, добавление сторон по делу, движения дела, ходатайств. Проект всего лишь скелет карточки по судебному делу любой категории.



## Установка/запуск проекта

```sh
python.exe -m pip install --upgrade pip
```
```sh
pip install -r requirements.txt
```
```sh
python manage.py createsuperuser
```
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```
Загрузка данных
```sh
python manage.py loading_csv
```
```sh
python manage.py runserver
```

```sh
127.0.0.1:8000
```


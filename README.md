# Quizzer app
The application can be used to create and run small tests and surveys.

## Features:
- Users can take part in existing polls and create their own
- Users can post comments under questions.
- User registration on the site and via facebook, linkedin is supported
- Sorting quizzes by name and creation date is supported
- Supports search on existing polls

## Run local server:
`python manage.py runserver localhost:8000`

### Before start
App used **python 3.7+** and **Django 2.2.13**.

#### Requirements:
To install the dependencies, type in the console:
`pip install -r requirements.txt`

#### Apply migrations and load initial data with fixtures
```
python manage.py migrate
python manage.py loaddata --format=json fixtures/initial_data.json
```

#### Test user admin:
- login: admin
- pass: admin
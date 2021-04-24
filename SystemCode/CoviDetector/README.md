# Django Multipage Form Demo

This is a prject to predict covid from sympthons

## System Requirements

Python 3
django

## Installation

Create and activate a python 3 virtual environment, and `pip install`
from the requirements file:

```bash
(py36) $ conda create --name py36 python=3.6
(py36) $ conda activate py36
(py36) $ pip install -r requirements.txt
(py36) $ python -m spacy download en
```

This should install Django (the only requirement).

## Configuration

Run migrations:

```bash
(py36) $ python manage.py makemigrations
(py36) $ python manage.py migrate
```

## Use

### Front-end

You should now be able to run the project with Django's built-in
`runserver` command on port 8000 (or any available port).

```bash
(py36) $ python manage.py runserver 8000
```

You should then be able to use the app in your browser at
`localhost:8000`.  Fill in form fields with test data and click the
"Continue" button until the form is complete.

### Back-end

You should also be able to log into the admin at
`localhost:8000/admin`.

Use the username "admin" and the password "admin" to log in as a
superuser that was created when migrations were run.  Form submissions
should appear in the admin under the "Job Application" app.

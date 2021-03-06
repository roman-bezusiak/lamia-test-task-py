# lamia-test-task-py

This API is currently available and running on [Heroku](https://lamia-py-api.herokuapp.com/) (as of 2020.12.05).

## Operating instructions

In order to run the project locally use:

```bash
pwd
"/.../project-root/"
cd api_server
python3 -m venv env
source env/bin/activate
pip install -r ../requirements.txt
python manage.py runserver
```

## Platform

This project and its dependencies are supported on **Ubuntu** and **Heroku VM**.

## Stack

- Django
- Gunicorn

## Environment variables

| Name                        | Description                                               |
| --------------------------- | --------------------------------------------------------- |
| **`CSRF_COOKIE_SECURE`**    | `True` to enable                                          |
| **`DEBUG`**                 | `True` to enable                                          |
| **`DISABLE_COLLECTSTATIC`** | `1` (this is only required, when deploying to **Heroku**) |
| **`OMDB_API_TOKEN`**        | OMBb API token                                            |
| **`OMDB_API_URL`**          | OMBb API URL                                              |
| **`OPENLIB_ISBN_API_URL`**  | OpenLibrary API URL                                       |
| **`SECRET_KEY`**            | Django secret key                                         |
| **`SESSION_COOKIE_SECURE`** | `True` to enable                                          |

## API

| Route           | Type | Description    |
| --------------- | ---- | -------------- |
| **`/getBook`**  | API  | Book data API  |
| **`/getMovie`** | API  | Movie data API |

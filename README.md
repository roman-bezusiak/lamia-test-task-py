# lamia-test-task-py

This client is currently available and running on [Heroku](https://lamia-py-api.herokuapp.com/) (as of 2020.12.05).

## Stack

- Django
- Gunicorn

## Environmant variables

| Name                        | Description         |
| --------------------------- | ------------------- |
| **`SECRET_KEY`**            | Django secret key   |
| **`DEBUG`**                 | `True` to enable    |
| **`OMDB_API_TOKEN`**        | OMBb API token      |
| **`OMDB_API_URL`**          | OMBb API URL        |
| **`OPENLIB_ISBN_API_URL`**  | OpenLibrary API URL |
| **`CSRF_COOKIE_SECURE`**    | `True` to enable    |
| **`SESSION_COOKIE_SECURE`** | `True` to enable    |

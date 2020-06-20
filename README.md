# django-drf-user-api

## Installation

### Development

Uses the default Django development server.

1. Update the environment variables in the *docker-compose.yml* file if you need.
2. Build the images and run the containers:

    ```sh
    docker-compose down -v --rmi all --remove-orphans  # if built before!
    docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "django_drf_user_api" folder is mounted into the container and your code changes apply automatically.

### Code Styling

#### Flake8 and Black with pre-commit

1. Installation:
 - with pip
    ```sh
    pip install pre-commit
    pre-commit install
    ```
 - with brew on OsX
    ```sh
    brew install pre-commit
    pre-commit install
    ```
2. Usage:
 - Just commit :)

### Tests

1. General:
```sh
docker-compose exec django-drf-user-api-web python manage.py test
```

2. App Based:
```sh
docker-compose exec django-drf-user-api-web python manage.py test {APP_NAME}
```

### API

1. Document Path: {DOMAIN}/users/docs/
2. API Path: {DOMAIN}/users/

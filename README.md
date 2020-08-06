# POSTGIS Test Case

1. git clone https://github.com/NickiHell/some-postgis-test-case.git
2. cd some-postgis-test-case
3. cp .env.example .env
4. cp docker-compose.prod.yml docker-compose.yml
5. docker-compose up -d --build
6. docker-compose exec app pipenv run pytest

http://0.0.0.0:8080 - API, Swagger схема
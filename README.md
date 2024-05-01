## PyBooking
Пример монолитного сервиса бронирования на FastApi.

## Технологии
- [FastApi](https://github.com/tiangolo/fastapi) - создание API-сервера.
- [Pydentic](https://github.com/pydantic/pydantic) - валидация данных.
- [Uvicorn](https://github.com/encode/uvicorn) - сервер с протоколом ASGI.
- [SqlAlchemy](https://github.com/sqlalchemy/sqlalchemy) - ORM для работы с базой данных.
- [Alembic](https://github.com/sqlalchemy/alembic) - управление миграциями БД.
- [fastapi-cache](https://github.com/long2ice/fastapi-cache) - кэширование запросов.
- [Celery](https://github.com/celery/celery) - создание очереди задач.
- [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) - отображение HTML-шаблонов.
<br></br>
- [PostgresSQL](https://www.postgresql.org/) - хранение данных.
- [Redis](https://redis.io/) - используется в качестве брокера сообщений и для кэширования.

## Запуск проекта на MAC OS M1

#### 1) Клонирование проекта:
```
git clone git clone git@github.com:justyfay/pybooking.git
```
#### 2) Добавление `prod.env` файла. Минимальная конфигурация:
```
MODE=Dev # Если нет необходимости запускать тесты, оставить как есть. В противном случае установить значение "Test".
LOG_LEVEL=INFO # Уровень логирования для сервиса pybooking. Возможные значения: INFO, DEBUG.

# Креды для подключения к postgres
DB_HOST={db_host}
DB_PORT={db_port}
DB_NAME={db_name}
DB_USER={db_user}
DB_PASS={db_pass}

SECRET_KEY={you_secret_key} # Ключ для создания подписи
ALGORITHM={you_algorithm} # Алгоритм шифрования

# Креды для подключения к PgAdmin
PG_LOGIN={you_pg_admin_login}
PG_PASSWORD={you_pg_admin_password}

# Креды для подключения к Redis
REDIS_HOST={you_redis_host}
REDIS_PORT={you_redis_port}

SENTRY_DSN={you_sentry_dsn_url} # Требуется зарегестрироваться в https://sentry.io/ и создать проект.

BASE_URL={your_url} # Адрес, по которому будет доступно приложение. Например http://localhost:9000
ORIGINS='["{you_origin_1}", "{you_origin_2}", ...]' # Источники, которым разрешен доступ
```
- Если нет желания добавлять **Sentry**, можно закомментировать переменную окружения `SENTRY_DSN` в `prod.env` и `config.py`,
а так же в `main.py` закомментировать функцию `sentry_sdk.init()`.

- Для запуска тестов нужно добавить в `prod.env` креды для подключения к тестовой базе:
```
TEST_DB_HOST={db_test_host}
TEST_DB_PORT={db_test_port}
TEST_DB_NAME={db_test_name}
TEST_DB_USER={db_test_user}
TEST_DB_PASS={db_test_pass}
```
- Для того, что бы работала отправка уведомлений, нужно создать приложение https://myaccount.google.com/apppasswords
(требуется подключение двухэтапной аутентификации в **Google** аккаунте) и добавить в `prod.env` соответствующие переменные:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER={your_gmail_address} # Адрес электронный почты
SMTP_PASSWORD='{your_gmail_application_password}' # Пароль, выданный при создании приложения
```

- Без настроенного **SMTP** будут падать ошибки связанные с `celery.task`.

#### 3) Запуск в Docker:
```
docker build .
```
```
docker-compose --env-file prod.env up
```

#### 4) Загрузка дампа базы:
```
cat src/migration/pybooking.sql | docker exec -i postgres_db psql -U {db_user}
```
В целом, основная настройка на этом завершена. Можно попробовать перейти на адрес, где развернуто приложение:
<br>http://localhost:9000 - Сервис бронирования PyBooking.
<br>http://localhost:9000/docs - Документация. Для просмотра описания api в новом формате подставить `redoc` вместо `docs`.

#### 5) Добавление дашборда Grafana:
1) Для начала нужно перейти в **Prometheus** (url по умолчанию http://localhost:9090/)
2) С помощью верхнего меню перейти в раздел **Status** -> **Targets**.
3) Проверить, что Prometheus и PyBooking имеют _state_ **UP**.
4) Перейти в Grafana (url по умолчанию http://localhost:3000/). Авторизация под дефолтными кредами admin@admin.
5) В Grafana открыть вкладку **Connection** -> **Data Source**.
6) В открывшемся разделе нажать "**Add new data source**", в поле **Connection** ввести адрес **prometheus**
в докере http://prometheus:9090 и сохранить изменения.
7) Перейти на созданный source и в url скопировать uid источника.
Пример url'а: http://localhost:3000/connections/datasources/edit/adkescl8z6txcd где _adkescl8z6txcd_ - это нужный uid.
8) В файле **grafana-dashbord.json** в каждом словаре datasource заменить uid на свой из п.7:
```
    "datasource": {
            "type": "prometheus",
            "uid": "ddkelon63k4qoe" <- ваш uid
          }
```
9) Далее перейти в **Dashboards** -> **New** -> **Import Dashboard** и импортировать файл **grafana-dashbord.json**.
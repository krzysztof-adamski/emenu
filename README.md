# emenu

***

Aplikacja prezentuje `posiłki` zawarte w `menu`

* możliwość tworzenia `menu`
* możliwość dodawnia `posiłku` do `menu`
* edycja, usuwanie `menu` i `posiłku` tylko dla zalogowanego użytkownika
* cykliczne powiadamianie użytkowników o nowych posiłkach i ostatnio zmodyfikowanych: każdego dnia o godz. 10:00
* obługa aplikacji przy wykorzystaniu API Rest Level 3
* uruchomienie aplikacji w środowisku `docker`, z bazą danych `postgres`,
* dokumentacja api z wykożystaniem `swagger` i `redoc`
* pokrycie kodu testami na poziomie `98%`

## Instalacja i uruchomienie

Wymagany jest plik zmiennych środowiskowych `.env`

```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=emenu
POSTGRES_HOST=

PORT=5001
DOMAIN=
DEBUG=False
SECRET_KEY=
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] your.domain

SQL_ENGINE=django.db.backends.postgresql_psycopg2
SQL_DATABASE=emenu
SQL_USER=
SQL_PASSWORD=
SQL_HOST=
SQL_PORT=5431

DEFAULT_FROM_EMAIL=potrawy@potrawy.pl
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

```

### Uruchomienie: `docker-compose up -d --build`
### Instalacja środowiska developerskiego: `pipenv install -d`
### Uruchomienie testów: `pipenv run tests`
### Pokrycie kodu testami: `pipenv run report`

## REST API LEVEL 3

```
http://localhost:5001/api/  <-  api  menus
http://localhost:5001/api/schema/  <- do pobrania
http://localhost:5001/api/schema/swagger-ui/
http://localhost:5001/api/schema/redoc/
```

# Demo

```
http://emenu.adamski.work/api/  <-  api  menus
http://emenu.adamski.work/api/schema/  <- do pobrania
http://emenu.adamski.work/api/schema/swagger-ui/
http://emenu.adamski.work/api/schema/redoc/
```

# Extra

Wykorzystane CI/CD oparte o Github actions, testuje aplikację i wykonuje deploy na środowsiko `demonstracyjne` po pozytywnym przejściu testów

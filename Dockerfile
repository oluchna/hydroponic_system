FROM python:3.12.4

RUN pip install poetry

WORKDIR /user/src/app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

EXPOSE 8000

ENV DJANGO_ENV=production

CMD ["sh", "-c", "poetry run python hydroponicsystem/manage.py migrate && poetry run python hydroponicsystem/manage.py runserver 0.0.0.0:8000"]
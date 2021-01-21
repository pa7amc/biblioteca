FROM python:3.8

RUN pip install poetry

RUN mkdir /app

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

COPY db.sqlite3 /app/

COPY static /app/static
COPY templates /app/templates
COPY app.py /app/

RUN poetry config virtualenvs.create false && poetry install

CMD ["python", "app.py"]
FROM python:3

RUN pip install poetry

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN poetry config virtualenvs.create false && poetry install

CMD ["python", "app.py"]
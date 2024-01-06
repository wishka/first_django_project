FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.7.1" "gunicorn"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./

COPY my_site .

CMD ["gunicorn", "my_site.wsgi:application", "--bind", "0.0.0.0:8000"]
FROM python:3.12

WORKDIR / .

COPY requirements.txt ./requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_PORT=$API_PORT
ENV HOST=$HOST

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . /

CMD gunicorn app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind $HOST:$API_PORT
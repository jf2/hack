FROM python:3.6-slim-stretch

RUN apt-get update && apt-get install -y build-essential

COPY Pipfile* /
RUN pip install pipenv

RUN pipenv install --skip-lock --system

COPY run.py /
COPY config.yaml /
COPY app /app
COPY credentials /root/.config/earthengine/credentials
COPY commit_hash.txt /

CMD python run.py
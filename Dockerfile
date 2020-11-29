FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /requirements.txt
RUN pip install --require-hashes -r /requirements.txt

COPY src /src

COPY entrypoint.sh /entrypoint.sh

WORKDIR /src

CMD ["/entrypoint.sh"]
ENTRYPOINT ["sh", "-c"]
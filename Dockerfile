FROM python:3-stretch

ENV APP_HOME /app
WORKDIR ${APP_HOME}
EXPOSE 80

COPY . ${APP_HOME}

RUN apt-get update && \
    apt-get install -y lsb-release && \
    wget http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-6-amd64.deb && \
    dpkg -i couchbase-release-1.0-6-amd64.deb && \
    apt-get update && \
    apt-get install -y libcouchbase-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

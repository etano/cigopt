# Cigopt 🚬

Like [Sigopt](https://sigopt.com), but self-hosted and using open-source components.

## Usage

Spin up the docker containers for `couchbase` and `cigopt`.

```
docker-compose up -d
curl -v -X POST http://localhost:8091/settings/web -d 'password=password&username=admin'
curl -v -X POST http://localhost:8091/pools/default/buckets -d 'name=experiments&ramQuotaMB=128'
```

NOTE: Data will be persisted in `./couchbase`.

Documentation for the API can be found at `http://127.0.0.1:8000/docs`.

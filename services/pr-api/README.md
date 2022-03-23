## Features

- Docker
- MySQL

## Non-Features

- Dockerized `MySQL` for dev

## Usage

Dev with dockerized `MySQL`

First, in docker-compose.local.yml file, edit mysql image suitable for your operating system.
`arm64v8/mysql:oracle` if use Mac m1, `mysql` for others

```sh
# for Mac M1
version: "3.9"

services:
  mysqldb:
    image: arm64v8/mysql:oracle
    restart: unless-stopped
    env_file: ./.env
...

# others
version: "3.9"

services:
  mysqldb:
    image: mysql
    restart: unless-stopped
    env_file: ./.env
...
```

Build container

```sh
docker-compose --file docker-compose.local.yml up -d --build
```

Remove container

```sh
docker-compose --file docker-compose.local.yml down
rm -rf mysql_db
```

## References

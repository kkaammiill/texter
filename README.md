# texter

## description
This application is a simple API to create, retrieve, update and delete short (up to 160 chars) messages. It also counts views per message.

## setting up
This repo has `Dockerfile` and `docker-compose.yaml` files which means setting up running, local instance suitable for development is as easy as typing `docker-compose up` in your terminal. It will set up `texter-app` container witch application running on `localhost:8000` and `texter-db` which is a PostgreSQL 12 database with attached persistent volume.

Additionally local `src` directory is mounted to `texter-app` container. In result, every local change to the project will trigger hot-reload and be immidiately reflected in your local instance.


## notes

- default Django project setup has been stripped of all unnecessary stuff, there is no sessions, user models, cookies etc. just "KISS"
- there is no binding between token and article, anyone with valid token can delete articles created usgin other tokens
- there is no listing of articles, it's up to user/front app to remember uuids of created articles
- tokens are not stored in DB, for this task there is only one token needed and it is stored in apps memory, if you want to make more generic token handling consider using some kind of cache, sending query to db with each request just to check tokens is ugly


## env vars

| variable | desc | example |
| - | - | - |
|`EDITOR_TOKENS` | list of tokens which can be used to authorize requests | `db35bf1d585f21a34d146b3ae2616e,5be4471d2744b21c0b80dcaf6d8cd2` |
| `DB_NAME` | name of database on postgres server | `postgres` |
| `DB_USER` | name of a user to use on postgres server | `postgres` |
| `DB_PASSWORD` | password of a user to be user on a postgres server | `postgres` |
| `DB_HOST` | host of a postgres server | `texter-db` |
| `DB_POST` | port of a postgres service | `5432` |

## endpoints and usage

### authentication
Keeping things simple, there is only one type of authorization, a token-based one. 3 out of 4 available actions (create, update and delete) require authorization. To authorize your request successfuly you have to add `authorization: token <token-value>` header with valid `token-value`. Valid tokens are part of the app configuration.

### endpoints

#### create
`POST localhost:8000/articles/`

###### access
anyone with valid token

###### description
creates new article, return newly created resource

###### example
```
curl -X POST \
    -H 'authorization: token ABC' \
    -H 'content-type: application/json' \
    -d '{"body": "my new article"}' \
    http://localhost:8000/articles/

{"uuid":"0e8fa3ec-b121-4bd0-b312-1d6ced5d5d8b","body":"my new article","views_count":0}
```

#### retrieve
`GET localhost:8000/articles/<article-uuid>/`

###### access
anyone who knows article uuid

###### description
returns requested article, increments views count

###### example
```
curl -X GET \
    http://localhost:8000/articles/0e8fa3ec-b121-4bd0-b312-1d6ced5d5d8b/

{"uuid":"0e8fa3ec-b121-4bd0-b312-1d6ced5d5d8b","body":"my new article","views_count":1}
```

#### update
`PUT localhost:8000/articles/<article-uuid>/`

###### access
anyone who knows article uuid and has a valid token

###### description
updates body of the article, restarts views counter

###### example
```
curl -X PUT \
    -H 'authorization: token ABC' \
    -H 'content-type: application/json' \
    -d '{"body": "new content"}' \
    http://localhost:8000/articles/0e8fa3ec-b121-4bd0-b312-1d6ced5d5d8b/

{"uuid":"0e8fa3ec-b121-4bd0-b312-1d6ced5d5d8b","body":"new content","views_count":0}
```

#### delete
`DELETE localhost:8000/articles/<article-uuid>/`

###### access
anyone who knows article uuid and has a valid token

###### description
deletes article

###### example
```
curl -X DELETE \
    -H 'authorization: token ABC' \
    http://localhost:8000/articles/0e8fa3ec-b121-4bd0-b312-1d6ced5d5d8b/


curl -X GET \
    http://localhost:8000/articles/0e8fa3ec-b121-4bd0-b312-1d6ced5d5d8b/

{"detail":"Not found."}
```

### running tests
assuming you will use docker
```
docker-compose up
docker exec -it texter-app bash
python manage.py test
```

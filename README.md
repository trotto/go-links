# Trotto Go Links

[![CircleCI](https://circleci.com/gh/trotto/go-links.svg?style=svg)](https://circleci.com/gh/trotto/go-links)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/trotto/go-links)

_(See the guide [here](https://www.trot.to/docs/deploy/deploy-to-heroku) to deploy to Heroku in minutes.)_


Reliable and battle-tested continuously in production since 2017, this [go links](https://www.trot.to/go-links) solution
is used by companies all around the world daily as the core of [Trotto](https://www.trot.to).

Try out the latest build at [latest-master.trotto.dev](https://latest-master.trotto.dev) and also check out the
matching [open-source browser extension](https://github.com/trotto/browser-extension).

If you'd rather use the fully-managed instance of Trotto, visit [www.trot.to](https://www.trot.to).

----

Don't hesitate to reach out to us through help@trot.to, a GitHub issue, or live chat
at https://www.trot.to.

----

## Features

Trotto provides all the baseline functionality you'd expect from a go links solution, including the ability to
create, use, and modify go links that are shared with your organization—and with nobody else.

Trotto also includes powerful features above and beyond a basic go links implementation, including a searchable go
links directory, a [browser extension](https://github.com/trotto/browser-extension) that makes go links work instantly,
and programmatic links, which are go links containing placeholders that map onto the destination
URL (ex: `go/gh/%s` pointing to `https://github.com/my_org/%s`).

For a full list of Trotto's features, check out https://www.trot.to/how-it-works.

## Authentication

At the moment, the open-source app solely supports authentication using a Google account,
but we plan to add support for additional identity providers upon request. So if you need support
for another provider, submit a GitHub issue, and we'll help you out!

## Deploy the app

See our deployment docs:

- [Deploy to Heroku](http://www.trot.to/docs/deploy/deploy-to-heroku)
- [Deploy with Docker](http://www.trot.to/docs/deploy/deploy-with-docker)

### Local deployment with docker-compose

#### Build and push image to a container registry

There is no official docker image for go-links, so you need to build the image
and push it to a container registry yourselves.
Here's an example on how to do so:

```
docker build -t your_dockerhub_username/golinks:0.1 .
docker push your_dockerhub_username/golinks:0.1
```

#### Add app.yml (and possibly client_secrets.json)

Add `app.yml` to `server/src/config/` - here is an example:
```
sessions_secret: it_is_a_secret
postgres:
  url: "postgresql://postgres_username:postgres_password@db/golinks"
```
More details on `app.yml` can be found at [Deploy with Docker](http://www.trot.to/docs/deploy/deploy-with-docker)

If you want to set up your own Google OAuth, then you can follow the instruction in Deploy with Docker.
However you could also use the provided `server/src/local/client_secrets_local_only.json`.

#### Create database and run migration

Create database
```
docker-compose up db
docker exec -it go-links_db_1 /bin/sh

> psql -U postgres
postgres=# CREATE DATABASE golinks;
postgres=# \q
> quit
```

Run migration
```
docker-compose up golinks
docker exec -it go-links /bin/sh

> cd /usr/src/app/server/src
> export FLASK_APP=main.py
> flask db upgrade
```

#### Run docker-compose

Modify `docker-compose.yaml` as required, at least modify the go-links image path.

```
docker-compose up
```

On your browser go to: `http://localhost:9095`.

## Local development

You can bring up a local instance of Trotto within a few minutes.

### Clone this repository

```
git clone git@github.com:trotto/go-links.git
cd go-links
```

### Create a virtualenv

Inside the `go-links/server` directory, create and enter a
Python 3.8 [virtualenv](https://docs.python.org/3/library/venv.html) and install dependencies:

```
cd go-links/server
python3 -m venv .virtualenv
source .virtualenv/bin/activate
pip install -r src/requirements.txt
```

You can use `pyenv` as well.

### Add an app.yml file

Add a file at `server/src/config/app.yml` with this format:

```yaml
sessions_secret: any_secret
postgres:
  url: "postgresql://username:password@host/database"
```

`postgres.url` should be the connection string for a Postgres 12 database. The server
startup script will add the tables Trotto needs.

### Start the backend server

From the `server/` directory, run:

```
./run_local.sh
```

### Start the frontend development server

In a separate terminal, from the `frontend/` directory, run:

```
yarn install
./start_dev_server.sh
```

Now, you can access the local instance at http://localhost:5007.

### Making changes

Most server-side and frontend changes should be picked up automatically, thanks to the Flask dev server and
[React Hot Loader](https://github.com/gaearon/react-hot-loader).


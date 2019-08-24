# go-links

[![CircleCI](https://circleci.com/gh/trotto/go-links.svg?style=svg)](https://circleci.com/gh/trotto/go-links)

Reliable and battle-tested, this go links solution is used by companies all around the world daily as the
core of [Trotto](https://www.trot.to).

Try out the latest build at [latest-master.trotto.dev](https://latest-master.trotto.dev). If you'd rather use
the fully-managed instance of Trotto, check out [www.trot.to](https://www.trot.to).

----

Don't hesitate to reach out to us through help@trot.to, a GitHub issue, or live chat
at https://www.trot.to.

----

## Features

Trotto provides all the baseline functionality you'd expect from a go links solution, including the ability to
create, use, and modify go links that are shared with your organization—and with nobody else.

Trotto also includes powerful features above and beyond a basic go links implementation, including a searchable go
links directory, a Chrome extension* that makes go links work instantly, and programmatic links, which are go links
containing placeholders that map onto the destination URL (ex: `go/gh/%s` pointing to `https://github.com/my_org/%s`).

For a full list of Trotto's features, check out https://www.trot.to/how-it-works.

_* We're in the process of open-sourcing the Chrome extension as well. If you'd like to be involved in that,
subscribe to [this issue](https://github.com/trotto/go-links/issues/4) or email us at help@trot.to._

## Authentication

At the moment, the open-source app solely supports authentication using a Google account,
but we plan to add support for additional identity providers upon request. So if you need support
for another provider, submit a GitHub issue, and we'll help you out!

## Local development

You can bring up a local instance of Trotto within a few minutes.

### Install the Google Cloud SDK

Follow the instructions [here](https://cloud.google.com/sdk/docs/quickstarts) to install the Cloud SDK for Google
Cloud Platform.

Once you've installed the SDK, you should be able to successfully run `gcloud info`.

### Clone this repository

```
git clone git@github.com:trotto/go-links.git
cd go-links
```

### Start the backend server

From the `server/` directory, run:

```
./install_deps.sh
./run_local.sh
```

### Start the frontend development server

In a separate terminal, from the `frontend/` directory, run:

```
npm install
./start_dev_server.sh
```

Now, you can access the local instance at http://localhost:5007.

### Making changes

Most server-side and frontend changes should be picked up automatically, thanks to the App Engine dev server and
[React Hot Loader](https://github.com/gaearon/react-hot-loader).

### View the admin console

Access the development admin console at http://localhost:8095. The admin console allows you to view the datastore,
use an interactive console, and more.

## Deploying your own Trotto instance

You can deploy your own instance to [Google App Engine](https://cloud.google.com/appengine/) in
around 15 minutes. If you have any trouble, contact us through any of the channels mentioned above,
and we'll get back to you ASAP.

### Sign up for App Engine

If you don't already use Google App Engine, sign up through https://console.cloud.google.com/freetrial.

### Create a new App Engine app

Go [here](https://console.cloud.google.com/projectcreate) and create a new Google Cloud
Platform project, then create a new App Engine application in that project.
See [this screencast](https://www.screencast.com/t/YMA4LswQuCB).

Be sure to note your GCP project ID, which is shown when you create a new project and is also visible
in the GCP console URL, as the `project=` query parameter. For example, in the screencast above,
the new project's ID is `trotto-test-7`.

### Obtain OAuth client credentials

To support Google authentication, you need to create OAuth client credentials to include with your
app. See [this screencast](https://www.screencast.com/t/f2hgCLlrEGi).

* Your authorized domain will have the format `PROJECT_ID.appspot.com` (example: `trotto-test-7.appspot.com`)
* Your authorized redirect URI will have the format `https://PROJECT_ID.appspot.com/_/auth/oauth2_callback`
(example: `https://trotto-test-7.appspot.com/_/auth/oauth2_callback`)
* You'll need to download a credentials file as shown in the screencast and rename it `client_secrets.json`

### Clone this repository

```
git clone git@github.com:trotto/go-links.git
cd go-links/server
```

### Install the Google Cloud SDK

Install the Google Cloud SDK using the instructions [here](https://cloud.google.com/sdk/docs/).

Once you've installed the SDK, authorize the SDK to access your GCP project:

```
gcloud auth login
```

### Create a virtualenv

Inside the `go-links/server` directory, create and enter a
Python 2 [virtualenv](https://virtualenv.pypa.io/en/latest/installation/):

```
cd go-links/server
virtualenv --python=/usr/bin/python2.7 .virtualenv/
source .virtualenv/bin/activate
```

### Install Python dependencies

From the same directory, run:

```
pip install -r requirements.txt
```

### Add your OAuth client credentials

Take the credentials file you generated above (which should be renamed to `client_secrets.json`) and
put it in the `server/src/config` directory.

### Deploy the app

Now, you can deploy the app. From the `server/` directory, run:

```
./deploy.sh
```

After a successful deploy, you'll be able to access your Trotto instance at https://PROJECT_ID.appspot.com!

# go-links

----

Don't hesitate to reach out to us through help@trot.to, a GitHub issue, or live chat
at https://www.trot.to.

----

## Deploying your own Trotto instance

_**Authentication**: At the moment, the open-source app solely supports authentication using a Google account,
but we plan to add support for additional identity providers as requested. So if you need support
for another provider, submit a GitHub issue, and we'll help you out!_

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

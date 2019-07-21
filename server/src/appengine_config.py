import os

from google.appengine.ext import vendor

vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs'))  # use full path for sake of unit tests

from requests_toolbelt.adapters import appengine

appengine.monkeypatch()

# Google+ Sign-In Python Test App

In order to explore the Google+ Sign-In API I wrote a few test programs based
on the python and javascript quick start applications. For more information
about this API see https://developers.google.com/+/web/signin/. 

This example makes use of the [Bottle web
framework](http://bottlepy.org/docs/stable/) and the [Beaker sessions
library](http://beaker.readthedocs.org/en/latest/). Prior to running the
application, you must install the following libraries:

* [bottle](https://pypi.python.org/pypi/bottle/0.11.6)
* [Beaker](https://pypi.python.org/pypi/Beaker/1.6.4)
* [httplib2](https://pypi.python.org/pypi/httplib2/0.8)
* [oauth2client](https://pypi.python.org/pypi/oauth2client/1.1) (1.1 or greater)

To run this demo you must register your application on the [Google APIs
Console](https://code.google.com/apis/console). Be sure to request access for
the Google+ API service and from
the JavaScript origin `http://localhost:9021/`. You can leave Redirect URIs
blank as the javascript handles the first part of the OAuth2 exchange.

Retrieve your Client ID and Client Secret and place them in the appropriate
areas of the `client_secrets.json` file. Then you can run the `signin.py`
program. This will start a server on port 9021 which you can reach using the
URL `http://localhost:9021/`. 

The endpoint `http://localhost:9021/` creates a page which performs the
server-side OAuth2 flow using a one-time code provided by a javascript
authorization request as described here
https://developers.google.com/+/web/signin/server-side-flow . There is also a
version at `http://localhost:9021/staticjs` which performs client-side flow to
display the same page. More information about that method is found here
https://developers.google.com/+/web/signin/#using_the_client-side_flow .

When performing server-side flow credentials are saved in the credentials
directory for each authorized user. The `offline_fetch.py` program
demonstrates how to use those credentials to perform API calls from the
server.

An important realization I had when going through the samples is that google
will generate only 1 refresh token for every client id/user pair. Therefore
when that refresh token is present, you should save the credentials if you
need to make offline calls to the API on behalf of the user. In the
server-side example I check if a refresh token is present and save the
credentials in that case.

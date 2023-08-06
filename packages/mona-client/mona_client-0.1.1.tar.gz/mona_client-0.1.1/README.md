# Python Client

## Installation

\$ pip install mona-client

## Environment variables

Mona uses several environment variables you need to set in order for things to
work as intended:

MONA_HOST - the Mona server's IP address you get from Mona.
MONA_PORT - The port for the above address.
MONA_USER_ID - A unique user id we provide for you.

## Quick Start and Example

- Install as mentioned above
- Set environment variables as mentioned above
- Instrument code with client as seen below

```
from mona_client import client
...

with client.new_mona_context(ARC_class="MY_COOL_ALGORITHM_NAME"):
    ...
    client.export({"foo": "bar"})
    ...
```

## ARCs, sub-ARCs, KAPIs and Dimensions

All the information you send Mona is sent using the "export()" function. You can
send any json-serializable dict via this function. All the fields sent via
export are either considered (raw) KAPIs or (raw) dimensions.

KAPI stands for Key Algorithmic Performance Indicator. These are all data
relevant for how your algorithm is performing. Examples could be a
sub-component's confidence score, or the amount of results received from a
specific algorithm.

Dimensions are all metadata relevant for segmenting KAPI values. For example,
end-user demographics, a customer/user-id or a data source id.

We call the exported data "raw", as sometimes we don't use this data directly,
but generate actual KAPIs/dimensions from it (e.g., when looking at an average
value over time as a KAPI).

As you export data to Mona throughout your code, Mona aggregates it on its
servers to a struct called an ARC. ARC stands for Algorithm Run Context. Each
ARC describes an entire algorithm run. You can create as many ARCs as you'd like
in your code, but in general, a single run of your code should correspond to a
single ARC. In order to tell Mona all exports should belong to the same ARC, you
must init a new context. This is usually done in one place in your code, where a
new run is started, using:

```
with client.new_mona_context(ARC_class="MY_COOL_ALGORITHM_NAME"):
```

You assign "classes" to contexts. This tells Mona which ARCs describe runs of
the same algorithm, thus allowing Mona to compare them, segment them and find
relevant insights.

If you have logically separable parts to your algorithm, you can init
sub-contexts using:

```
with client.new_mona_sub_context(ARC_class="MY_COOL_SUB_COMPONENT_NAME"):
```

## Concurrency

Mona saves the ARC's id as a special variable, which is local to the thread and
to greenlets. This means that if you start a new thread/greenlet, by default the
new thread will have an empty context.

This is usually the preffered behavior, as a new thread usually means a new
received request (on servers) or a completely new run of an algorithm.

If by any chance you'd like to continue with the same context on a new thread,
just use the child class MonaThread under mona_thread.py. This class takes
care of transferring the full context id to the newly started thread.

```
from mona_client import client
from mona_client.mona_thread import MonaThread

def threaded_function():
    print(client.get_full_context_id() == main_context)

with client.new_mona_context():
    global main_context
    main_context = client.get_full_context_id()
    MonaThread(target=threaded_function).start()  # Prints "True"
```

## Testing the client code

The client's tests are written using the pytest framework, so in order to run
the tests (assuming you have pytest installed on your environment), you just
need to type "pytest" to your shell.

## Uploading new version to PyPI

The main reference to follow to do that is on:
https://packaging.python.org/tutorials/packaging-projects/

- Register on PyPI with your mona email: https://pypi.org/
- Ask itai@monalabs.io to add you as collaborator
- If not installed, install twine: \$ python3 -m pip install --user --upgrade twine
- Change version number under setup.py
- If a new dependency is required, add it under setup.py under "install_requires"
- If not installed, install build tools: \$ python3 -m pip install --user --upgrade setuptools wheel
- Build new version: \$ python3 setup.py sdist bdist_wheel
- Upload new version (can change '\*' to actual version): \$ python -m twine upload dist/\_

## Configuration and Big Red Button

If you'd like to set up configuration for mona, you can fill a simple json
configuration file. See mona_client_config.json for the default configuration
file used. There is currently only one configuration option, which is the "Big
Red Button" - the "disable_all" configuration, which, when set to true,
completely disables all mona activity (no more exporting and context inits).

Mona listens to changes on the configuartion file under the environment variable
"MONA_CLIENT_CONFIG_FILE". So if you want to disable mona while running, just
change "disable_all" from "false" to "true" in your config file and mona will
update automatically.

regindexer
==========
regindexer is a tool for creating an index of a container registry. It can be run manually from the command line, or can run as a daemon that consumes message from fedmsg and rebuilds the index when it sees messages from Bodhi.

regindexer creates a static index or indexes and always scans the entire registry. [Flagstate](https://github.com/owtaylor/flagstate) is a more advanced (and also trickier to deploy) version of the registry-indexing concept - it maintains a incrementally updated database of the registry metadata and supports flexible queries against the database. regindexer and Flagstate share the same output JSON format. See https://github.com/owtaylor/flagstate/blob/master/docs/protocol.md#responses for a description of the format.

One thing that regindexer supports that Flagstate doesn't currently is icon extraction: if `extract_icons` is true in the config file, then when a `org.freedesktop.appstream.icon-64` or
`org.freedesktop.appstream.icon-128` annotations is found and the contents point to a data URI, then the icon is stored in the configured icon directory (with a content-addressed path), and the data: URI converted to a URI pointing to the icon.

Installation
============
To install:

``` sh
python3 setup.py install
```

this installs the code, and the `regindexer` script.

Usage
=====

The indexer is run manually as:

```
regindexer [-c/--config=CONFIG_FILE] [-v/--verbose] index
```

regindexer-daemon
=================

`regindexer-daemon` is a daemon that listens `<topic>.<env>.bodhi.mashtask.complete` where `<topic>` and `<env>` come from `config.yaml`, checks if the content type of the mask task is `container` or `flatpak`, and rebuilds the index.

Configuration
=============

The config file has a default location of `/etc/regindexer/config.yaml` and has the following structure:

``` yaml
# Directory to extract icons into, resolved with the index as a base
icons_dir: /var/lib/regindexer/icons
# Public URI relative to the index file URIs for the icon directory
icons_uri: /icons/
indexes:
    flatpak_amd64:
        # Local location where to write the index JSON
        output: /var/lib/regindexer/index/flatpak-amd64.json
        # Registry to index
        registry: https://1.2.3.4:5000
        # Public URI to the registry, to be included in the output index,
        # resolved with the index as a base
        registry_public: https://registry.example.com:5000
        # Tags of images to index (* and ? are supported for globbing)
        tags: ['latest', 'latest-*']
        # Only index images with the specified annotations
        required_annotations: ['org.flatpak.body']
        # Only index images for the specified architectures
        architectures: ['amd64']
        # Whether to extract icons into the icons directory
        output: /home/otaylor/tmp/flatpak.json
    all:
        output: /var/lib/regindexer/index/all.json
        registry: https://1.2.3.4:5000
        registry_public: https://registry.example.com:5000
        tags: ['latest']
daemon:
    # Listen for messages of <topic_prefix>.<environment>.bodhi...
    topic_prefix: org.fedoraproject
    environment: dev
```

Development environment
=======================

The distribution contains a docker-compose environment that sets up:

 * a registry with test data
 * a local fedmsg bus
 * a regindexer index triggerered off of fedmsg
 * a HTTP frontend that exports the registry and index in a combined web heirarchy

To start it up and load the test data, do:

```
docker-compose build && docker-compose up
```

The index and registry will be available at http://localhost:7080 and https://localhost:7443 ; to test access via https with valid certificates, `make trust-local` will adjust `/etc/pki/ca-trust/source/anchors/` and `/etc/hosts` so that https://registry.local.fishsoup.net:7443 works. You can find a generated index at: https://https://registry.local.fishsoup.net:7443/index/all.json

To trigger a reindex via fedmsg, use `make trigger-reindex`.

You can also run regindexer from a Python virtualenv, either against a remote registry, or against the registry from the docker-compose setup.

```
$ virtualenv-3 ~/.virtualenvs/regindexer
$ . ~/.virtualenvs/regindexer/bin/active
$ pip install -e .

# Read from docker-compose registry and writes output into out/
$ regindexer -v -c config-devel.yaml index
```

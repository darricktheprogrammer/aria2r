aria2r
==========

In the spirit of [aria2c][1] and [aria2p][2], aria2r is a command line utility to add downloads to a (r)emote, or (r)unning instance of aria2.

While aria2 is a great download manager, one of its biggest drawbacks is the inability to easily add additional downloads when run as a daemon. While it is possible to add downloads through one of the several available GUIs, you are limited to adding one download at a time, and scrolling through seemingly endless options to find the ones you want to change.

The goal of aria2r is to provide a familiar interface for quickly and easily adding a single or multiple downloads to aria2 without having to restart the service. As much as possible, aria2r strives to match the interface, design, and verbiage used by aria2c. Any notable divergences come with an explanation behind the decision.

[Full documentation][4].


## Installation

aria2r is written in Python and can be installed through pip.

```bash
pip install aria2r --user
```


## Examples

Basic example of adding a single download to aria2 running on the same machine

```bash
aria2r --urls "http://host/file.zip"
```

Download a file from 2 mirrors

```bash
aria2r -u "http://host/file.zip" "http://mirror/file.zip"
```

Add downloads to a remote server listening on a non-default port

```bash
aria2r --host 10.0.0.1 --port 8660 "http://host/file.zip"
```

Add multiple downloads through an [aria2 input file](https://aria2.github.io/manual/en/html/aria2c.html#input-file)

```bash
aria2r -i /path/to/input-file.txt
```


## Command Line Options

```text
usage: cli.py [-h] [-c CONFIG] [-u [URLS [URLS ...]]] [-i INPUT_FILE] [-d]
              [--host HOST] [--port PORT] [--rpc-secret RPC_SECRET] [-v] [-q]

Add downloads to a running instance of aria2c. Given one or more URLS (or an
INPUT_FILE in the same format as aria2c input files), aria2r will use aria2's
RPC interface to add the downloads (with options) to a running instance of
aria2c. It is mandatory to supply either the URLS or INPUT_FILE argument, but
it is an error to provide both.

optional arguments:
  -h, --help            show this help message and exit

  -c CONFIG, --config CONFIG
                        config file path

  -u [URLS [URLS ...]], --urls [URLS [URLS ...]]
                        One or more urls to a file. All given urls must be
                        mirrors to the same file and be http/https protocol.
                        Torrent, Magnet, and Metalink files are not supported.

  -i INPUT_FILE, --input_file INPUT_FILE
                        Path to an aria2c formatted input file

  -d, --dry-run         Read the input file or urls and build the request, but
                        don't send it to the aria2 instance.

  --host HOST           The ip or fully qualified domain name where aria2 is
                        located. (Default: localhost)

  --port PORT           The port that aria2 listens on. (Default: 8600)

  --rpc-secret RPC_SECRET
                        Secret authorization token set for the aria2 rpc
                        interface.

  -v, --verbose         Increase level of output.

  -q, --quiet           Decrease level of output.
```


[1]: https://aria2.github.io/
[2]: https://github.com/pawamoy/aria2p
[4]: https://aria2r.readthedocs.io/en/latest/

aria2r
==========

In the spirit of [aria2c][1] and [aria2p][2], aria2r is a command line utility to add downloads to a (r)emote, or (r)unning instance of aria2.

While aria2 is a great download manager, one of its biggest drawbacks is the inability to easily add additional downloads once it is started. While it is possible to add downloads through one of the several available GUIs, you are limited to adding and setting options for each download manually, one at a time.

For more information, [see the full documentation][4].


## Philosophy

The goal of aria2r is to provide a familiar interface for quickly and easily adding as many downloads as you'd like. As much as possible, aria2r strives to match the interface, design, and verbiage used by aria2c. Any notable divergences come with an explanation behind the decision.


## Installation

aria2r is written in Python and hosted on PyPi, and can be installed through pip.

	pip install aria2r --user


## Examples

Basic example of adding a single download for aria2 running on the same machine

	aria2r --urls https://raw.githubusercontent.com/darricktheprogrammer/aria2r/master/README.md


Download a file from 2 mirrors

	aria2r --urls https://raw1.githubusercontent.com/darricktheprogrammer/aria2r/master/README.md https://raw2.githubusercontent.com/darricktheprogrammer/aria2r/master/README.md


Add downloads to a remote server listening on a non-default port through an [aria2 input file][3]

	aria2r -i /path/to/input-file.txt --host 10.0.0.1 --port 8660

## Command Line Options

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
	  --host HOST           The ip or address where aria2 is located. (Default:
	                        localhost)
	  --port PORT           The port that aria2 listens on. (Default: 8600)
	  --rpc-secret RPC_SECRET
	                        Secret authorization token set for the aria2 rpc
	                        interface.
	  -v, --verbose         Increase level of output.
	  -q, --quiet           Decrease level of output.


[1]: https://aria2.github.io/
[2]: https://github.com/pawamoy/aria2p
[3]: https://aria2.github.io/manual/en/html/aria2c.html#input-file
[4]: #

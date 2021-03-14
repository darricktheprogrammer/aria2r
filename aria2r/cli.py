#!/usr/bin/env python3
"""
Add downloads from a file to a running instance of aria2c

Given an INPUT_FILE in the same format as aria2c input files, aria2r will
use the jsonrpc api to add the downloads (with options) to a running instance
of aria2c.
"""
import logging
import sys
from pathlib import Path
from pprint import pformat

import configargparse
from xdg import XDG_CONFIG_HOME

from aria2r import api


logging.basicConfig(
	stream=sys.stdout, format="%(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)


def set_logging(args):
	if args.verbose:
		log.setLevel(logging.DEBUG)
	elif args.quiet:
		log.setLevel(logging.WARN)


def parse_aria2_options(aria2_args):
	aria2_parser = configargparse.ArgParser()
	for option in filter(lambda x: x.startswith("--"), aria2_args):
		aria2_parser.add(option)
	aria2_dict = vars(aria2_parser.parse_args(aria2_args))
	return {k.replace("_", "-"): v for k, v in aria2_dict.items()}


def _get_parser():
	config_files = [
		str(Path(__file__).resolve().parent / "defaults.conf"),
		str(XDG_CONFIG_HOME / "aria2r" / "config"),
	]
	p = configargparse.ArgParser(
		description=__doc__,
		add_config_file_help=False,
		default_config_files=config_files,
		formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
	)
	p.add("-c", "--config", is_config_file=True, help="config file path")
	return p


def main():
	p = _get_parser()
	p.add("input_file")
	p.add("-d", "--dry-run", default=False)
	p.add("--host")
	p.add("--port")
	p.add("--rpc-secret", default=None, help="secret text.")
	p.add_argument(
		"-v",
		"--verbose",
		action="store_true",
		default=False,
		help="a boolean flag.",
	)
	p.add_argument(
		"-q",
		"--quiet",
		action="store_true",
		default=False,
		help="a boolean flag.",
	)
	config, extra_arguments = p.parse_known_args()

	set_logging(config)
	aria2_options = parse_aria2_options(extra_arguments)
	with open(config.input_file) as inputfile:
		downloads = api.parse(inputfile.read())
	downloads = api.add_command_line_options(downloads, aria2_options)
	log.debug(config)
	log.info(pformat(downloads))


if __name__ == "__main__":
	main()

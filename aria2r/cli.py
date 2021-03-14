#!/usr/bin/env python3
"""
Add downloads from a file to a running instance of aria2c

Given an INPUT_FILE in the same format as aria2c input files, aria2r will
use the jsonrpc api to add the downloads (with options) to a running instance
of aria2c.
"""
import logging
import sys
import uuid
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
	log.debug(f"Parsing global args from: {aria2_args}")
	aria2_parser = configargparse.ArgParser()
	for option in filter(lambda x: x.startswith("--"), aria2_args):
		aria2_parser.add(option)
		log.debug(f"Found global option: {option}")
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


def build_rpc_request(downloads):
	# Not all parameters for the request are named. The unique portion
	# (url and options) are sent as a two item list where the first item is a
	# list of uris and the second item is any options to apply to the download.
	#
	# Example:
	# {
	# 	"jsonrpc": "2.0",
	# 	"method": "aria2.addUri",
	# 	"id": str(uuid.uuid4())[:12],
	# 	"params": [
	# 		[{uri1}, {uri2}],
	# 		{
	# 			"option1": "value",
	# 			"option2": "value"
	# 		}
	# 	]
	# }
	common_payload = {
		"jsonrpc": "2.0",
		"method": "aria2.addUri",
		"id": str(uuid.uuid4())[:8],
	}
	return [
		dict(common_payload, params=[dl["uris"], dl["options"]])
		for dl in downloads
	]
	return downloads


def main():
	p = _get_parser()
	p.add("-u", "--urls", nargs="*")
	p.add("-i", "--input_file", help="Path to an aria2c formatted infile")
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
	args, extra_arguments = p.parse_known_args()
	set_logging(args)
	log.debug(f"aria2r arguments: {pformat(vars(args))}")
	aria2_options = parse_aria2_options(extra_arguments)
	log.debug(f"aria2c global arguments: {pformat(aria2_options)}")
	downloads = []
	if args.input_file and args.urls:
		log.error("Error: Must provide url(s) or input file, not both.")
		exit(1)
	elif args.urls:
		downloads.append({"options": {}, "uris": [*args.urls]})
	elif args.input_file:
		with open(args.input_file) as inputfile:
			downloads.extend(api.parse(inputfile.read()))
	downloads = api.add_command_line_options(downloads, aria2_options)
	rpc_data = build_rpc_request(downloads)
	log.debug(f"Download json: {pformat(downloads)}")
	log.info(f"Making request: {pformat(rpc_data)}")


if __name__ == "__main__":
	main()

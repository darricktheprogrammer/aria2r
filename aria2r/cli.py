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

import requests
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
	for arg in aria2_args:
		if arg.startswith("-") and not arg.startswith("--"):
			msg = f"Invalid argument: {arg}\n"
			msg += "Cannot use short variations of aria2 global args"
			log.error(msg)
			exit(1)
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


def build_rpc_request(downloads, rpc_secret):
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

	# The id below is not aria2 specific, but is part of the [json rpc
	# specification](https://www.jsonrpc.org/specification). Each request
	# object must have a unique identifier. This is only used during the
	# initial request. Aria2 will provide a gid for each download, which is
	# separate from the request id.
	common_payload = {
		"jsonrpc": "2.0",
		"method": "aria2.addUri",
	}
	return [
		dict(
			common_payload,
			id=str(uuid.uuid4()),
			params=[f"token:{rpc_secret}", dl["uris"], dl["options"]],
		)
		for dl in downloads
	]


def handle_response(response, downloads):
	# If secret is wrong for the first download, it will be wrong for all of
	# them. Fail early with a meaningful message.
	first_dl_err = response[0].get("error", {}).get("message", None)
	if first_dl_err == "Unauthorized":
		msg = "Error adding downloads\nMissing or incorrect rpc secret"
		log.error(msg)
		exit(1)

	# aria2r will not check all possible error messages. If an error is caused
	# due to aria2c-specific issues, alert the user using the returned code.
	dl_lookup = {dl["id"]: dl["params"][1:] for dl in downloads}
	failed_downloads = [dl for dl in response if "error" in dl.keys()]
	for err_response in failed_downloads:
		download_id = err_response["id"]
		failed_download = dl_lookup[download_id]
		uris, options = failed_download
		formatted = api.dict_to_input_file({"uris": uris, "options": options})
		errmsg = err_response["error"]["message"]
		msg = f"\nDownload error\n"
		msg += f"--------------\n"
		msg += f"message: '{errmsg}'\n"
		msg += f"{formatted}\n"
		log.error(msg)


def main():
	p = _get_parser()
	p.add("-u", "--urls", nargs="*")
	p.add("-i", "--input_file", help="Path to an aria2c formatted infile")
	p.add(
		"-d",
		"--dry-run",
		action="store_true",
		default=False,
		help="a boolean flag.",
	)
	p.add("--host")
	p.add("--port")
	p.add("--rpc-secret", default="", help="secret text.")
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
	log.debug(f"aria2c arguments: {pformat(aria2_options)}")
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
	rpc_data = build_rpc_request(downloads, args.rpc_secret)
	log.debug(f"Parsed from input file:\n{pformat(downloads)}")
	rpc_endpoint = f"http://{args.host}:{args.port}/jsonrpc"
	if args.dry_run:
		msg = f"Dry run. Skip sending request to aria2 instance at {rpc_endpoint}..."
		log.info(msg)
		msg = f"data sent:\n{pformat(rpc_data)}"
		log.debug(msg)
	else:
		msg = f"Sending request to aria2 instance at {rpc_endpoint}..."
		log.info(msg)
		msg = f"data sent:\n{pformat(rpc_data)}"
		log.debug(msg)
		response = requests.post(rpc_endpoint, json=rpc_data)
		log.debug(f"response:\n{pformat(response.json())}")
		handle_response(response.json(), rpc_data)


if __name__ == "__main__":
	main()

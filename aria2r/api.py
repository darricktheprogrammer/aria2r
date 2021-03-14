"""
Docstring for main module in aria2r.

A longer description...
"""
import re
import configparser
from typing import List


def parse(text: str) -> List[dict]:
	uris = re.findall(r"^[^(\s?#|$)].*", text, re.M)
	for uri in uris:
		text = text.replace(uri, f"[{uri}]")
	parser = configparser.ConfigParser()
	parser.read_string(text)
	return [
		{"uris": uris.split("\t"), "options": dict(parser[uris])}
		for uris in parser.sections()
	]


def add_command_line_options(downloads: List[dict], options: dict):
	for download in downloads:
		download["options"].update(options)
	return downloads

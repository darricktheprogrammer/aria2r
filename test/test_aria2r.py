#!/usr/bin/env python3
import pytest

from aria2r import cli


@pytest.fixture
def sample_infile():
	return"""
# a file
https://www.reddit.com/r/devops/comments/b2rf4y/are_you_using_containers_in_production/	https://www.reddit.com/r/devops/comments/b2rf4y/are_you_using_containers_in_production/
	# some options
	out=rd_containers-production_b2rf4y.html
	http-user=packersfan
	http-passwd=abcd7260&$$()

https://www.reddit.com/r/devops/comments/avozad/is_there_a_way_to_not_use_load_balance_when_using/
	out=rd_balancing_avozad.html
"""


def test_aria2r_GivenConfig_ReturnsParsedConfig(sample_infile):
	downloads = cli.parse_input_file(sample_infile)
	assert len(downloads) == 2
	assert len(downloads[0]["uris"]) == 2
	assert len(downloads[1]["uris"]) == 1
	assert downloads[0]["options"] == {
		"out": "rd_containers-production_b2rf4y.html",
		"http-user": "packersfan",
		"http-passwd": "abcd7260&$$()",
	}


def test_aria2r_GivenEqualSignAsOptionValue_ReturnsCorrectValue():
	sample_infile = """
https://www.reddit.com/r/devops/comments/avozad/is_there_a_way_to_not_use_load_balance_when_using/
	http-passwd=abcd7260&$$=()
"""
	downloads = cli.parse_input_file(sample_infile)
	assert downloads[0]["options"]["http-passwd"] == "abcd7260&$$=()"


def test_aria2r_GivenCommandLineOptions_OptionsAreAddedToDownloadOptions(sample_infile):
	downloads = cli.parse_input_file(sample_infile)
	aria2_options = {"timeout": "60"}
	downloads_final = cli.add_command_line_options(downloads, aria2_options)
	assert "timeout" in downloads_final[0]["options"]
	assert "timeout" in downloads_final[1]["options"]
	assert downloads_final[0]["options"]["timeout"] == "60"
	assert downloads_final[1]["options"]["timeout"] == "60"

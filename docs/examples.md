Examples
========

:::{include} ../README.md
------------
	start-after: "## Examples"
	end-before: "## Command Line Options"
------------	
:::

Add multiple downloads through an input file, specifying options that will be applied to all downloads located in the file (in this case all downloads are behind basic authentication)

	aria2r -i /path/to/input-file.txt --http-user username --http-passwd 'pa$$word'

Providing a config file in an alternate location

	ari2r -c ~/myconfigs/aria2r.conf "http://host/file.zip"

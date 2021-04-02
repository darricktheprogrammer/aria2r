# Command Line Options

The following options are available to aria2r. Each option can be provided at the command line as shown, or in the [configuration file][1] without the `--` prefix.

:::{option} -c , --config <config>

Alternate path to a configuration file.

(Default: `$XDG_CONFIG_HOME/aria2r/config`)
:::


::::{option} -u , --urls <url> [<url> ...]

One or more urls to a file. All given urls must be mirrors to the same file and be http/https protocol. Torrent, Magnet, and Metalink files are not supported.

You do not need to specify this flag more than one time. For multiple mirrors, you can add as many urls after the argument as you like, each separated with a space.

:::{note}
It is mandatory to supply either the `--urls` or `--input_file` argument, but it is an error to provide both.
:::

This is the most notable change from aria2c's interface. The use of the `-u` flag in place of positional arguments and support for only http downloads is partially technical and partially for simplicity.

When running the `aria2c` command, all http urls must point to the same file, but torrents, magnets, and metalinks are each treated as a separate download. Due to my own use case, in which I only use aria2 to download http files, I decided for now that it's not worth the effort of sorting through multiple urls and attempting to determine which are mirrored locations and which are separate downloads.

The `-u` flag is a tradeoff for the ability to [use all of the options][2] available in the `aria2c` command. Due to the fact that aria2r attempts to gather those options and pass them on without hardcoding all of the options available makes it difficult to allow positional arguments as part of the interface. For more detailed technical information on this, see [issue #1][3]. This may be changed in a later version.
::::


:::{option} -i , --input_file <input_file>

Path to an [aria2c formatted input file][4]. Use this to add multiple downloads.
:::


:::{option} -d, --dry-run

Read the input file or urls and build the request, but don't send it to the aria2 instance. This supercedes the aria2c option of the same name. The only way to specify a dry run to aria2 at this time is to add it as an option in an input file.
:::


:::{option} --host <host>

The ip or fully qualified domain name where aria2 is located.

(Default: localhost)
:::


:::{option} --port <port>

The port that aria2 listens on.

(Default: 8600)
:::


:::{option} --rpc-secret <rpc-secret>

Secret authorization token expected by the running aria2 rpc interface. This is the only authorization method supported by aria2r as `rpc-user`/`rpc-passwd` have [been deprecated][5].

(Default: "")
:::


:::{option} -v, --verbose 

Increase level of output.
:::


:::{option} -q, --quiet 
Decrease level of output.
:::


## Passing Options to aria2

All of the normal [command line options for aria2c][6] are available in aria2r. For instance, you can provide the `--http-user`/`--http-passwd` for downloads behind basic auth. Or you can use the `--dir` option to change the download location.

In the case of adding a single download with the `--urls` flag, these options are simply applied to that download.

In the case of adding downloads through an input file, any `aria2c` option provided through the comand line will be applied to all downloads in the current batch. To use an option against only some of the downloads (such as `--out` or if only some of the downloads require authentication), you will need to add each option to their respective download in the input file.



[1]: configuration.md
[2]: #passing-options-to-aria2
[3]: https://github.com/darricktheprogrammer/aria2r/issues/1
[4]: https://aria2.github.io/manual/en/html/aria2c.html#input-file
[5]: https://aria2.github.io/manual/en/html/aria2c.html#cmdoption-rpc-user
[6]: https://aria2.github.io/manual/en/html/aria2c.html#options

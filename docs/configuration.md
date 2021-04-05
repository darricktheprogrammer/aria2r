Configuration
=============

For configuration, aria2r takes its cues from aria2c. aria2r has its own defaults which can be overridden by a user supplied configuration file, or by using arguments on the command line.


## Config File

By default, aria2r looks for a configuration file in the [XDG_CONFIG_HOME][1] directory (typically `~/.config/aria2r/config`). An alternate path can be provided with the `-c` option, in which case the former config file will be ignored.

The config file uses INI-style formatting of `OPTION=VALUE`, where `OPTION` is the [command line option][2] excluding the `--` prefix. Note that in the config file, you must use the long form name of the option. For instance, on the command line, `aria2r` accepts either `-v` or `--verbose`, but the configuration file must only use `verbose=true`.

```ini
# Example config for a remote server with an --rpc-secret token
host=10.0.0.1
rpc-secret=$$secret$$
```


## Order of resolution

The order in which aria2r applies options is as follows, with input lower in the list taking precedence and overriding those higher in the list.

* aria2r defaults
* config file (either in `XDG_CONFIG_HOME/aria2r/config` or supplied with the `-c` option)
* arguments supplied on the command line



[1]: https://wiki.archlinux.org/index.php/XDG_Base_Directory#User_directories
[2]: options.md

servicecontrol usage
======================

servicecontrol is a script intended to perform a number of functions

  * allow one program  to turn on/off any other program
  * log output of that program
  * restart program if it crashes (for whatever reason)
  * monitor that program's resource utilisation and reboot if necessary

Syntax
--------

The syntax is::

    servicecontrol <paramters> "<program with its own parameters>"


As usual you can get help by typing::

    serviceconrol --help

Which will produce the built-in help on the available syntax::

    usage: servicecontrol.py [-h] [--start] [--addr ADDR] [--port PORT]
                             [--no-echo] [--autorestart] [--cpurestart CPURESTART]
                             [--log LOG] [-i]
                             cmd

    positional arguments:
      cmd                   The command to parse

    optional arguments:
      -h, --help            show this help message and exit
      --start               Immediately start software (do not wait for start())
      --addr ADDR           xmlrpc address, default=localhost
      --port PORT           xmlrpc port, default=9001
      --no-echo             Do not display output to stdout
      --autorestart         Restart on crash
      --cpurestart CPURESTART
                            Set CPU threshold to automatically restart service at
      --log LOG             Filename to log to (default is None - stdout only)
      -i, --interact

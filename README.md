# rtl_433-graylog.py
_[ By sirkus7, https://github.com/sirkus7/rtl_433-graylog ]_

This script provides a simple way to send results from `rtl_433` directly to a Graylog server with very little setup. Pipe results from `rtl_433` to `rtl_433-graylog.py` and it will format the results into a GELF message and fire them off to the Graylog server you specify. No need to set up extractors or set up other transport mechanisms. Quick and solid. 

_Quick background:_ https://github.com/merbanan/rtl_433 is a generic data receiver that uses an SDR receiver to listen to a frequency (or several, if hopping frequencies), and attempts to identify and decode broadcast messages from various devices. Sending results to Graylog allows you to query/chart/analyze the results over time.

## Configure 
Edit `rtl_433-graylog.py` and set the GL_SERVER variable value to your hostname or IP address of your Graylog server, and the port to the UDP GELF input port you configured on the Graylog server. 

For example: 

    GL_SERVER=("192.168.20.12",12201)

## Basic Use
_Example 1, most basic use case:_ 

    $ rtl_433 -F json | ./rtl_433-graylog.py

Fundamentally, run `rtl_433` with the "-F json" argument so that it formats all output as json, then pipe that to `rtl_433-graylog.py`.

_Example 2, include additional metadata fields, like frequency, level info, protocol id; also using -v to print out the message on the console:_

    $ rtl_433 -M level -M protocol -F json | ./rtl_433-graylog.py -v


_Example 3, tuning into 315MHz, include meta data, verbose messages to console_

    $ rtl_433 -M level -M protocol -f 315M -F json | ./rtl_433-graylog.py -v
# rtl_433-graylog.py
[ By sirkus7, https://github.com/sirkus7/rtl_433-graylog ]

This script takes output from `rtl_433` and formats it, then sends it directly to a Graylog server in GELF UDP format. This allows Graylog to consume all `rtl_433` results without having to rely on syslog or other transport mechanisms. 

Quick background: https://github.com/merbanan/rtl_433 is a generic data receiver that uses an SDR receiver to listen to a frequency (or several, if hopping frequencies), and attempts to identify and decode broadcast messages from various devices. I've found it useful and many occasions to send the results to a Graylog server for indexing, where I can then query, chart, and otherwise analyze the results over time. This script, makes it easy to send the results to a Graylog server. 

## Configure 
Edit `rtl_433-graylog.py` and set the GL_SERVER variable value to your hostname or IP address of your Graylog server, and the port to the UDP GELF input port you configured on the Graylog server. 

For example: 

    GL_SERVER=("192.168.20.12",12201)

## Basic Use
Most basic use example:

    $ rtl_433 -F json | ./rtl_433-graylog.py

The above demonstrates the most basic use of `rtl_433-graylog.py`. Run rtl_433 with the "-F json" argument so that it formats all output as json, then pipe that to `rtl_433-graylog.py`.

## Args
Sometimes it's helpful to log the frequency that you targeted when you received these messages. Since  `rtl_433` doesn't include this data in the json output, you can use the `-f` argument with a desriptive string to have `rtl_433-graylog.py` to add this field. Whatever you give as the string will be the value of a new field "freq" in the Graylog entry. 

Example, adding a "freq" field

    $ rtl_433 -F json | ./rtl_433-graylog.py -f 433.920MHz

Since, by default, `rtl_433` tunes into 433.920MHz, you could use the `-f 433.920MHz` argument to add the field "freq" to the Graylog entry, with the matching frequency value. Remember, this is a free form string, you can put any string in any format in it. Which means, you could also put the wrong frequency in there, in an it won't care. But whatever you add will be logged in Graylog as "freq" for that entry. 

Example, tuning into 315MHz, and adding a matching `freq` field:

    $ rtl_433 -f 315M -F json | ./rtl_433-graylog.py -f 315.000MHz -v
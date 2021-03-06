#!/usr/bin/python3
#
# rtl_433-graylog.py - https://github.com/sirkus7/rtl_433-graylog
# A simple way to send rtl_433 results directly to Graylog.
# In Graylog, configure a UDP GELF input, note the port you choose.
# Configure this script by setting the GL_SERVER to point to the Graylog
# host and port.
#
# Example use, (-M level with rtl_433 to include frequency info):
# $ rtl_433 -M level -F json | ./rtl_433-graylog.py
# Example 2, set frequency, also print messages to console (-v)
# $ rtl_433 -M level -f 315M -F json | ./rtl_433-graylog.py -v

import sys
import argparse
import json
import socket

# Configure to your Graylog server's UDP GELF input: ("hostname-or-IP-address", port)
GL_SERVER=("graylog",12204)

# Send UDP Gelf Message, arg is a dict of params to values
def sendGelfMsg(params):
    gelfmsg = json.dumps(params).encode()
    if len(gelfmsg) > 8190:                 # If for some reason, this is too large for a GELF UDP packet
        gelfmsg = gelfmsg.encode("zlib")    #, zlib compresss it, which Graylog supports.
    if len(gelfmsg) > 8190:                 #, If still too big, error out.
        print("Error: Compressed GELF UDP packet > 8190, not indexed!")
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(gelfmsg, GL_SERVER)

# Setup and get arguments
parser = argparse.ArgumentParser(description='Pipe rtl_433 results directly to a Graylog UDP GELF input.')
parser.add_argument("-v", action='store_true', help="Verbose, print GELF messages to console.")
args = parser.parse_args()

# Get hostname
hostname = socket.gethostname() 

# Process incoming json data from STDIN
for line in sys.stdin:
    #print(f"Input line: {line}")
    try:
        jdata = json.loads(line)
        gdata={
            "version":"1.1",
            "host" : hostname,
            "_rtl_433" : "true"
        }

        # Convert json data to GELF message
        msg="rtl: "
        for item in jdata:
            gdata['_'+item]=jdata[item] # Convert each key name to a GELF custom property, with a "_" prefix
            if item != 'time':    # Build short message, full K:V list, without timestamp, for brevity
                msg+=f"{item}:{jdata[item]} "  
        gdata['short_message']=msg
        
        if args.v is not None: 
            print(f"\nGELF: {gdata}")
        #Send GELF message
        sendGelfMsg(gdata)

    except:
        print('Error: could not deserialize line into jason: ' + line)
    
    


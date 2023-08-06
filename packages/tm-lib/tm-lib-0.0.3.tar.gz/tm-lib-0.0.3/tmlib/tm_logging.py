#!/usr/bin/env python3
import logging
import socket
from time import localtime, strftime

# import db connection functions
from tmlib.tm_db import open_db


def write_accesslog(activity, param_json):
    # remove any _id values
    param_json.pop("_id", None)

    db_trading_minions = open_db()
    col_accesslogs = db_trading_minions.access_logs
    logging.debug("Writing access log: " + activity)
    local_time = strftime("%Y.%m.%d %HH:%HH.%SS", localtime())
    hostname = socket.gethostname()
    col_accesslogs.insert({"activity": activity, "timestamp": local_time, "hostname": hostname, "data": param_json})

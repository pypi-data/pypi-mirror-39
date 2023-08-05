#!/usr/bin/env python3
import json
import logging
import re
import sys
from time import gmtime, strftime

# import connexion
from connexion import NoContent

# Import utils
from tmlib.eiutils import toJson
from tmlib.rego_key import get_regokey
from tmlib.tm_authorisation import authorization
# Authentication imports
# import db connection functions
from tmlib.tm_db import open_db
# Imports to write accesslog
from tmlib.tm_logging import write_accesslog
from tmlib.tradingminion import get_tradingminion


@authorization()
def check_update(account_number, broker_name, minion_name, minion_version, parameters_version=''):
    logging.debug("In check_update")
    accesslog_json = {
        "account_number": account_number,
        "broker_name": broker_name,
        "minion_name": minion_name,
        "parameters_version": parameters_version
    }
    minion_version = assert_version_format(minion_version)
    parameters_version = assert_version_format(parameters_version)
    logging.debug("Authenticated: going for data")
    # get the last versions from the trading minion. Get this from the minion info
    minion, error = get_tradingminion(minion_name)
    if not minion:
        logging.info("Bad minion_name")
        return NoContent, 404

    logging.debug("Retrieved minion record. Type=" + type(minion).__name__)
    # Strip off the lists
    while isinstance(minion, list):
        minion = minion[0]  # get the first item

    if isinstance(minion, str):
        json_out = json.loads(minion)
    else:
        json_out = json.dumps(minion)

    logging.debug("json_out type=" + type(json_out).__name__)
    # check if support is still valid. Get this from the rego json
    rego, error = get_regokey(account_number, broker_name, minion_name)
    if error == 404:
        logging.info("Could not retrieve rego key")
        return NoContent, 404
    # build the return json

    logging.debug(("jsonout is type: " + type(json_out).__name__))
    if isinstance(json_out, str):
        json_out = json.dumps(json_out)
    logging.debug(("jsonout is NOW type: " + type(json_out).__name__))

    json_out.update(rego)
    # Do the comparision and set boolean flags
    current_gmt = strftime("%Y.%m.%d", gmtime())

    support_expired = current_gmt > json_out['support_expiry']
    expert_update_available = minion_version < json_out['last_version_expert']
    parameters_update_available = parameters_version < json_out['last_version_parameters']

    json_out['support_expired'] = support_expired
    json_out['expert_update_available'] = expert_update_available
    json_out['parameters_update_available'] = parameters_update_available
    # Write to the access log
    accesslog_json.update(json_out)
    write_accesslog(sys._getframe().f_code.co_name, accesslog_json)
    return json_out, 200


@authorization()
def get_parameter_update(minion_name, broker_name, minion_edition, parameters_version=""):
    logging.debug("In get_parameter_update")
    parameters_version = assert_version_format(parameters_version)
    accesslog_json = {
        "minion_name": minion_name,
        "broker_name": broker_name,
        "parameters_version": parameters_version
    }
    logging.debug("Authenticated: going for data")
    db_trading_minions = open_db()
    col_parameters = db_trading_minions.parameters
    if len(parameters_version):
        logging.debug(
            "Looking for specific parameter set: " + minion_name + "; " + broker_name + ";" + minion_edition + "; " + parameters_version)
        results = list(col_parameters.find(
            {"minion_name": minion_name,
             "broker_name": broker_name,
             "edition": minion_edition,
             "version": parameters_version}
        ))
    else:  # no param version passed - get the latest
        logging.debug(
            "Looking for latest parameter set: " + minion_name + "; " + broker_name + ";" + minion_edition)
        results = list(col_parameters.find(
            {"minion_name": minion_name,
             "broker_name": broker_name,
             "edition": minion_edition
             }).sort("version", -1).limit(1)
                       )
    logging.debug(str(len(results)) + " results returned.")
    logging.debug("results is type: " + type(results).__name__)
    if results:
        error_code = 200
    else:
        return NoContent, 404
    update = [toJson(r) for r in results]
    # Strip off the lists
    while isinstance(update, list):
        update = update[0]  # get the first item
    if isinstance(update, str):
        json_out = json.loads(update)
    else:
        json_out = update.copy()

    # Write to the access log
    accesslog_json.update(json_out)
    accesslog_json['filedata'] = "<<deleted>>"
    write_accesslog(sys._getframe().f_code.co_name, accesslog_json)
    return json_out, error_code


def assert_version_format(version_stamp):
    # Ensures that the version is in YYYY.MM.DD format (assumin it may be in YYYYMMDDxx format)
    squishdate = "^[\\d]{8}"
    mt4date = "^[\\d]{4}\\.[\\d]{2}\\.[\\d]{2}$"
    if version_stamp == "":
        return ""
    if re.match(mt4date, version_stamp):
        #        logging.debug("Version OK for " + version_stamp)
        return version_stamp
    #    logging.debug("Asserting version format on " + version_stamp)
    match_obj = re.match(squishdate, version_stamp)
    if match_obj:
        # match_obj.group() contains the date part. insert the dots
        stamp = match_obj.group()
        new_stamp = stamp[0:4] + "." + stamp[4:6] + "." + stamp[6:8]
        #        logging.debug("Updated version format to " + new_stamp)
        return new_stamp
    # Unhandled format
    logging.info("Could NOT asset version format for " + version_stamp)
    return ""

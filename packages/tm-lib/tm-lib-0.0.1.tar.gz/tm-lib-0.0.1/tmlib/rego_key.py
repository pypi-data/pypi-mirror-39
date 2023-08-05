#!/usr/bin/env python3
import logging
import sys

# import connexion
from connexion import NoContent

from tmlib.eiutils import get_or_404
from tmlib.models import Customer, Registration
# Authentication imports
from tmlib.tm_authorisation import authorization
# import constants
from tmlib.tm_db import open_db
# Imports to write accesslog
from tmlib.tm_logging import write_accesslog
# Import utils
from tmlib.tm_obfuscate import deobfuscate, obfuscate


# from pymongo import MongoClient
# from jsonschema import validate


def _regokey_from_json(minion_name, account_number, broker_name, in_json):
    try:
        rego_key = in_json["licenses"][minion_name]["account_registrations"][str(account_number)]["rego_key"]
    except:
        rego_key = ""
    support_expiry = in_json["licenses"][minion_name]["support_expires"]
    # Make the expire MT4 format
    support_expiry = support_expiry.replace("-", ".")

    if rego_key:
        rego_expiry = deobfuscate(rego_key)
        logging.debug("deobf rego key: " + rego_expiry)
        str_start = rego_expiry.find("--")
        if str_start > 0:
            str_start += 2
            rego_expiry = rego_expiry[str_start: str_start + len("1970.01.01")]
        else:
            rego_expiry = ""
    else:
        rego_key = ""
        rego_expiry = ""

    return {
        "minion_name": minion_name,
        "account_number": account_number,
        "broker_name": broker_name,
        "rego_key": rego_key,
        "rego_expiry": rego_expiry,
        "support_expiry": support_expiry
    }


"""
get_regokey
"""


@authorization()
def get_regokey(account_number, broker_name, minion_name, experimental=False):
    if experimental:
        return get_regokey_experimental(account_number=account_number, broker_name=broker_name,
                                        minion_name=minion_name)
    return get_regokey_legacy(account_number=account_number, broker_name=broker_name,
                              minion_name=minion_name)


def get_regokey_legacy(account_number, broker_name, minion_name):
    logging.debug("In get_regokey")
    # Setup json for accesslog
    access_log_json = {
        "account_number": account_number,
        "broker_name": broker_name,
        "minion_name": minion_name
    }
    logging.debug("Authenticated: going for data")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    logging.debug("Looking for specific account: " + broker_name + "; " + str(account_number) + ";" + minion_name)
    results = list(col_contacts.find({"licenses." + minion_name + ".account_registrations." + str(
        account_number) + ".broker": broker_name}))  # ,
    #                                    "licenses.account_registrations.account_number": account_number,
    #                                   "licenses.account_registrations.broker": broker_name }))
    logging.debug(str(len(results)) + " results returned.")
    if len(results) == 0:
        access_log_json.update({"registered": False})
        write_accesslog(sys._getframe().f_code.co_name, access_log_json)
        return NoContent, 404
    else:
        error_code = 200
        access_log_json.update({"registered": True})
        regokey_json = _regokey_from_json(minion_name, account_number, broker_name, results[0])

    # Write to the access log
    access_log_json.update(regokey_json)
    write_accesslog(sys._getframe().f_code.co_name, access_log_json)
    return regokey_json, error_code


def get_regokey_experimental(account_number, broker_name, minion_name):
    logging.debug("In get_regokey")
    # Setup json for accesslog
    access_log_json = {
        "account_number": account_number,
        "broker_name": broker_name,
        "minion_name": minion_name
    }
    logging.debug("Authenticated: going for data")
    logging.debug("Looking for specific account: " + broker_name + "; " + str(account_number) + ";" + minion_name)
    pipelines = [
        {"$match": {"licenses.minion_name": minion_name,
                    "licenses.account_registrations.account_number": account_number,
                    "licenses.account_registrations.broker": broker_name}},
        {"$unwind": "$licenses"},
        {"$unwind": "$licenses.account_registrations"},
        {"$match": {"licenses.minion_name": minion_name,
                    "licenses.account_registrations.account_number": account_number,
                    "licenses.account_registrations.broker": broker_name}},
        {"$project": {"_id": 0, "rego_key": "$licenses.account_registrations.rego_key",
                      "support_expires": "$licenses.support_expires"}}
    ]
    results = Customer.objects.aggregate(*pipelines)
    results = list(results)
    logging.debug(str(len(results)) + " results returned.")
    if not results:
        access_log_json.update({"registered": False})
        write_accesslog(sys._getframe().f_code.co_name, access_log_json)
        return NoContent, 404

    error_code = 200
    access_log_json.update({"registered": True})
    try:
        rego_key = results[0]["rego_key"]
    except:
        rego_key = ""
    support_expiry = results[0]["support_expires"]
    # Make the expire MT4 format
    support_expiry = support_expiry.strftime('%Y.%m.%d')

    if rego_key:
        rego_expiry = deobfuscate(rego_key)
        logging.debug("deobf rego key: " + rego_expiry)
        try:
            _, rego_expiry = rego_expiry.split("--")
            rego_expiry = rego_expiry[:len("1970.01.01")]
        except ValueError:
            rego_expiry = ""
    else:
        rego_key = ""
        rego_expiry = ""

    result_json = {
        "minion_name": minion_name,
        "account_number": account_number,
        "broker_name": broker_name,
        "rego_key": rego_key,
        "rego_expiry": rego_expiry,
        "support_expiry": support_expiry
    }
    # Write to the access log
    access_log_json.update(result_json)
    write_accesslog(sys._getframe().f_code.co_name, access_log_json)
    return result_json, error_code


"""
eof get_regokey
"""

"""
put_regokey
"""


@authorization()
def put_regokey(contact_login, minion_name, account_number, rego_expiry_string='_NO_EXPIRY_STRING',
                in_rego_key='_NO_REGO_KEY', experimental=False):
    if experimental:
        pass
    return put_regokey_legacy(contact_login=contact_login, minion_name=minion_name, account_number=account_number,
                              rego_expiry_string=rego_expiry_string, in_rego_key=in_rego_key)


def put_regokey_legacy(contact_login, minion_name, account_number, rego_expiry_string='_NO_EXPIRY_STRING',
                       in_rego_key='_NO_REGO_KEY'):
    if in_rego_key != '_NO_REGO_KEY':
        rego_key = in_rego_key
    else:
        if rego_expiry_string != '_NO_EXPIRY_STRING':
            rego_key = obfuscate(str(account_number) + "--" + rego_expiry_string)
        else:
            # No expiry - use 1970.01.01 (never expires)
            rego_key = obfuscate(str(account_number) + "--1970.01.01")
    # Connect
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts

    updateresult = col_contacts.update_one(
        {'login': contact_login},
        {
            '$set': {
                'licenses.' + minion_name + '.account_registrations.' + str(
                    account_number) + '.rego_key': rego_key
            }
        },
        False
    )
    if not updateresult.acknowledged:
        return_text = "The Upsert was not acknowledged by the server."
        return_code = 500
    else:
        return_text = "Rego key updated."
        return_code = 200
    return return_text, return_code


@get_or_404
def put_regokey_experimental(contact_login, minion_name, account_number, rego_expiry_string='_NO_EXPIRY_STRING',
                             in_rego_key='_NO_REGO_KEY'):
    if in_rego_key != '_NO_REGO_KEY':
        rego_key = in_rego_key
    else:
        if rego_expiry_string != '_NO_EXPIRY_STRING':
            rego_key = obfuscate(str(account_number) + "--" + rego_expiry_string)
        else:
            # No expiry - use 1970.01.01 (never expires)
            rego_key = obfuscate(str(account_number) + "--1970.01.01")

    contact = Customer.objects.get(login=contact_login)
    # get license
    account_registration: Registration = contact.get_account_registration(
        minion_name=minion_name, account_number=account_number
    )
    account_registration.rego_key = rego_key
    contact.save()
    return "Rego key updated.", 200


"""
eof put_regokey
"""
"""
delete_regokey
"""


@authorization()
def delete_regokey(contact_login, account_number, minion_name, experimental=False):
    if experimental:
        return delete_regokey_experimental(
            contact_login=contact_login,
            account_number=account_number,
            minion_name=minion_name
        )
    return delete_regokey_legacy(
        contact_login=contact_login,
        account_number=account_number,
        minion_name=minion_name
    )


def delete_regokey_legacy(contact_login, account_number, minion_name):
    print("In delete_regokey")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    update_result = col_contacts.update_one(
        {'login': contact_login},
        {
            '$set': {
                'licenses.' + minion_name + '.account_registrations.' + str(
                    account_number) + '.rego_key': ""
            }
        },
        False)
    if update_result.acknowledged:
        return NoContent, 204
    else:
        return "The Upsert was not acknowledged by the server.", 500


@get_or_404
def delete_regokey_experimental(contact_login, account_number, minion_name):
    print("In delete_regokey")
    contact = Customer.objects.get(login=contact_login)
    account_registration: Registration = contact.get_account_registration(
        account_number=account_number, minion_name=minion_name
    )
    account_registration.rego_key = ''
    contact.save()
    return NoContent, 204


"""
eof delete_regokey
"""

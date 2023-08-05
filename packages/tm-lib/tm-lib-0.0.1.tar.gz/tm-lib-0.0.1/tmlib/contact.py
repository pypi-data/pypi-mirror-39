#!/usr/bin/env python3
import json
import logging

from bson.json_util import dumps
from connexion import NoContent
from mongoengine.errors import ValidationError

# Import utils
from tmlib.eiutils import toJson
from tmlib.models import Customer, License, Registration
# Authentication imports
from tmlib.tm_authorisation import authorization
# import db connection functions
from tmlib.tm_db import open_db


def get_contacts(experimental=False):
    return get_contact("_NO_NAME", experimental=experimental)


"""
Get contact
"""


@authorization()
def get_contact(contact_login, experimental=False):
    if experimental:
        return get_contact_experimental(
            contact_login=contact_login
        )
    return get_contact_legacy(
        contact_login=contact_login
    )


def get_contact_legacy(contact_login):
    logging.debug("In get_contact")
    logging.debug("Authenticated: going for data")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    if contact_login != "_NO_NAME":
        logging.debug("Looking for specific contact: " + contact_login)
        results = dumps(col_contacts.find({"login": contact_login}))
        results_obj = json.loads(results)
        if not results_obj:
            return NoContent, 404
        contacts = results_obj[0]
    else:
        logging.debug("Getting all contacts")
        results = col_contacts.find({})
        contacts = [json.loads(toJson(r)) for r in results]
    return contacts, 200


def get_contact_experimental(contact_login):
    logging.debug("In get_contact")
    logging.debug("Authenticated: going for data")

    if contact_login != "_NO_NAME":
        logging.debug("Looking for specific contact: " + contact_login)
        try:
            contact = Customer.objects.get(login=contact_login)
            results_obj = json.loads(contact.to_json())
            contacts = results_obj[0]
        except Customer.DoesNotExist:
            return NoContent, 404
    else:
        logging.debug("Getting all contacts")
        contacts = [json.loads(c.to_json()) for c in Customer.objects()]
    return contacts

"""
EOF Get contact
"""

"""
Put contact
"""


@authorization()
def put_contact(contact_login, given_name, surname, experimental=False):
    if experimental:
        return put_contact_experimental(
            contact_login=contact_login, given_name=given_name, surname=surname
        )
    return put_contact_legacy(
        contact_login=contact_login, given_name=given_name, surname=surname
    )


def put_contact_legacy(contact_login, given_name, surname):
    # See if the minion already exists
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    # build the json to set

    updateresult = col_contacts.update_one({'login': contact_login},
                                           {'$set': {"given_name": given_name, "surname": surname}}, True)
    if updateresult.acknowledged:
        if updateresult.matched_count == 1:
            return_code = 200
            return_text = "Existing contact updated."
        else:
            return_code = 201
            return_text = "New contact created."
    else:
        logging.exception("The Upsert was not acknowledged by the server.")
        return "The Upsert was not acknowledged by the server.", 400

    return return_text, return_code


def put_contact_experimental(contact_login, given_name, surname):
    try:
        update_result = Customer.objects(login=contact_login).update(
            set__given_name=given_name, set__surname=surname,
            upsert=True, full_result=True
        )

        if update_result.acknowledged:
            if update_result.matched_count == 1:
                return_code = 200
                return_text = "Existing contact updated."
            else:
                return_code = 201
                return_text = "New contact created."
        else:
            logging.exception("The Upsert was not acknowledged by the server.")
            return "The Upsert was not acknowledged by the server.", 400
    except ValidationError as validation_error:
        return_text = validation_error.message
        return_code = 400

    return return_text, return_code


"""
EOF put contact
"""

"""
Deleted contact
"""


@authorization()
def delete_contact(contact_login, experimental=False):
    if experimental:
        return delete_contact_experimental(contact_login=contact_login)
    return delete_contact_legacy(contact_login=contact_login)


def delete_contact_legacy(contact_login):
    logging.debug("In delete_contact")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    logging.debug("Deleting " + contact_login)
    results = col_contacts.find_one_and_delete({"login": contact_login})

    if results:
        return NoContent, 204
    else:
        return NoContent, 404


def delete_contact_experimental(contact_login):
    logging.debug("In delete_contact")
    logging.debug("Deleting " + contact_login)
    if Customer.objects(login=contact_login).delete():
        return NoContent, 204
    return NoContent, 404


"""
EOF delete contact 
"""

"""
get_licenses
"""


@authorization()
def get_licenses(contact_login, experimental=False):
    if experimental:
        return get_licenses_experimental(contact_login=contact_login)
    return get_licenses_legacy(contact_login=contact_login)


def get_licenses_legacy(contact_login):
    logging.debug("In get_licenses")
    logging.debug("Authenticated: going for data")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    results = dumps(col_contacts.find({"login": contact_login}))
    results_obj = json.loads(results)
    # the results are now in a single element array.
    licenses = results_obj[0]["licenses"]
    return [licenses], 200


def get_licenses_experimental(contact_login):
    logging.debug("In get_licenses")
    logging.debug("Authenticated: going for data")
    try:
        licenses = Customer.objects.get(login=contact_login).licenses
        return [l.to_mongo() for l in licenses], 200
    except Customer.DoesNotExist:
        return [], 404


"""
EOF get_licenses
"""

"""
get_license
"""


@authorization()
def get_license(contact_login, minion_name, experimental=False):
    if experimental:
        return get_license_experimental(
            contact_login=contact_login, minion_name=minion_name
        )
    return get_license_legacy(
        contact_login=contact_login, minion_name=minion_name
    )


def get_license_legacy(contact_login, minion_name):
    logging.debug("In get_license")
    logging.debug("Authenticated: going for data")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    results = dumps(col_contacts.find({"login": contact_login, "licenses." + minion_name: {"$exists": "true"}}))
    results_obj = json.loads(results)
    if not results_obj:
        return NoContent, 404
    # the results are now in a single element array.
    license = results_obj[0]["licenses"][minion_name]
    return license, 200


def get_license_experimental(contact_login, minion_name):
    logging.debug("In get_license")
    logging.debug("Authenticated: going for data")
    data, status = {}, 200
    try:
        contact = Customer.objects.get(
            login=contact_login, licenses__minion_name=minion_name
        )
        data = next(l.to_mongo() for l in contact.licenses if l.minion_name == minion_name)
    except (Customer.DoesNotExist, StopIteration):
        status = 404
    return data, status


"""
EOF get_license
"""

"""
put_license
"""


@authorization()
def put_license(contact_login, wp_membership_id, minion_name,
                minion_license, support_expires, experimental=False):
    if experimental:
        return put_license_experimental(contact_login=contact_login,
                                        wp_membership_id=wp_membership_id,
                                        minion_name=minion_name,
                                        minion_license=minion_license,
                                        support_expires=support_expires)
    return put_license_legacy(contact_login=contact_login,
                              wp_membership_id=wp_membership_id,
                              minion_name=minion_name,
                              minion_license=minion_license,
                              support_expires=support_expires)


def put_license_legacy(contact_login, wp_membership_id, minion_name, minion_license, support_expires):
    # See if the minion already exists
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    # build the json to set
    update_result = col_contacts.update_one({'login': contact_login},
                                            {'$set': {'licenses.' + minion_name + '.minion_name': minion_name,
                                                      'licenses.' + minion_name + '.wp_membership_id': wp_membership_id,
                                                      'licenses.' + minion_name + '.minion_license': minion_license,
                                                      'licenses.' + minion_name + '.support_expires': support_expires}},
                                            False)
    if update_result.acknowledged:
        if update_result.matched_count == 1:
            return_code = 200
            return_text = "Existing contact updated."
        else:
            return_code = 201
            return_text = "New contact created."
    else:
        logging.exception("The Upsert was not acknowledged by the server.")
        return "The Upsert was not acknowledged by the server.", 400
    return return_text, return_code


def put_license_experimental(contact_login, wp_membership_id, minion_name, minion_license, support_expires):
    # See if the minion already exists
    try:
        contact = Customer.objects.get(login=contact_login)
    except Customer.DoesNotExist:
        return "Customer does not exists", 404
    license: License = next(
        (l for l in contact.licenses if l.minion_name == minion_name),
        None
    )
    if license:
        license.wp_membership_id = wp_membership_id
        license.minion_license = minion_license
        license.support_expires = support_expires
        return_code = 200
        return_text = "Existing contact updated."
    else:
        new_license = License(
            minion_name=minion_name,
            wp_membership_id=wp_membership_id,
            minion_license=minion_license,
            support_expires=support_expires
        )
        contact.licenses.append(new_license)
        return_code = 201
        return_text = "New contact created."
    try:
        contact.save()
    except ValidationError as validation_error:
        return_text = validation_error.message
        return_code = 400
    return return_text, return_code


"""
eof put_license
"""

"""
get_license_accounts
"""


@authorization()
def get_license_accounts(contact_login, minion_name, experimental=False):
    if experimental:
        return get_license_accounts_experimental(
            contact_login=contact_login, minion_name=minion_name
        )
    return get_license_accounts_legacy(
        contact_login=contact_login, minion_name=minion_name
    )


def get_license_accounts_legacy(contact_login, minion_name):
    logging.debug("In get_license_account")
    logging.debug("Authenticated: going for data")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    results = dumps(col_contacts.find(
        {"login": contact_login, "licenses." + minion_name + ".account_registrations": {"$exists": "true"}}))
    if results != '[]':  # empty array
        results_obj = json.loads(results)
        # the results are now in a single element array.
        accounts = results_obj[0]["licenses"][minion_name]["account_registrations"]
    else:
        return [], 200
    return [accounts], 200


def get_license_accounts_experimental(contact_login, minion_name):
    logging.debug("In get_license_account")
    logging.debug("Authenticated: going for data")
    try:
        Customer.objects.get(login=contact_login)
    except Customer.DoesNotExist:
        return [], 404

    pipeline = [
        {"$match": {"login": contact_login}},
        {"$unwind": "$licenses"},
        {"$match": {"licenses.minion_name": minion_name}},
        {"$unwind": "$licenses.account_registrations"},
        {"$project": {
            "_id": 0,
            "account_number": "$licenses.account_registrations.account_number",
            "broker": "$licenses.account_registrations.broker",
            "rego_key": "$licenses.account_registrations.rego_key",
            "checkins": "$licenses.account_registrations.checkins"}}
    ]

    data = Customer.objects.aggregate(*pipeline)
    return list(data), 200


"""
EOF get_license_accounts
"""

"""
get_license_account
"""


@authorization()
def get_license_account(contact_login, minion_name, account_number, experimental=False):
    if experimental:
        return get_license_account_experimental(
            contact_login=contact_login,
            minion_name=minion_name,
            account_number=account_number
        )
    return get_license_account_legacy(
        contact_login=contact_login,
        minion_name=minion_name,
        account_number=account_number
    )


def get_license_account_legacy(contact_login, minion_name, account_number):
    logging.debug("In get_license_account")
    logging.debug("Authenticated: going for data")
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    results = dumps(col_contacts.find({"login": contact_login,
                                       "licenses." + minion_name + ".account_registrations." + str(
                                           account_number): {"$exists": "true"}}))
    results_obj = json.loads(results)
    if not results_obj:
        return NoContent, 404
    # the results are now in a single element array.
    account = results_obj[0]["licenses"][minion_name]  # account_registrations #.[account_number]
    return account, 200


def get_license_account_experimental(contact_login, minion_name, account_number):
    logging.debug("In get_license_account")
    logging.debug("Authenticated: going for data")
    try:
        Customer.objects.get(login=contact_login)
    except Customer.DoesNotExist:
        return [], 404

    pipeline = [
        {"$match": {"login": contact_login}},
        {"$unwind": "$licenses"},
        {"$unwind": "$licenses.account_registrations"},
        {"$match": {
            "licenses.minion_name": minion_name,
            "licenses.account_registrations.account_number": account_number
        }},
        {"$project": {
            "_id": 0,
            "account_number": "$licenses.account_registrations.account_number",
            "broker": "$licenses.account_registrations.broker",
            "rego_key": "$licenses.account_registrations.rego_key",
            "checkins": "$licenses.account_registrations.checkins"
        }}
    ]

    data = Customer.objects.aggregate(*pipeline)
    data = list(data)
    data = data.pop() if data else {}
    return data, 200


"""
EOF get_license_account
"""

"""
put_license_account
"""


@authorization()
def put_license_account(contact_login, minion_name, account_number,
                        broker_name, in_rego_key="", experimental=False):
    if experimental:
        return put_license_account_experimental(
            contact_login=contact_login, minion_name=minion_name,
            account_number=account_number, broker_name=broker_name,
            in_rego_key=in_rego_key
        )
    return put_license_account_legacy(
        contact_login=contact_login, minion_name=minion_name,
        account_number=account_number, broker_name=broker_name,
        in_rego_key=in_rego_key
    )


def put_license_account_legacy(contact_login, minion_name, account_number, broker_name, in_rego_key=""):
    # See if the minion already exists
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    # build the json to set
    if in_rego_key != "":
        update_result = col_contacts.update_one(
            {'login': contact_login},
            {'$set': {
                # 'licenses.' + minion_name + '.account_registrations.' + str(account_number) : str(account_number),
                'licenses.' + minion_name + '.account_registrations.' + str(
                    account_number) + '.account_number': account_number,
                'licenses.' + minion_name + '.account_registrations.' + str(
                    account_number) + '.broker': broker_name,
                'licenses.' + minion_name + '.account_registrations.' + str(
                    account_number) + '.rego_key': in_rego_key}},
            False
        )
    else:
        update_result = col_contacts.update_one(
            {'login': contact_login},
            {'$set': {
                # 'licenses.' + minion_name + '.account_registrations.' + str(account_number) : str(account_number),
                'licenses.' + minion_name + '.account_registrations.' + str(
                    account_number) + '.account_number': account_number,
                'licenses.' + minion_name + '.account_registrations.' + str(
                    account_number) + '.broker': broker_name}},
            False
        )

    if update_result.acknowledged:
        if update_result.matched_count == 1:
            return_code = 200
            return_text = "Existing contact updated."
        else:
            return_code = 201
            return_text = "New contact created."
    else:
        logging.exception("The Upsert was not acknowledged by the server.")
        return "The Upsert was not acknowledged by the server.", 400

    return return_text, return_code


def put_license_account_experimental(contact_login, minion_name, account_number,
                                     broker_name, in_rego_key=""):
    return_text = ""
    return_code = 200
    try:
        # get contact
        contact = Customer.objects.get(login=contact_login)
        # license by minion_name
        license: License = next(
            (l for l in contact.licenses if l.minion_name == minion_name),
            None
        )
        if license is None:
            raise Customer.DoesNotExist()

        account: Registration = next(
            (a for a in license.account_registrations if a.account_number == account_number),
            None
        )
        if account:
            # update if exists
            account.broker = broker_name
            return_code = 200
            return_text = "Existing contact updated."
        else:
            # create a new account
            account = Registration(broker=broker_name, account_number=account_number)
            license.account_registrations.append(account)
            return_code = 201
            return_text = "New contact created."
        if in_rego_key:
            account.rego_key = in_rego_key
        # save data to mongo
        contact.save()
    except Customer.DoesNotExist:
        return_code = 404
        return_text = "Does not exists"
    except (ValidationError, Exception) as err:
        return_code = 400
        return_text = err.message
    finally:
        return return_text, return_code


"""
EOF put_license_account
"""

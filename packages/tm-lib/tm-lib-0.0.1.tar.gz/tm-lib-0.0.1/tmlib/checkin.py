"""
Function _update_last_checkin(string minion_name, string symbol, string broker, number account_number):
# Update the appropriate mongodb node with the current timestamp.
# if the node exists – update it – if not, create it.

return true/false (success/fail)
Notes:
The combination of Broker Name + account number is unique, and can be used to identify the document.

"""
import logging
from datetime import datetime
from typing import List, Tuple

from connexion import NoContent
from mongoengine import Q

from tmlib.models import Checkin, Customer, License, Registration
from tmlib.tm_authorisation import authorization
from tmlib.tm_db import open_db

logger = logging.getLogger()

"""
Update last checkin:
views is a update_last_checkin_view function that calls 
_update_last_checkin_legacy (a function driven by pymongo) and 
_update_last_checkin_experimental (a new made function that uses mongoengine)
"""


@authorization()
def update_last_checkin_view(account_number, broker_name, minion_name, symbol, experimental=False):
    """

    :param account_number:
    :param broker_name:
    :param minion_name:
    :param symbol:
    :param experimental: an argument to use experimental mongoengine implementation
                            with the new JSON structure
    :return:
    """
    if experimental:
        return NoContent, _update_last_checkin_experimental(account_number=account_number,
                                                            broker=broker_name,
                                                            minion_name=minion_name,
                                                            symbol=symbol)
    return NoContent, _update_last_checkin_legacy(account_number=account_number,
                                                  broker=broker_name,
                                                  minion_name=minion_name,
                                                  symbol=symbol)


def _update_last_checkin_legacy(minion_name: str, symbol: str, broker: str, account_number: int) -> int:
    """
    Update the appropriate mongodb node with the current timestamp.
    if the node exists – update it – if not, create it.
    :param minion_name:
    :param symbol:
    :param broker:
    :param account_number:
    :return: true/false (success/fail)
    """
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    status = 404

    query = {
        '$and':
            [
                {f'licenses.{minion_name}.account_registrations.{account_number}'
                 f'.account_number': account_number},
                {f'licenses.{minion_name}.account_registrations.{account_number}'
                 f'.broker': broker}
            ]
    }
    item = col_contacts.find_one(query)
    if item is None:
        return status  # item not found

    checkins = item['licenses'][minion_name].get('checkins', [])
    checkin = next(
        (
            c for c in checkins if
            (c['account_number'] == account_number
             and c['broker'] == broker
             and c['symbol'] == symbol)
        ),
        None
    )
    # update
    if checkin:
        index = checkins.index(checkin)
        checkin['last_checkin'] = datetime.now()
        checkins[index] = checkin
        status = 200
    # create
    else:
        checkins.append(
            {
                "symbol": symbol,
                "account_number": account_number,
                "broker": broker,
                "last_checkin": datetime.utcnow()
            }
        )
        status = 201
    item['licenses'][minion_name]['checkins'] = checkins
    # update data in the mongo db
    col_contacts.update_one({'_id': item['_id']}, {'$set': item})
    return status


def _update_last_checkin_experimental(
        minion_name: str, symbol: str, broker: str, account_number: int
) -> int:
    """
        Update the appropriate mongodb node with the current timestamp.
        if the node exists – update it – if not, create it.
        :param minion_name:
        :param symbol:
        :param broker:
        :param account_number:
        :return: true/false (success/fail)
        """
    status = 404

    try:
        contact: Customer = Customer.objects.get(
            (Q(licenses__account_registrations__account_number=account_number) &
             Q(licenses__account_registrations__broker=broker))
        )
    except Customer.DoesNotExist:
        return status  # item not found

    except Customer.MultipleObjectsReturned:
        logger.error(
            'Multiple object is returned for the account_number: %s and broker: %s',
            account_number, broker
        )
        return status
    account_license: License = next(
        (l for l in contact.licenses if l.minion_name == minion_name),
    )
    # license doesn't exist
    if not account_license:
        return status

    account_registration: Registration = next(
        (r for r in account_license.account_registrations if r.account_number == account_number),
        None
    )
    # account doesn't exist
    if not account_registration:
        return status

    checkin: Checkin = next(
        (c for c in account_registration.checkins if c.broker == broker and c.symbol == symbol), None
    )
    if checkin:
        # update query
        status = 200
        checkin.last_checkin = datetime.now()
    else:
        # add query
        status = 201
        account_registration.checkins.append(
            Checkin(symbol=symbol, broker=broker, last_checkin=datetime.now())
        )
    contact.save()
    return status


"""
EOF update last checkin
"""

"""
Get last checkins part legacy and experimental functions
"""

@authorization()
def get_last_checkins_json_view(experimental=False):
    """
    :param experimental: an argument to use experimental mongoengine implementation
                            with the new JSON structure
    :return:
    """
    if experimental:
        return _get_last_checkins_experimental()
    return _get_last_checkins_legacy()


def _get_last_checkins_legacy() -> Tuple[List[dict], int]:
    """
    Get users with the last checkin information.
    :return: a generator with dicts.
    """
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts
    # prepare response
    data: List[dict] = []
    status = 200  # only 200 status is possible
    for contact in col_contacts.find():
        last_checkin = None
        try:
            # get the last checkin if exists
            for license_value in contact.get('licenses', {}).values():
                for checkin in license_value.get('checkins', []):
                    checkin['minion_name'] = license_value['minion_name']
                    if isinstance(checkin['last_checkin'], str):
                        checkin['last_checkin'] = datetime.strptime(
                            checkin['last_checkin'], '%m/%d/%Y %H:%M:%S'
                        )
                    if last_checkin is None:
                        last_checkin = checkin
                    elif last_checkin['last_checkin'] < checkin['last_checkin']:
                        last_checkin = checkin
            # add info if checkin exists
            if last_checkin:
                data.append({
                    'given_name': contact['given_name'],
                    'surname': contact['surname'],
                    'login': contact['login'],
                    'minion_name': last_checkin['minion_name'],
                    'account': last_checkin['account_number'],
                    'last_checkin': last_checkin['last_checkin']
                })
        # this error should happen if the structure is changed
        # so we log this error and structure
        except Exception as e:
            logger.error("msg: %s, data: %s", e, contact)
    return data, status


def _get_last_checkins_experimental() -> Tuple[List[dict], int]:
    """
        Get users with the last checkin information.
        :return: a generator with dicts.
    """
    # prepare response

    status = 200  # only 200 status is possible
    # response structure
    pipeline = [
        # pre filter values
        {"$match": {"licenses.account_registrations.checkins": {"$exists": True}}},
        # extract embedded docs
        {"$unwind": "$licenses"},
        {"$unwind": "$licenses.account_registrations"},
        {"$unwind": "$licenses.account_registrations.checkins"},
        # group by data and get only last one
        {
            "$group":
                {
                    "_id": "$_id",
                    "given_name": {"$last": "$given_name"},
                    "surname": {"$last": "$surname"},
                    "login": {"$last": "$login"},
                    "account": {"$last": "$licenses.account_registrations.account_number"},
                    "minion_name": {"$last": "$licenses.minion_name"},
                    "last_checkin": {"$last": "$licenses.account_registrations.checkins.last_checkin"}
                }
        },
        # configure fields for the response
        {"$project": {
            "_id": 0,
            "given_name": 1,
            "surname": 1,
            "login": 1,
            "account": 1,
            "minion_name": 1,
            "last_checkin": 1,
        }}

    ]
    data = list(Customer.objects.aggregate(*pipeline))
    return data, status


"""
EOF get last checkins
"""

"""
Get last checkin details legacy and experimental functions
"""


@authorization()
def get_last_checkin_detail_json_view(contact_login, experimental=False):
    if experimental:
        return _get_last_checkin_detail_experimental(contact_login)
    return _get_last_checkin_detail_legacy(contact_login)


def _get_last_checkin_detail_legacy(login: str) -> Tuple[List[dict], int]:
    """
    Get detailed information about user's checkins
    :param login: login of the user
    :return: a dict with information
    """
    db_trading_minions = open_db()
    col_contacts = db_trading_minions.contacts

    details: List[dict] = []
    # login is a unique id, so use just find_one
    contact = col_contacts.find_one({'login': login})
    if not contact:
        # if login doesn't exist in db, return 404
        return NoContent, 404
    for license in contact.get('licenses', {}).values():
        minion_name = license['minion_name']
        for checkin in license.get('checkins', []):
            details.append({
                'minion_name': minion_name,
                'account': checkin['account_number'],
                'symbol': checkin['symbol'],
                'last_checkin': checkin['last_checkin'],
            })
    return details, 200


def _get_last_checkin_detail_experimental(login: str) -> Tuple[List[dict], int]:
    """
    Get detailed information about user's checkins
    :param login: login of the user
    :return: a dict with information
    """
    try:
        Customer.objects.get({"login": login})
    except Customer.DoesNotExist:
        return NoContent, 404

    pipeline = [
        # pre filter values
        {"$match": {"login": login}},
        # extract embedded docs
        {"$unwind": "$licenses"},
        {"$unwind": "$licenses.account_registrations"},
        {"$unwind": "$licenses.account_registrations.checkins"},
        # select data to show
        {
            "$project":
                {
                    "_id": 0,
                    "minion_name": "$licenses.minion_name",
                    "account": "$licenses.account_registrations.account_number",
                    "symbol": "$licenses.account_registrations.checkins.symbol",
                    "last_checkin": "$licenses.account_registrations.checkins.last_checkin",
                }
        },
        # sort by date
        {"$sort": {"last_checkin": -1}}
    ]
    data = list(Customer.objects.aggregate(*pipeline))

    return data, 200


"""
EOF Get last checkin details 
"""
if __name__ == '__main__':
    _update_last_checkin_legacy('Alpha', 'GBPJPY1', 'Acme Broker', 12345)
    _update_last_checkin_experimental('Alpha', 'GBPJPY1', 'Acme Broker', 12345)
    print(list(_get_last_checkins_legacy()))
    print(list(_get_last_checkin_detail_legacy("bloggsjoe@gmail.com")))

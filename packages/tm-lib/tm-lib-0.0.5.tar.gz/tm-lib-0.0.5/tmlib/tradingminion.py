#!/usr/bin/env python3
# from pymongo import MongoClient

# Authentication imports

# import db connection functions

# Import utils
# from pymongo import MongoClient
import json
import logging

from connexion import NoContent
from jsonschema import validate

# Import utils
from tmlib.eiutils import toJson
# Authentication imports
from tmlib.tm_authorisation import authorization
# import db connection functions
from tmlib.tm_db import open_db


def get_tradingminions():
    return get_tradingminion("_NO_NAME")


@authorization()
def get_tradingminion(tradingminion_name):
    logging.debug("In get_tradingminion")
    json_results = []
    logging.debug("Authenticated: going for data")
    db_tradingminions = open_db()
    minions = db_tradingminions.minions
    if tradingminion_name != "_NO_NAME":
        logging.debug("Looking for specific trading minion: " + tradingminion_name)
        results = list(minions.find({"name": tradingminion_name}))
        for result in results:
            json_results.append(toJson(result))
        tradingminions = json_results
        # # Strip off the lists
        logging.debug("Strip off the list. Type=" + type(tradingminions).__name__)
        if isinstance(tradingminions, list) and tradingminions:
            tradingminions = tradingminions[0]  # get the first item
        # logging.debug("Strip off the list (2). Type=" + type(tradingminions).__name__)
        # if type(tradingminions).__name__ == 'str':
        #     logging.debug(tradingminions)
        #     tradingminions = json.loads(tradingminions)
        #     logging.debug("Strip off the list (3). Type=" + type(tradingminions).__name__ )
        # else:
        #     tradingminions = tradingminions.copy()
        return tradingminions, 200
    else:
        logging.debug("Getting all trading minions")
        results = minions.find({})
        tradingminions = [toJson(r) for r in results]
        return tradingminions, 200


@authorization()
def put_tradingminion(tradingminion_name, tradingminion_body):
    # Validate the body against the schema
    # load the schema
    schema_name = 'minion-schema.json'
    with open('schemas/' + schema_name) as f:
        schema_data = f.read()
    schema = json.loads(schema_data)
    try:
        validate(tradingminion_body, schema)
        logging.debug("JSON schema validation OK.")
    except schema.exceptions.ValidationError as ve:
        logging.debug("JSON schema validation failed: " + ve)
        return "JSON schema validation failed.", 400

    # Check that the tradingminion_name matches the one in the body
    logging.debug("Name in body: " + tradingminion_body['name'])
    if tradingminion_name != tradingminion_body['name']:
        return "Name in JSON body doesn't match path.", 400
    # See if the minion already exists
    db_tradingminions = open_db()
    minions = db_tradingminions.minions
    updateresult = minions.update_one({'name': tradingminion_name}, {'$set': tradingminion_body}, True)
    if updateresult.acknowledged:
        if updateresult.matched_count == 1:
            return_code = 200
            return_text = "Existing record updated."
        else:
            return_code = 201
            return_text = "New record created."
    else:
        logging.exception("The Upsert was not acknowledged by the server.")
        return "The Upsert was not acknowledged by the server.", 400

    return return_text, return_code  # NoContent, (200 if exists else 201)


@authorization()
def delete_tradingminion(tradingminion_name):
    logging.debug("In delete_tradingminion")
    db_tradingminions = open_db()
    minions = db_tradingminions.minions
    logging.debug("Deleting " + tradingminion_name)
    results = minions.find_one_and_delete({"name": tradingminion_name})
    #        logging.debug("Deleted " +results['name'])
    # for result in results:
    #     delete_results.append(toJson(result))
    # logging.debug("find_one_and_delete() returned " + deleteresult)
    if results:  # len(delete_results) > 0:
        return NoContent, 204
    else:
        return NoContent, 404

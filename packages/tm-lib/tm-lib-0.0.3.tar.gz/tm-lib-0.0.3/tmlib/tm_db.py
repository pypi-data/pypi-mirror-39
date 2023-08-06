#!/usr/bin/env python3
import logging

from pymongo import MongoClient

from tmlib.settings import Settings


def mongo_uri():
    return Settings.MONGO_URI


def connect_mongo():
    logging.debug("Connecting to Mongo URI")
    return MongoClient(mongo_uri())


def open_db():
    mdb = connect_mongo()
    logging.debug("Connected to Mongo URI")
    db = mdb[Settings.MONGO_DBNAME]
    logging.debug("Connected to database")
    return db

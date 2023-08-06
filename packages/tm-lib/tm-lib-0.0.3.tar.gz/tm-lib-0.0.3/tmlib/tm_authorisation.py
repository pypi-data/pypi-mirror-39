#!/usr/bin/env python3
import logging

# from connexion import NoContent
import connexion

from tmlib.settings import Settings


# def authenticate_account():
#     # Check the authenication headers are there
# #    if connexion.request.headers.find('X-account') == -1:
# #        logging.warning("No Account apikey.")
# #        return 401
# #    if connexion.request.headers.find('X-regokey') == -1:
# #        logging.warning("No Regokey apikey.")
# #        return 401
#     # Retrieve them
#     logging.debug("In authenticate_account")
#     logging.info("MONGO_DB at " + mongo_server() + ":" + mongo_port())
#     try:
#         account = connexion.request.headers['X-account']
#         regokey = connexion.request.headers['X-regokey']
#     except LookupError:
#         logging.exception("Lookup Error.")
#         return 401
#     except Exception:
#         logging.exception("Some exception occurred.")
#         return 401

#     logging.info("account=" + account)
#     logging.info("regokey=" + regokey)
#     # Check them
#     client = MongoClient(mongo_server(), mongo_port())
#     db_lazytrader = client.LazyTrader
#     regokeys = db_lazytrader.rego_keys
#     user = regokeys.find({"account": account, "rego_key": regokey})
#     if user.count() > 1:
#         logging.error("More than one user returned from authentication query")
#     if user.count() == 1:
#         logging.info("account=" + account + " authenticated OK.")
#         return 0
#     logging.info("account=" + account + "failed to authenticate.")
#     return 401

def authenticate_admin():
    # Check the authenication headers are there
    # if connexion.request.headers.find('X-account') == -1:
    #     logging.warning("No Account apikey.")
    #     return 401
    # if connexion.request.headers.find('X-regokey') == -1:
    #     logging.warning("No Regokey apikey.")
    #     return 401
    # Retrieve them
    logging.debug("In authenticate_admin")
    logging.debug("**** BYPASSING API_KEY CHECK ******")
    try:
        api_key_admin = connexion.request.headers['X-admin']
    except LookupError:
        return 401
    except Exception as e:
        logging.exception("Some exception occurred.")
        logging.exception(str(e))
        return 401

    logging.debug("api_key_admin=" + api_key_admin)
    # Check them
    if api_key_admin == Settings.ADMIN_API_KEY:
        return 0
    return 401


def authorization(skip_auth: bool = False):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            if not skip_auth:
                auth_code = authenticate_admin()
                if auth_code != 0:
                    logging.debug("Failed to Authenticate")
                    return connexion.NoContent, 401
            return f(*args, **kwargs)

        return wrapped_f

    return wrap

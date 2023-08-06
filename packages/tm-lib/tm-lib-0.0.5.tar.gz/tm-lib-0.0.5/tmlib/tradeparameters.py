# Functions pointing to old database - based on individual symbol parameter sets - superceded

# def get_tradeparametersets(broker, version, limit):
#     logging.debug("In get_tradeparametersets")
#     authenticated = authenticate_account()
#     json_results = []
#     if authenticated == 0:
#         logging.debug("Authenticated: going for data")
#         client = MongoClient(mongo_server(), mongo_port())
#         db_lazytrader = client.LazyTrader
#         parameters = db_lazytrader.parameters
#         if version:
#             logging.debug("Came back from data 1")
#             results=list(parameters.find({"Broker": broker, "Version": version}))
#             for result in results:
#                 json_results.append(toJson(result))
#             tradeparameters = json_results
#         else:
#             logging.debug("Came back from data 2")
#             results=parameters.find({})
#             for result in results:
#                 json_results.append(toJson(result))
#             tradeparameters = json_results
#     else:
#         logging.debug("Failed to Authenticate")
#         return NoContent, 401
#     return [tradeparameters][:limit]

# def get_tradeparameterset(symbol_name, broker, version):
#     logging.debug("In get_tradeparameterset")
#     json_results = []
#     authenticated = authenticate_account()
#     if authenticated == 0:
#         client = MongoClient(mongo_server(), mongo_port())
#         db_lazytrader = client.LazyTrader
#         parameters = db_lazytrader.parameters
#         results=parameters.find({"Broker": broker, "Version": version, "Name": symbol_name})
#         for result in results:
#             json_results.append(toJson(result))
#         symbol = json_results[0]
#         if len(symbol) == 2:
#             symbol = None
#     else:
#         return NoContent, 401
# #    symbol = SYMBOLS.get(symbol_name)
#     return symbol or ('Not found', 404)


# def put_tradeparameterset(symbol_name, symbol):
#     authenticated = authenticate_admin()
#     # if authenticated == 0:
#     # exists = symbol_name in SYMBOLS
#     # symbol['id'] = symbol_name
#     # if exists:
#     #     logging.info('Updating symbol %s..', symbol_name)
#     #     SYMBOLS[symbol_name].update(symbol)
#     # else:
#     #     logging.info('Creating symbol %s..', symbol_name)
#     #     symbol['created'] = datetime.datetime.utcnow()
#     #     SYMBOLS[symbol_name] = symbol
#     return 0 #NoContent, (200 if exists else 201)


# def delete_tradeparameterset(symbol_name, version, broker):
#     authenticated = authenticate_admin()
#     if authenticated == 0:
#         client = MongoClient(mongo_server(), mongo_port())
#         db_lazytrader = client.LazyTrader
#         parameters = db_lazytrader.parameters
#         deleteresult = dumps(parameters.find_one_and_delete({"Broker": broker, "Version": version, "Name": symbol_name}))
#         logging.debug("find_one_and_delete() returned " + deleteresult)  
#         if deleteresult != "null":
#             return NoContent, 204
#         else:
#             return NoContent, 404          
#     else:
#         return NoContent, 401
#     return NoContent, 404

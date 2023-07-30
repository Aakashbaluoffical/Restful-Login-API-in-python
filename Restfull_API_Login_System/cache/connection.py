# import redis
# import sys
# from common.configuration import REDISCACHE
# REDISCACHE = REDISCACHE()
# def redis_connect() -> redis.client.Redis:
#     try:
#         client = redis.Redis(
#             host=REDISCACHE.HOST,
#             port=REDISCACHE.PORT,
#             #password=REDISCACHE.PASSWORD,
#             db=REDISCACHE.DB,
#             socket_timeout=REDISCACHE.SOCKET_TIMEOUT,
#         )
#         ping = client.ping()
#         if ping is True:
#             print('Redis ping is OK')
#             return client
#         else:
#             print('Redis ping is NOK')
#     except redis.AuthenticationError:

#         print("AuthenticationError")

#     except :
#         print("Redis errror")
#         # sys.exit(1)



# client = redis_connect()
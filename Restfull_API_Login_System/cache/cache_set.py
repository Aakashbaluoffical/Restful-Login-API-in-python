# from common.configuration import CACHEKEY
# from cache import utility
# import json
# from fastapi.encoders import jsonable_encoder
# from storage import querydata
# import pandas as pd
# from datetime import datetime,date

# CACHEKEY  = CACHEKEY()


# def get_trim_data(db,imo):
#     data = utility.get_data(key=CACHEKEY.TRIM_DATA+imo)
#     cache = False
#     if data is not None:
#         cache = True
#     else:
#         data = querydata.get_trim_data(db,imo)
#         try:
#             if data is not None:
#                 cache = False
#                 data = json.dumps(jsonable_encoder(data))
#                 state = utility.set_data(key=CACHEKEY.TRIM_DATA+imo, value=data)
#                 if state is True:
#                     print('Cache Set Successfully') 
#         except Exception as e:
#             print(e)
#             print('cache set failure')
#     if data:
#         data = json.loads(data)

#     return data
from pydantic import BaseSettings
# from dotenv import load_dotenv
import os

# load_dotenv()

  

# class REDISCACHE(BaseSettings):
#     PASSWORD: str = os.environ["REDIS_PASSWORD"]
#     HOST:  str = os.environ["REDIS_HOST"]
#     PORT:  str = os.environ["REDIS_PORT"]
#     SOCKET_TIMEOUT : int = os.environ["REDIS_SOCKET_TIMEOUT"]
#     DB : int = os.environ["REDIS_DB"]

class POSTGRESDB(BaseSettings):
    USERNAME1:  str = 'postgres'
    PASSWORD: str = 'admin'
    HOST:  str = 'localhost'
    PORT:  str = '5432'
    SCHEMA: str = 'local_client'
    
  
# class TWILIO_CRED(BaseSettings):
#     ACCOUNT_SID = os.getenv("ACCOUNT_SID")
#     AUTH_TOKEN = os.getenv("AUTH_TOKEN")
#     YOUR_TWILIO_PHONE_NUMBER = os.getenv("YOUR_TWILIO_PHONE_NUMBER")    

# # class STRAPIDB(BaseSettings):
# #     URL: str =  os.environ["STRAPI_URL"]
# #     IDENTIFIER: str =  os.environ["STRAPI_IDENTIFIER"]
# #     PASSWORD: str =  os.environ["STRAPI_PASSWORD"]

# # class VDMDB(BaseSettings):
# #     USERNAME1:  str = "analytic_user"
# #     PASSWORD: str = "bVArxruwE9RbyxnyS@Y"
# #     HOST:  str = "mscsmvdm-prod.c9jsnq2znqag.eu-west-1.rds.amazonaws.com" 
# #     PORT:  str = "SYSYEM API"
# #     SCHEMA:str = "mscsmvdm_vms"
    
# # class SETTINGS(BaseSettings):
# #     CLIENT: str = os.environ["CLIENT_NAME"] + "_"
# #     CACHE_EXPIRY_IN_SECONDS: int = CLIENT + os.environ["CACHE_EXPIRY_IN_SECONDS"] #SECONDS

# # class CACHEKEY(BaseSettings):
# #     CLIENT: str = os.environ["CLIENT_NAME"] + "_"
# #     TRIM_DATA: str = CLIENT + os.environ["CACHE_TRIM_DATA"]


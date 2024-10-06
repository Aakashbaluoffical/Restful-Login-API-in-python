from fastapi import APIRouter,Depends , Cookie
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from storage.database import get_db
from storage import querydata
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials #jwt
from twilio.rest import Client
from common.configuration import TWILIO_CRED
import json
import smtplib
import logging
import jwt   #jwt 
import random


from email.mime.text import MIMEText




router = APIRouter(prefix="",
                   tags=["Login"])


TWILIO_CRED = TWILIO_CRED()



# ============== Twilio =============================
client = Client(TWILIO_CRED.ACCOUNT_SID,TWILIO_CRED.AUTH_TOKEN)
print(f"Twilio cred: Account sid: {TWILIO_CRED.ACCOUNT_SID}, Token: {TWILIO_CRED.AUTH_TOKEN}, Mobile number : {TWILIO_CRED.YOUR_TWILIO_PHONE_NUMBER}")
# -------------

def genarate_otp(Length=6):
   otp = random.randint(10**(Length-1), (10**Length)-1)
   return otp

def send_otp(user_mobile_number):
    otp = genarate_otp()
    print("OTP:",otp)
    print("TWILIO_CRED.YOUR_TWILIO_PHONE_NUMBER:",TWILIO_CRED.YOUR_TWILIO_PHONE_NUMBER)
    print("user_mobile_number:",user_mobile_number)


    
    
    message = client.messages.create(
        body=f'Your OTP is {otp}.',
        from_=TWILIO_CRED.YOUR_TWILIO_PHONE_NUMBER,
        to=f"+91{user_mobile_number}"
    )
    print(f"OTP sent to {user_mobile_number}: {otp}")
    return otp
    
# ===================================================

#======= Manual Entries =====================================
blocking_minutes = 1
blocking_seconds = 10
#===========================================================

def send_email_otp():
    otp = genarate_otp()
    from_address = ''
    to_address = ''#'
    password = ''
    subject = "Restful Login Verification Code"
    body = 'Your OTP is '+str(otp) +'.'
    
    port = 587
    # server = 'outlook.office365.com' #microsoft
    smtp_server = 'smtp.gmail.com' #gmail
    
    msg = MIMEText(body)
    
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Identify the client to the server
    server.starttls()  # Upgrade the connection to a secure encrypted TLS connection
    server.ehlo()
    
    server.login(from_address, password)
    
    

    try:
        server.sendmail(from_address, to_address, msg.as_string())
    except Exception as e:
        logging.error(str(e))

    server.quit()
    
    return  otp
# ========================================

  



    
    
    response = JSONResponse(content={"message": "OTP sent!"})
    response.set_cookie(key='otp',value=str(otp),httponly=True)
    return response
    #----------------------------------------------------




@router.post("/api/v1/login")
def login(username:str = None,password:str = None, db:Session = Depends(get_db)):
    print("Here is your entered Username:",username,"and Password:",password)
    if (username== 'undefined' and password== 'undefined'):
        return JSONResponse(status_code=400,content={"data": "Invalid!"})
    if (username == None  and password == None) or (username == ""  and password == ""):
        return JSONResponse(status_code=400,content ={"data": "Please enter your Username & Password."})
    if (username == None and username== 'undefined')or (username == ""):
        return JSONResponse(status_code=400,content={"data": "Please enter your Username."})
    if (password == None and password== 'undefined') or (password == ""):
        return JSONResponse(status_code=400,content={"data": "Please enter your Password."})
    #--------------Function ---------------------------------------------
    # def homepage(times):
    #     print("count ",times)
    #     return '''Welcome your Home page'''
    
    times = 4
    now_time = datetime.now()
    
    data = querydata.check_user_pass(db,username,password)
    data = json.dumps(jsonable_encoder(data))
    data = json.loads(data)
    if data and data['block'] == 'block':
        return JSONResponse(status_code=423,content={"data":"Account has been permanently suspended "})
    if data and data['block_date_time']=="" :
        return {"data":"Welcome your Home page"}
    if data and data['block_date_time'] and data['times'] !=0: 
        querydata.update_times_after(db,username)
        print("data['block_date_time'] and data['times']",data['block_date_time'], data['times'])
        return {"data":"Welcome your Home page"}
         
    elif username:
        user_check = querydata.check_user(db,username)
        user_check = json.dumps(jsonable_encoder(user_check))
        user_check = json.loads(user_check)
        if user_check :
            if user_check['times']!=0 :
                times = user_check['times']-1
                querydata.update_times(db,times,username,now_time)
                return JSONResponse(status_code=401,content={"data":f"Incorrect Password, {user_check['times']} more changes"})
            else:
                user_check = querydata.check_user(db,username)
                user_check = json.dumps(jsonable_encoder(user_check))
                user_time_check = json.loads(user_check)
                if user_time_check['block_date_time'] != "":
                    block_date_time =datetime.strptime(user_time_check['block_date_time'], "%Y-%m-%dT%H:%M:%S.%f")
                    # new_block_date = block_date_time + relativedelta(minutes=blocking_minutes)
                    new_block_date = block_date_time + relativedelta(seconds=blocking_seconds)
                    
                    print("now_time",now_time)
                    print("new_block_date",new_block_date)
                    # if user_time_check['block'] == 'clear' and user_time_check['block'] == 'unblock':
                    if now_time > new_block_date :
                        querydata.update_times_after(db,username)
                        return  JSONResponse(status_code=401,content={"data":"Your account is unlocked ,please enter correct password"})
                    else:
                        return JSONResponse(status_code=423,content={"data":"Account is locked due to multiple incorrect attempts. Check after 10 sec"})
                    # else:
                    #      return {"data":"Account has been permanently suspended "}   
                else:
                    blocked_time = datetime.now()
                    querydata.update_only_times(db,username,blocked_time)
                    
                    return JSONResponse(status_code=423,content={"data":"Account is locked due to multiple incorrect attempts. Check after 10 sec"})
        else:
            return JSONResponse(status_code=404, content={"data":"User not found!"})
     
     
@router.post("/api/v1/login/email/{email}")
def login(email:str = None,otp:int = None, db:Session = Depends(get_db)): 
    
    if otp is None:
        if email is not None:
            user_check = querydata.check_user_email(db,email)
            if user_check:
                print("before ===============")
                otp = send_email_otp()
                return otp
            else:
                return 0
 
     
     
@router.post("/api/v1/login/otp/{user_mobile_number}")
def login(user_mobile_number:str = None,otp:int = None, db:Session = Depends(get_db)):
    print("Please enter your Mobile no:",user_mobile_number)
    number_lenth_list = list(user_mobile_number)
    
    
    if otp is None:
        if (user_mobile_number== 'undefined'):
            return JSONResponse(status_code=400,content={"data": "Invalid!"})    
        if len(number_lenth_list)>=10:
            otp = send_otp(user_mobile_number)
            response = JSONResponse(content={"message": "OTP sent!"})
            response.set_cookie(key='otp',value=str(otp),httponly=True)
            return response
        else:
            return JSONResponse(status_code=400,content={"data": "Mobile no: less than 10 digit"})
   
from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from storage.database import get_db
from storage import querydata
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials #jwt
import json
import smtplib
import logging
import jwt   #jwt 



router = APIRouter(prefix="",
                   tags=["Login"])


@router.post("/api/v1/login")
def login(username:str = None,password:str = None, db:Session = Depends(get_db)):
    print("Here is your entered Username:",username,"and Password:",password)
    if (username== 'undefined' and password== 'undefined'):
        return {"data": "Invalid!"}
    if (username == None  and password == None) or (username == ""  and password == ""):
        return {"data": "Please enter your Username & Password."}
    if (username == None and username== 'undefined')or (username == ""):
        return {"data": "Please enter your Username."}
    if (password == None and password== 'undefined') or (password == ""):
        return {"data": "Please enter your Password."}
    #--------------Function ---------------------------------------------
    # def homepage(times):
    #     print("count ",times)
    #     return '''Welcome your Home page'''
    def alert_mail(mail_subject,mail_body,to_address_mail_id,from_address_mail_id,from_address_mail_password):
        from_address = from_address_mail_id
        to_address = [to_address_mail_id]#'
        password = from_address_mail_password
        subject = mail_subject
        body = mail_body
        msg = f"Subject: {subject}\n\n{datetime}\n{body}"
        port = 587
        server = 'outlook.office365.com'
        server = smtplib.SMTP(server, port)
        server.starttls()
        server.login(from_address, password)

        try:
            server.sendmail(from_address, to_address, msg)
        except Exception as e:
            logging.error(str(e))

        server.quit()
    #----------------------------------------------------
    times = 4
    now_time = datetime.now()
    
    data = querydata.check_user_pass(db,username,password)
    data = json.dumps(jsonable_encoder(data))
    data = json.loads(data)
    if data and data['block'] == 'block':
        return {"data":"Account has been permanently suspended "}
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
                return {"data":f"Incorrect Password, {user_check['times']} more changes"}
            else:
                user_check = querydata.check_user(db,username)
                user_check = json.dumps(jsonable_encoder(user_check))
                user_time_check = json.loads(user_check)
                if user_time_check['block_date_time'] != "":
                    block_date_time =datetime.strptime(user_time_check['block_date_time'], "%Y-%m-%dT%H:%M:%S.%f")
                    new_block_date = block_date_time + relativedelta(minutes=1)
                    print("now_time",now_time)
                    print("new_block_date",new_block_date)
                    # if user_time_check['block'] == 'clear' and user_time_check['block'] == 'unblock':
                    if now_time > new_block_date :
                        querydata.update_times_after(db,username)
                        return {"data":"Your account is unlocked ,please enter correct password"}
                    else:
                        return {"data":"Account is locked due to multiple incorrect attempts. Check after 1 minites"}
                    # else:
                    #      return {"data":"Account has been permanently suspended "}   
                else:
                    blocked_time = datetime.now()
                    querydata.update_only_times(db,username,blocked_time)
                    
                    return {"data":"Account is locked due to multiple incorrect attempts. Check after 1 minites"}
        else:
            return {"data":"User not found!"}
     
     
     
     
    
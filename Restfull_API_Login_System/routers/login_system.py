from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from storage.database import get_db
from storage import querydata
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta



# CACHEKEY = CACHEKEY()

router = APIRouter(
      prefix="",
      tags=["SpeedLoss"],
      )

router = APIRouter(prefix="",
                   tags=["Login"])


@router.post("/api/v1/login")
def login(username:str = None,password:str = None, db:Session = Depends(get_db)):
    print("Here is your entered Username:",username,"and Password:",password)
    if (username== 'undefined' and password== 'undefined'):
        return '''Invalid!'''
    if (username == None  and password == None) or (username == ""  and password == ""):
        return '''Please enter your Username & Password.'''
    if (username == None and username== 'undefined')or (username == ""):
        return '''Please enter your Username.'''
    if (password == None and password== 'undefined') or (password == ""):
        return '''Please enter your Password.'''
    #--------------Function ---------------------------------------------
    # def homepage(times):
    #     print("count ",times)
    #     return '''Welcome your Home page'''
    
    times = 4
    now_time = datetime.now()
    
    data = querydata.check_user_pass(db,username,password)
    data = json.dumps(jsonable_encoder(data))
    data = json.loads(data)
    print("data",data) 
    if data and data['block_date_time']=="":
        return '''Welcome your Home page'''
    if data and data['block_date_time'] and data['times'] !=0: 
        querydata.update_times_after(db,username)
        print("data['block_date_time'] and data['times']",data['block_date_time'], data['times'])
        return '''Welcome your Home page'''
         
    elif username:
        user_check = querydata.check_user(db,username)
        user_check = json.dumps(jsonable_encoder(user_check))
        user_check = json.loads(user_check)
        if user_check :
            if user_check['times']!=0:
                times = user_check['times']-1
                querydata.update_times(db,times,username,now_time)
                return f"Incorrect Password, {user_check['times']} more changes"
            else:
                user_check = querydata.check_user(db,username)
                user_check = json.dumps(jsonable_encoder(user_check))
                user_time_check = json.loads(user_check)
                if user_time_check['block_date_time'] != "":
                    block_date_time =datetime.strptime(user_time_check['block_date_time'], "%Y-%m-%dT%H:%M:%S.%f")
                    new_block_date = block_date_time + relativedelta(minutes=1)
                    print("now_time",now_time)
                    print("new_block_date",new_block_date)
                    
                    if now_time > new_block_date :
                        querydata.update_times_after(db,username)
                        return """Your account is unlocked ,please enter correct password"""
                    else:
                        return """Account is locked due to multiple incorrect attempts. Check after 5 minites"""
                else:
                    blocked_time = datetime.now()
                    querydata.update_only_times(db,username,blocked_time)
                    return """Account is locked due to multiple incorrect attempts. Check after 5 minites"""
        else:
            return "User not found!"
     
     
     
     
    
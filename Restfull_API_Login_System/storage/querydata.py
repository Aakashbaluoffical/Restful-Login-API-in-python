from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from sqlalchemy import String, cast,Integer ,Date ,Float
from sqlalchemy.orm import Session

from datetime import date, datetime, timedelta
from models import properties_models



def check_user(db:Session,username):
    return db.query(properties_models.User).filter(properties_models.User.username == username).first()


def check_user_pass(db:Session,username,password):
    return db.query(properties_models.User).filter(properties_models.User.username == username,properties_models.User.password == password).first()

def update_times(db:Session,times,username,now_time):
    print("times",times,now_time)
    
    update = db.query(properties_models.User).filter(properties_models.User.username == username).update({'times':times,'block_date_time':now_time})
    db.commit()
    return update

def update_only_times(db:Session,username,blocked_time):
    update = db.query(properties_models.User).filter(properties_models.User.username == username).update({'block_date_time':blocked_time})
    db.commit()
    return update





def update_times_after(db:Session,username):
    update = db.query(properties_models.User).filter(properties_models.User.username == username).update({'times':'3'})
    db.commit()
    return update

def update_block(db:Session,username):
    update = db.query(properties_models.User).filter(properties_models.User.username == username).update({'block':'block'})
    db.commit()
    return update
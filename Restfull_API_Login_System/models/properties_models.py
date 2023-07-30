from datetime import date
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Date
from sqlalchemy.orm import relationship

from storage.database import Base

class User(Base):
    __tablename__ = "user_tbls"  

    id = Column(Integer, primary_key=True, index=True)
    username =  Column (String)
    password =  Column (String)
    email =  Column (String)
    status =  Column (String)
    mobile_no =  Column (Integer)
    type =  Column (String)
    block =  Column (String)
    times =  Column (Integer) 
    block_date_time =  Column (Date) 
    
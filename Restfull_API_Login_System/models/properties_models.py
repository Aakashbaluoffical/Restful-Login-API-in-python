from datetime import date
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Date
from sqlalchemy.orm import relationship

from storage.database import Base

class CFDResults(Base):
    __tablename__ = "an_cfd_results"

    id = Column(Integer, primary_key=True, index=True)
    imo =  Column (String)
    draft =  Column (String)
    speed =  Column (String)
    trim =  Column (String)
    resistance =  Column (String)
    power =  Column (String)
    
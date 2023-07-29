from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from sqlalchemy import String, cast,Integer ,Date ,Float
from sqlalchemy.orm import Session

from datetime import date, datetime, timedelta
from models import properties_models


def get_trim_data(db:Session,imo):
    return db.query(properties_models.CFDResults).filter(properties_models.CFDResults.imo == imo).all()


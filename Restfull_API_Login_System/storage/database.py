from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from common.configuration import POSTGRESDB


POSTGRESDB = POSTGRESDB()
SQLALCHEMY_DATABASE_URL_LOCAL = "postgresql://"+ POSTGRESDB.USERNAME1 +":"+ POSTGRESDB.PASSWORD +"@"+ POSTGRESDB.HOST +"/" + POSTGRESDB.SCHEMA
print(SQLALCHEMY_DATABASE_URL_LOCAL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL_LOCAL,pool_size=20, max_overflow=30
)
SessionLocal_db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal_db()
    try:
        yield db
    finally:
        db.close() 

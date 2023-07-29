from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from common.configuration import POSTGRESDB


#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
POSTGRESDB = POSTGRESDB()
SQLALCHEMY_DATABASE_URL = "postgresql://"+ POSTGRESDB.POSTGRES_USERNAME +":"+ POSTGRESDB.PASSWORD.replace("@", "%40") +"@"+ POSTGRESDB.HOST +"/" + POSTGRESDB.SCHEMA 

print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=30
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

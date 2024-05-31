from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://abdullah:password@localhost/fastapi'
# SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@host/db'

# sql lite needs connection args
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':  False}
# )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import yaml

with open('config.yaml') as f:
    SQLALCHEMY_DATABASE_URL = yaml.safe_load(f)['SQLALCHEMY_DATABASE_URL']

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) # On sqlite
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) # On non sqlite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
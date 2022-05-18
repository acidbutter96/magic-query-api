from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.dotenv import config

SQLALCHEMY_DATABASE_URL = f"postgresql://{config['DATABASE_USER']}:{config['DATABASE_PASSWORD']}@{config['DATABASE_SERVER']}:{config['DATABASE_PORT']}/{config['DATABASE_NAME']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoFlush=False,
                            bind=engine
                )

Base = declarative_base()

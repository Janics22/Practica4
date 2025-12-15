import os
from typing import Annotated

import sqlalchemy
from fastapi import Depends
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

IS_PROD = ["true", "1"]

def get_engine() -> Engine:
    return get_prod_engine() if is_production() else get_dev_engine()

def get_prod_engine() -> Engine:
    if not all_env_vars_set():
        raise EnvironmentError("One or more required environment variables are not set for production database connection.")

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    postgre_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    print("Using production PostgreSQL database.")
    return create_engine(postgre_url)

def get_dev_engine() -> Engine:
    sqlite_file = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file}"
    connect_args = {"check_same_thread": False}
    print("Using development SQLite database.")
    return create_engine(sqlite_url, echo=True, connect_args=connect_args)

def is_production() -> bool:
    prod: str | None = os.getenv("PROD", "false")
    prod = prod.lower()
    return prod in IS_PROD

def all_env_vars_set() -> bool:
    required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    return all(os.getenv(var) is not None for var in required_vars)

def create_db_and_tables():
    try:
        engine = get_engine()
        SQLModel.metadata.create_all(engine)
    except sqlalchemy.exc.OperationalError as e:
        raise ConnectionError("Failed to connect to the production database. Some of the environment variables might are probably incorrect") from e

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

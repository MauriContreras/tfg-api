from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

db_params = {
    'dbname': 'omop54',
    'user': 'lucia_researcher',
    'password': '3y%P@zQ9hur4zsV$8f',
    'host': 'omop',
    'port': '5432'
}

password_encoded = quote_plus(db_params["password"])
engine = create_engine(f"postgresql://{db_params['user']}:{password_encoded}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

api_keys = {
    "e54d4431-5dab-474e-b71a-0db1fcb9e659": "7oDYjo3d9r58EJKYi5x4E8",
    "5f0c7127-3be9-4488-b801-c7b6415b45e9": "mUP7PpTHmFAkxcQLWKMY8t"
}

users = {
    "7oDYjo3d9r58EJKYi5x4E8": {
        "name": "Bob"
    },
    "mUP7PpTHmFAkxcQLWKMY8t": {
        "name": "Alice"
    },
}

def check_api_key(api_key: str):
    return api_key in api_keys

def get_user_from_api_key(api_key: str):
    return users[api_keys[api_key]]



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
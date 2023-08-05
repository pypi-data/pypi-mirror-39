from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import config

__ssssion_map = {}


def get_sqlalchemy_connection_address(label, database):
    host = config(label, 'host')
    port = config(label, 'port')
    user = config(label, 'user')
    password = config(label, 'password', '')
    if password == '':
        password = config(label, 'pass', '')
    return "mysql://%s:%s@%s:%s/%s" % (user, password, host, port, database)


def get_sqlalchemy_session(label, database):
    global __ssssion_map
    label1 = label + database
    if label1 in __ssssion_map:
        return __ssssion_map[label1]
    log_level = config('settings', 'log_level', 'debug')
    engine = create_engine(get_sqlalchemy_connection_address(label, database), echo=(log_level == 'debug'))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    __ssssion_map[label1] = session
    return session


def close_sqlalchemy_session(label,database):
    label1 = label + database
    global __ssssion_map
    if label in __ssssion_map:
        try:
            __ssssion_map[label1].close()
        finally:
            del __ssssion_map[label1]


Base = declarative_base()


class BaseModel:
    __label__ = None
    __database__ = None

    @classmethod
    def get_session(cls):
        return get_sqlalchemy_session(cls.__label__, cls.__database__)

    @classmethod
    def close_session(cls):
        close_sqlalchemy_session(cls.__label__, cls.__database__)

    @classmethod
    def save(cls, o):
        session = cls.get_session()
        session.add(o)
        session.commit()

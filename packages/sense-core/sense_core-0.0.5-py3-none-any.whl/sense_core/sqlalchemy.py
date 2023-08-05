from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import config
from .log import *

__engine_map = {}


def get_sqlalchemy_connection_address(label, database):
    host = config(label, 'host')
    port = config(label, 'port')
    user = config(label, 'user')
    password = config(label, 'password', '')
    if password == '':
        password = config(label, 'pass', '')
    return "mysql://%s:%s@%s:%s/%s" % (user, password, host, port, database)


def _get_sqlalchemy_engine(label, database):
    global __engine_map
    label1 = label + database
    if label1 in __engine_map:
        return __engine_map[label1]
    log_level = config('settings', 'log_level', 'debug')
    engine = create_engine(get_sqlalchemy_connection_address(label, database), echo=(log_level == 'debug'))
    __engine_map[label1] = engine
    return engine


def get_sqlalchemy_session(label, database):
    engine = _get_sqlalchemy_engine(label, database)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def close_sqlalchemy_session(session):
    try:
        session.close()
    except:
        pass


Base = declarative_base()


class BaseModel:
    __label__ = None
    __database__ = None

    @classmethod
    def get_session(cls):
        return get_sqlalchemy_session(cls.__label__, cls.__database__)

    @classmethod
    def close_session(cls, session):
        if session is None:
            return
        close_sqlalchemy_session(session)

    @classmethod
    def save(cls, o, session=None):
        session1 = session
        if not session1:
            session1 = cls.get_session()
        session1.add(o)
        session1.commit()
        if not session:
            session1.close()

    @classmethod
    def get_by_field(cls, field, value, session=None):
        try:
            session1 = session
            if not session1:
                session1 = cls.get_session()
            item = session1.query(cls).filter(field == value).first()
            if not session:
                session1.close()
            return item
        except Exception as ex:
            log_exception(ex)
            return None

    @classmethod
    def get_by_id(cls, id, session=None):
        return cls.get_by_field(cls.id, id, session)

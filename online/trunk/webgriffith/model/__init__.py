"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from webgriffith.model import meta
from webgriffith.model.db import *

def init_model(engine):

    sm = orm.sessionmaker(bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)


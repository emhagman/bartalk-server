from sqlalchemy import *
import json
import datetime
from django.http import HttpResponse


class Database:
    def __init__(self):
        print('init db')

    # connect to the Database
    meta = MetaData()
    engine = None
    connection = None

    # set the table up
    drinker = \
        Table('drinker',
              meta,
              Column('id', Integer, primary_key=True),
              Column('name', String(32), nullable=False),
              Column('email', String(512), nullable=False, unique=True),
              Column('birthday', Date, nullable=False),
              Column('password', String(512), nullable=False),
              Column('created', Date, default=datetime.datetime.now()))

    bar = \
        Table('bar',
              meta,
              Column('id', Integer, primary_key=True),
              Column('name', String(32)),
              Column('description', String(512)),
              Column('latitude', Float),
              Column('longitude', Float),
              Column('google_id', String(64), unique=True, nullable=False),
              Column('created', Date, default=datetime.datetime.now()))

    # create all the tables and clear the data
    @staticmethod
    def reset_database():

        # drop the tables
        meta = MetaData(Database.engine)
        meta.reflect()
        meta.drop_all()

        # create all the tables
        Database.create_drinker_table()
        Database.create_bar_table()

    # connect to the clio Database
    @staticmethod
    def connect():

        # first define the connection if it doesnt exist
        if Database.engine is None:
            Database.engine = \
                create_engine('postgresql://localhost:5432/bartalk', pool_size=20, max_overflow=0)

        # connect to our Database
        Database.connection = Database.engine.connect()

    # disconnec
    @staticmethod
    def disconnect():
        Database.engine.disconnect()

    # method to create the user table (and update it if necessary)
    # dont call this unless you want to lose all of your data
    @staticmethod
    def create_drinker_table():

        # drop then recreate the table
        Database.drinker.drop(Database.engine, checkfirst=True)
        Database.drinker.create(Database.engine)

    # create the location structure
    @staticmethod
    def create_bar_table():

        Database.bar.drop(Database.engine, checkfirst=True)
        Database.bar.create(Database.engine)

    # array
    @staticmethod
    def array(arr, filter=None):
        if not filter:
            return [dict(a) for a in arr]
        else:
            narr = []
            for a in arr:
                a = dict(a)
                for f in filter:
                    del a[f]
                narr.append(a)
            return narr

    # object
    @staticmethod
    def object(obje):
        date_handler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) else None
        return json.dumps(obje, default=date_handler)

    # error
    @staticmethod
    def error(msg):
        return HttpResponse(Database.object({'success': False, 'message': msg}), content_type="application/json")

    # errors
    @staticmethod
    def errors(errs):
        return HttpResponse(Database.object({'success': False, 'errors': errs}), content_type="application/json")

    # success
    @staticmethod
    def success(msg):
        return HttpResponse(Database.object({'success': True, 'message': msg}), content_type="application/json")
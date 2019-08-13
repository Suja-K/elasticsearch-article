import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

TO_INSERT = [
    {'name': 'First', 'text': 'MIDWAY upon the journey of our life'},
    {'name': 'Second', 'text': 'I found myself within a forest dark,'},
    {'name': 'Third', 'text': 'For the straightforward pathway had been lost.'},
    {'name': 'Fourth', 'text': 'Ah me! how hard a thing it is to say'},
    {'name': 'Fifth', 'text': 'What was this forest savage, rough, and stern,'},
    {'name': 'Sixth', 'text': 'Which in the very thought renews the fear.'},
    {'name': 'Seventh', 'text': 'So bitter is it, death is little more;'},
    {'name': 'Eighth', 'text': 'But of the good to treat, which there I found,'},
    {'name': 'Ninth', 'text': 'Speak will I of the other things I saw there.'},
    {'name': 'Tenth', 'text': 'I cannot well repeat how there I entered,'},
]

engine = create_engine('postgresql://{}:{}@db:5432/{}'.format(os.environ['POSTGRES_USER'],
                                                              os.environ['POSTGRES_PASSWORD'],
                                                              os.environ['POSTGRES_DB']),
                       echo=True)

metadata = MetaData()
post = Table('post', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String),
             Column('text', String))
metadata.create_all(engine)

conn = engine.connect()
conn.execute(post.insert(), TO_INSERT)

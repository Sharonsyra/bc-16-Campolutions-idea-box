import sys 

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):


	__tablename__ = 'user'

	id = Column(Integer, primary_key = True, autoincrement = True)
	name = Column(String(80), nullable = False)
	username = Column(String(80), nullable = False)
	email = Column(String(100), nullable = True)
	password = Column(String)

class Ideas(Base):

	__tablename__ = 'idea'

	id = Column(Integer, primary_key = True, autoincrement = True)
	name = Column(String(80), nullable = False)
	description = Column(String(250), nullable = False)
	rating = Column(String(8), nullable = False)
	category = Column(String(250), nullable = False)
	tags = Column(String(250))
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

class Comments(Base):

	__tablename__ = 'comments'

	id = Column(Integer, primary_key = True, autoincrement = True)
	comment = Column(String(250), nullable = True)
	idea_id = Column(Integer, ForeignKey('idea.id'))
	user_id = Column(Integer, ForeignKey('user.id'))
		
#end of file code
engine = create_engine('sqlite:///userideas.db')
Base.metadata.create_all(engine)
from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Ideas, Comments

engine = create_engine('sqlite:///userideas.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/users/<int:user_id>/')
def user(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	idea = session.query(Ideas).filter_by(user_id = user.id)
	output = ''
	for i in idea:
		output += i.name
		output += '</br>'
		output += i.description
		output += '</br>'
		output += i.category
		output += '</br>'
		output += i.tags
		output += '</br>'
		output += '</br>'

	return output

def newIdea(user_id):
	return "page to create new idea"

def editIdea(user_id, idea_id):
	return "page to edit an idea"

def deleteIdea():
	return "Page to delete idea"

if __name__ == '__main__':
 	app.run(debug = True)
from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Ideas

engine = create_engine('sqlite:///i.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
	user = session.query(User).first()
	idea = session.query(Ideas).filter_by(user_id = user.id)
	output = ''
	for i in idea:
		output += i.name
		output += '</br>'
	return output



if __name__ == '__main__':
	app.run(debug = True)
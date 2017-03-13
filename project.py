from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Ideas, Comments

engine = create_engine('sqlite:///userideas.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def DefaultUser():
	user = session.query(User).first()
	idea = session.query(Ideas).filter_by(user_id = user_id)

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

@app.route('/users/<int:user_id>/')
def user(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	idea = session.query(Ideas).filter_by(user_id = user.id)
	return render_template('user.html', user = user, idea = idea)

@app.route('/users/<int:user_id>/new/', methods = ['GET', 'POST'])
def newIdea(user_id):
	if request.method == 'POST':
		newIdea = Ideas(name = request.form['name'], user_id = user_id)
		session.add(newIdea)
		session.commit()
		return redirect(url_for('user', user_id = user_id)) 
	else:
		return render_template('newIdea.html', user_id = user_id)
@app.route('/users/<int:user_id>/edit/')
def editIdea(user_id, idea_id):
	return "page to edit an idea"

@app.route('/users/<int:user_id>/<int:idea_id>/delete/')
def deleteIdea():
	return "Page to delete idea"

if __name__ == '__main__':
 	app.run(debug = True)
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Ideas, Comments

engine = create_engine('sqlite:///userideas.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()
app.secret_key = "my_key"

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        name = request.form['inputName']
        username = request.form['inputUserName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        newUser = User(name = name, username = username, email = email, password = password)
        session.add(newUser)
        session.commit()
        return redirect(url_for('signin'))
    
@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        checkUser = session.query(User).filter_by(email = email)
        if not checkUser:
            flash("Invalid email!")
            return render_template("signin.html")

        checkPassword = session.query(User).filter_by(email == email and password == password)
        if not checkPassword:
            flash("Invalid credentials!")
            return render_template("signin.html")
        return render_template("ideabox.html")

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/ideas')
def DefaultUser():
    user = session.query(User).first()
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

@app.route('/users/<int:user_id>/')
def user(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    idea = session.query(Ideas).filter_by(user_id = user.id)
    return render_template('user.html', user = user, idea = idea)

@app.route('/users/<int:user_id>/new/', methods = ['GET','POST'])
def newIdea(user_id):
    if request.method == 'POST':
        newIdea = Ideas(name = request.form['name'], user_id = user_id)
        session.add(newIdea)
        session.commit()
        flash("new Idea created!")
        return redirect(url_for('user', user_id = user_id)) 
    else:
        return render_template('newIdea.html', user_id = user_id)

@app.route('/users/<int:user_id>/<int:idea_id>/edit/', methods = ['GET','POST'])
def editIdea(user_id, idea_id):
    editedIdea = session.query(Ideas).filter_by(id = idea_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedIdea.name = request.form['name']
        session.commit()
        flash("Idea has been edited ")
        return redirect(url_for('user', user_id = user_id))
    else:
        return render_template('editIdea.html', user_id = user_id, idea_id = id, i = editedIdea)
    
@app.route('/users/<int:user_id>/<int:idea_id>/delete/', methods = ['GET', 'POST'])
def deleteIdea(user_id, idea_id):
    deletedIdea = session.query(Ideas).filter_by(id = idea_id).one()
    if request.method == 'POST':
        session.delete(deletedIdea)
        session.commit()
        flash("Idea has been deleted")
        return redirect(url_for('user', user_id = user_id))
    else:
        return render_template('deleteIdea.html', user_id = user_id, idea_id = id, i = deletedIdea)

if __name__ == '__main__':
    app.run(debug = True)

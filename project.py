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

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call the MySQL

            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    _hashed_password = generate_password_hash(_password)
                    cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
                    data = cursor.fetchall()

                    if len(data) is 0:
                        conn.commit()
                        return json.dumps({'message':'User created successfully !'})
                    else:
                        return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        # validate the received values
        if _username and _password:

            # All Good, let's call the MySQL

            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.callproc('sp_validateLogin',(_username))
                    data = cursor.fetchall()

                    if len(data) > 0:
                        if check_password_hash(str(data[0][3]),_password):
                            session['user'] = data[0][0]
                            return redirect('/userHome')
                        else:
                            return render_template('error.html',error = 'Wrong Email address or Password.')
                    else:
                        return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

 
    except Exception as e:
        return render_template('error.html',error = str(e))

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
    print("My new idea", editedIdea)
    if request.method == 'POST':
        if request.form['name']:
            editedIdea.name = request.form['name']
        session.commit()
        flash("Idea has been edited ")
        return redirect(url_for('user', user_id = user_id))
    else:
        return render_template('editIdea.html', user_id = user_id, idea_id = id, i = editedIdea)
    
@app.route('/users/<int:user_id>/<int:idea_id>/delete/', methods = ['GET', 'DELETE'])
def deleteIdea(user_id, idea_id):
    deletedIdea = session.query(Ideas).filter_by(id = idea_id).one()
    print("This is the deleted idea:", deletedIdea) 
    if request.method == 'POST':
        session.delete(deletedIdea)
        session.commit()
        flash("Idea has been deleted")
        return redirect(url_for('user', user_id = user_id))
    else:
        return render_template('deleteIdea.html', user_id = user_id, idea_id = id, i = deletedIdea)

if __name__ == '__main__':
    app.run(debug = True)


import os
from flask import render_template, redirect, url_for
from flask_user import login_required, roles_required
from flask_login import logout_user, current_user

#import database tables
from create_database import app, User, Accounts

from flask_restless import APIManager, ProcessingException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOST = "0.0.0.0"
PORT = 5000

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def user_auth(*args, **kwargs):
    con = engine.connect()
    role = con.execute("SELECT name FROM role WHERE id = (SELECT role_id FROM user_roles WHERE user_id == {})".format(current_user.id))
    role = role.first()[0]
    con.close()
    if role != 'admin':
        raise ProcessingException(description='Not authenticated!', code=401)

def account_auth(*args, **kwargs):
    con = engine.connect()
    role = con.execute("SELECT name FROM role WHERE id = (SELECT role_id FROM user_roles WHERE user_id == {})".format(current_user.id))
    role = role.first()[0]
    con.close()
    if not role in ("developer", "admin"):
        raise ProcessingException(description='Not authenticated!', code=401)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.sqlite")
engine = create_engine('sqlite:///{}'.format(DATABASE_PATH))

Session = sessionmaker(bind = engine)
sesh = Session()
MANAGER = APIManager(app, session=sesh)

user_api_settings = dict(POST = [user_auth],
						  GET_SINGLE = [user_auth],
						  GET_MANY = [user_auth],
						  PATCH_SINGLE = [user_auth],
						  PATCH_MANY = [user_auth],
						  DELETE_SINGLE = [user_auth],
						  DELETE_MANY = [user_auth])
		
account_api_settings = dict(POST = [account_auth],
						    GET_SINGLE = [account_auth],
						    GET_MANY = [account_auth],
						    PATCH_SINGLE = [account_auth],
						    PATCH_MANY = [account_auth],
						    DELETE_SINGLE = [account_auth],
						    DELETE_MANY = [account_auth])

# only admin can see user api							   
MANAGER.create_api(User, methods = ['GET', 'POST', 'PATCH', 'DELETE'], preprocessors=user_api_settings)

# admin and developer can see Accounts API
MANAGER.create_api(Accounts, methods = ['GET', 'POST', 'PATCH', 'DELETE'], preprocessors=account_api_settings)

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/members')
@login_required
#https://pythonhosted.org/Flask-User/authorization.html#roles-required
# @roles_required('admin')
def members_page():
    return render_template('members_page.html', accounts=sesh.query(Accounts).all(), user_info=sesh.query(User).filter(User.username == current_user.username))

@app.route('/logout')
def logout():
	#can pop the user_id from the session but the logout_user() is cleaner
	# sesh.pop('user_id', None)
    logout_user()
    return redirect(url_for('home_page'))
    
# Start development web server
if __name__=='__main__':
    app.run(host=HOST, port=PORT)

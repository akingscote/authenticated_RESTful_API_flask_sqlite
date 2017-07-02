import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import SQLAlchemyAdapter, UserManager, UserMixin
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_NAME = 'database'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}.sqlite'.format(DATABASE_NAME)

SECRET_KEY = 'THIS IS AN INSECURE SECRET'
SQLALCHEMY_TRACK_MODIFICATIONS  = True
app = Flask(__name__)
app.config.from_object(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User data model. Make sure to add flask_user UserMixin
# as we are using db.Model, the members until it runs so pylint cannot detect it
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # User authentication information
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, server_default='')

    # User email information
    email = db.Column(db.String, nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String, nullable=False, server_default='')
    last_name = db.Column(db.String, nullable=False, server_default='')
    house_number = db.Column(db.Integer) 
    street_name = db.Column(db.String)
    postcode = db.Column(db.String)

    # Relationships
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String)

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
	
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    #address info
    number = db.Column(db.Integer)
    street_name = db.Column(db.String)
    postcode = db.Column(db.String)

	#contacts into
    total_contracts = db.Column(db.Integer)
	
# Reset all the database tables
db.create_all()
	
# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db,  User)
user_manager = UserManager(db_adapter, app)

if __name__ == '__main__':
	# commit now because otherwise the role wont exist ready for the default user
    db.session.commit()

	# user parameters
    admin_user = User(email=r'test@test.com',
                        username='admin',
                        first_name='a',
                        last_name='kingscote',
                        password=app.user_manager.hash_password('password'),
                        active=True,
                        confirmed_at=datetime.datetime.utcnow(),
                        house_number = 27,
                        street_name = 'Python Drive',
                        postcode = 'PY27 4EVA'
						)

	# create an admin role and give it to the admin user
    admin_user.roles.append(Role(name='admin'))
    db.session.add(admin_user)

    developer_user = User(email=r'test2@test.com',
                        username='developer',
                        first_name='a',
                        last_name='kingscote',
                        password=app.user_manager.hash_password('password'),
                        active=True,
                        confirmed_at=datetime.datetime.utcnow(),
                        house_number = 27,
                        street_name = 'Python Drive',
                        postcode = 'PY27 4EVA'
                        )

	# create a developer role and give it to the developer user
    developer_user.roles.append(Role(name='developer'))
    db.session.add(developer_user)
	
	
    standard_user = User(email=r'test3@test.com',
                        username='standard',
                        first_name='a',
                        last_name='kingscote',
                        password=app.user_manager.hash_password('password'),
                        active=True,
                        confirmed_at=datetime.datetime.utcnow(),
                        house_number = 27,
                        street_name = 'Python Drive',
                        postcode = 'PY27 4EVA'
                        )

	# create a standard role and give it to the standard user
    standard_user.roles.append(Role(name='standard'))
    db.session.add(standard_user)
	
	
    account1 = Accounts(name="account1",
                        number=5,
                        street_name="fake street",
                        postcode="PY4 LYF",
                        total_contracts=10)
	
    db.session.add(account1)
    db.session.commit()

#
# Imports 
#
from flask import Flask   
# for flask, and for rendering html templates, flash to display, redirect to get url redict
from flask_sqlalchemy import SQLAlchemy 


#
# Flask Config
#
app = Flask(__name__)   # the name of the module
app.config['SECRET_KEY']='HAHAHAHA'    # currently empty string, but should be empty string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SESSION_COOKIE_NAME"] = "spot app cookie"

#
# Database config
#
db = SQLAlchemy(app)

from LiveToPlay import routes
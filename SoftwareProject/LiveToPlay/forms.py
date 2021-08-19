from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LookUpForm(FlaskForm):
	url = StringField('URL', validators=[DataRequired(), Length(min=10, max=500)])
	submit = SubmitField('Search')
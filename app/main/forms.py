from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp, Optional, Email
from wtforms.fields.html5 import DateField
from ..models import Branch, Employee, Client, Loan

class BranchSearchForm(FlaskForm):
    name = StringField("Branch Name")
    city = StringField("City")
    submit = SubmitField("Search")


class BranchEditForm(FlaskForm):
    name = StringField("Branch Name", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    asset = FloatField("Asset", validators=[InputRequired(), NumberRange(min=0., message='Assest must be greater than 0')])
    submit = SubmitField("Submit")

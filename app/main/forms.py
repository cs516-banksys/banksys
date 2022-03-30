from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp, Optional, Email
from wtforms.fields import DateField
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

### Chengyu Wu
class ClientSearchForm(FlaskForm):
    id = StringField("SSN", validators=[
        Optional(),
        Regexp(r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$', 0,
            "SSN is invalid")
    ])
    name = StringField("Name")
    phone = StringField("Phone Number")
    address = StringField("Address")
    email=StringField("Email")
    contact_name = StringField("Contact Name")
    submit = SubmitField("Search")
    

class ClientEditForm(FlaskForm):
    id = StringField("SSN", validators=[
        InputRequired(),
        Regexp(r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$', 0,
            "SSN is invalid")
    ])
    name = StringField("Name", validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    contact_name = StringField("Contact Name", validators=[InputRequired()])
    contact_phone = StringField("Contact Phone")
    contact_email = StringField("Contact Email", validators=[Optional(), Email()])
    contact_relation = StringField("Contact Relation")
    submit = SubmitField("Submit")


class SavingAccountSearchForm(FlaskForm):
    id = StringField("Account ID", validators=[])
    clients = SelectMultipleField("Client Name", validators=[])
    branch_name = SelectField('Branch Name')
    employee_id = SelectField('Employee')
    submit = SubmitField("Search")

    def __init__(self, *args, **kwargs):
        super(SavingAccountSearchForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [('', '')]
        self.branch_name.choices.extend([(branch.name, branch.name)
                             for branch in Branch.query.all()])
        self.clients.choices = [(client.id, client.name + ', ' + client.id)
                             for client in Client.query.all()]
        self.employee_id.choices = [('', '')]
        self.employee_id.choices.extend([(employee.id, employee.name + ', ' + employee.id)
                             for employee in Employee.query.all()])


class SavingAccountEditForm(FlaskForm):
    id = StringField("Account ID", validators=[InputRequired()])
    branch_name = SelectField('Branch Name', validators=[InputRequired()])
    employee_id = SelectField('Employee Name', validators=[InputRequired()])
    balance = FloatField("Balance", validators=[InputRequired(), NumberRange(min=0., message="Balance must be greater than 0")])
    interest_rate = StringField("Interest Rate", validators=[InputRequired()])
    currency_type = StringField("Currency Type", validators=[InputRequired()])
    clients = SelectMultipleField("Client Name", validators=[InputRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(SavingAccountEditForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [(branch.name, branch.name)
                             for branch in Branch.query.all()]
        self.clients.choices = [(client.id, client.name + ', ' + client.id)
                             for client in Client.query.all()]
        self.employee_id.choices = [(employee.id, employee.name + ', ' + employee.id)
                             for employee in Employee.query.all()]


class CheckAccountSearchForm(FlaskForm):
    id = StringField("Account ID", validators=[])
    clients = SelectMultipleField("Client Name", validators=[])
    branch_name = SelectField('Branch Name')
    employee_id = SelectField('Employee')
    submit = SubmitField("Search")

    def __init__(self, *args, **kwargs):
        super(CheckAccountSearchForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [('', '')]
        self.branch_name.choices.extend([(branch.name, branch.name)
                             for branch in Branch.query.all()])
        self.clients.choices = [(client.id, client.name + ', ' + client.id)
                             for client in Client.query.all()]
        self.employee_id.choices = [('', '')]
        self.employee_id.choices.extend([(employee.id, employee.name + ', ' + employee.id)
                             for employee in Employee.query.all()])

class CheckAccountEditForm(FlaskForm):
    id = StringField("Account ID", validators=[InputRequired()])
    branch_name = SelectField('Branch Name', validators=[InputRequired()])
    employee_id = SelectField('Employee', validators=[InputRequired()])
    balance = FloatField("balance", validators=[InputRequired(), NumberRange(min=0., message="Balance mush be greater than 0")])
    over_draft = FloatField("overdraft", validators=[InputRequired(), NumberRange(min=0., message="Overdraft mush be greater than 0")])
    clients = SelectMultipleField("Client", validators=[InputRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(CheckAccountEditForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [(branch.name, branch.name)
                             for branch in Branch.query.all()]
        self.clients.choices = [(client.id, client.name + ', ' + client.id)
                             for client in Client.query.all()]
        self.employee_id.choices = [(employee.id, employee.name + ', ' + employee.id)
                             for employee in Employee.query.all()]


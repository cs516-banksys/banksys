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

### Chengyu Wu
class ClientSearchForm(FlaskForm):
    id = StringField("SSN", validators=[
        Optional(),
        Regexp(r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$', 0,
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
        Regexp(r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$', 0,
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
    branch_name = SelectField('Brach Name')
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
    balance = FloatField("Balance", validators=[InputRequired(), NumberRange(min=0., message="Balance must greater than 0")])
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

class EmployeeSearchForm(FlaskForm):
    id = StringField("SSN", validators=[
        Optional(),
        Regexp(r'^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$', 0,
            "Invalid SSN")
    ])
    name = StringField("Name")
    branch_name = SelectField('Branch')
    phone = StringField("Phone number")
    address = StringField("Address")
    submit = SubmitField("Search")
    
    def __init__(self, *args, **kwargs):
        super(EmployeeSearchForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [('', '')]
        self.branch_name.choices.extend([(branch.name, branch.name)
                             for branch in Branch.query.all()])

class EmployeeEditForm(FlaskForm):
    id = StringField("SSN", validators=[
        InputRequired(),
        Regexp(r'^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$', 0,
            "Invalid SSN")
    ])
    name = StringField("Name", validators=[InputRequired()])
    branch_name = SelectField('Branch')
    phone = StringField("Phone number")
    address = StringField("Address")
    enroll_date = DateField("Date of employment", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [(branch.name, branch.name)
                             for branch in Branch.query.all()]
class LoanEditForm(FlaskForm):
    id = StringField("Loan ID", validators=[InputRequired()])
    branch_name = SelectField('Issuing Branch', validators=[InputRequired()])
    employee_id = SelectField('Contacting employee', validators=[InputRequired()])
    amount = FloatField("Amount", validators=[InputRequired(), NumberRange(min=0., message="Amount of a loan must be greater than 0")])
    clients = SelectMultipleField("Loanee", validators=[InputRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(LoanEditForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [(branch.name, branch.name)
                             for branch in Branch.query.all()]
        self.clients.choices = [(client.id, client.name + ', ' + client.id)
                             for client in Client.query.all()]
        self.employee_id.choices = [(employee.id, employee.name + ', ' + employee.id)
                             for employee in Employee.query.all()]


class LoanSearchForm(FlaskForm):
    id = StringField("Loan ID", validators=[])
    clients = SelectMultipleField("Loanee", validators=[])
    branch_name = SelectField('Issuing branch')
    employee_id = SelectField('Contacting employee')
    submit = SubmitField("Search")

    def __init__(self, *args, **kwargs):
        super(LoanSearchForm, self).__init__(*args, **kwargs)
        self.branch_name.choices = [('', '')]
        self.branch_name.choices.extend([(branch.name, branch.name)
                             for branch in Branch.query.all()])
        self.clients.choices = [(client.id, client.name + ', ' + client.id)
                             for client in Client.query.all()]
        self.employee_id.choices = [('', '')]
        self.employee_id.choices.extend([(employee.id, employee.name + ', ' + employee.id)
                             for employee in Employee.query.all()])


class LoanLogEditForm(FlaskForm):
    id = StringField("Loan offer ID", validators=[InputRequired()])
    loan_id = SelectField('Loan ID', validators=[InputRequired()])
    amount = FloatField("Amount", validators=[InputRequired(), NumberRange(min=0., message="Amount of an offer must be greater than 0")])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(LoanLogEditForm, self).__init__(*args, **kwargs)
        self.loan_id.choices = [(loan.id, loan.id)
                             for loan in Loan.query.all()]

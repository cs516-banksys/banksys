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
    amount = FloatField("Amount", validators=[InputRequired(), NumberRange(min=0., message="贷款金额必须大于0")])
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
    amount = FloatField("Amount", validators=[InputRequired(), NumberRange(min=0., message="发放金额必须大于0")])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(LoanLogEditForm, self).__init__(*args, **kwargs)
        self.loan_id.choices = [(loan.id, loan.id)
                             for loan in Loan.query.all()]

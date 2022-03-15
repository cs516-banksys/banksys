from datetime import date
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class HasLoan(db.Model):
    __tablename__ = 'hasloans'
    client_id = db.Column(db.String(20), db.ForeignKey(
        'clients.id'), primary_key=True)
    loan_id = db.Column(db.String(20), db.ForeignKey(
        'loans.id'), primary_key=True)

class ClientSaving(db.Model):
    __tablename__ = 'clientsavings'
    client_id = db.Column(db.String(20), db.ForeignKey(
        'clients.id'), primary_key=True)
    saving_id = db.Column(db.String(20), db.ForeignKey(
        'savings.id'), primary_key=True)


class ClientCheck(db.Model):
    __tablename__ = 'clientchecks'
    client_id = db.Column(db.String(20), db.ForeignKey(
        'clients.id'), primary_key=True)
    check_id = db.Column(db.String(20), db.ForeignKey(
        'checks.id'), primary_key=True)


class Branch(db.Model):
    __tablename__ = 'branches'
    name = db.Column(db.String(100), primary_key=True)
    city = db.Column(db.String(20))
    asset = db.Column(db.Integer)

    employees = db.relationship('Employee', backref='branch', lazy='dynamic')
    loans = db.relationship('Loan', backref='branch', lazy='dynamic')
    saving_accounts = db.relationship(
        'SavingAccount', backref='branch', lazy='dynamic')
    check_accounts = db.relationship(
        'CheckAccount', backref='branch', lazy='dynamic')

class BranchRecords(db.Model):
    __tablename__ = 'branchrecords'
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey('branches.name'))
    OpType = db.Column(db.String(4))
    OpTime = db.Column(db.DateTime, default=datetime.utcnow)
    OpMoney = db.Column(db.Float)


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(256))
    email = db.Column(db.String(30), default='')
    contact_name = db.Column(db.String(20))
    contact_phone = db.Column(db.String(15), default='')
    contact_email = db.Column(db.String(30), default='')
    contact_relation = db.Column(
        db.String(40), default='Prefer not to disclose')

    loans = db.relationship(
        'HasLoan',
        foreign_keys=[HasLoan.client_id],
        backref=db.backref('client', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    saving_accounts = db.relationship(
        'ClientSaving',
        foreign_keys=[ClientSaving.client_id],
        backref=db.backref('client', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    check_accounts = db.relationship(
        'ClientCheck',
        foreign_keys=[ClientCheck.client_id],
        backref=db.backref('client', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.String(20), primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey('branches.name'))
    name = db.Column(db.String(20))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(256))
    enroll_date = db.Column(db.Date, default=date.today())

    saving_accounts_managed = db.relationship(
        'SavingAccount', backref='employee', lazy='dynamic')
    check_accounts_managed = db.relationship(
        'CheckAccount', backref='employee', lazy='dynamic')
    loans_managed = db.relationship('Loan', backref='employee', lazy='dynamic')


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.String(20), primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey('branches.name'))
    employee_id = db.Column(db.String(20), db.ForeignKey('employees.id'))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='Not started to issue')

    clients = db.relationship(
        'HasLoan',
        foreign_keys=[HasLoan.loan_id],
        backref=db.backref('loan', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    loan_logs = db.relationship('LoanLog', backref='loan', lazy='dynamic')


class LoanLog(db.Model):
    __tablename__ = "loanlogs"
    id = db.Column(db.String(30), primary_key=True)
    loan_id = db.Column(db.String(20), db.ForeignKey('loans.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)


class SavingAccount(db.Model):
    __tablename__ = 'savings'
    id = db.Column(db.String(20), primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey('branches.name'))
    employee_id = db.Column(db.String(20), db.ForeignKey('employees.id'))
    balance = db.Column(db.Float)
    open_date = db.Column(db.DateTime, default=datetime.utcnow)
    interest_rate = db.Column(db.String(10))
    currency_type = db.Column(db.String(5))
    last_access_date = db.Column(db.DateTime, default=datetime.utcnow)

    clients = db.relationship(
        'ClientSaving',
        foreign_keys=[ClientSaving.saving_id],
        backref=db.backref('saving_account', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @staticmethod
    def on_changed_balance(target, value, oldvalue, initiator):
        target.last_access_date = datetime.utcnow()

db.event.listen(SavingAccount.balance, 'set', SavingAccount.on_changed_balance)


class SavingConstraint(db.Model):
    __tablename__ = 'savingconstraints'
    client_id = db.Column(db.String(20), db.ForeignKey(
        'clients.id'), primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey(
        'branches.name'), primary_key=True)
    saving_id = db.Column(db.String(20), db.ForeignKey(
        'savings.id'), primary_key=True)

    __table_args__ = (
        db.UniqueConstraint('client_id', 'branch_name', name='con1'),
    )


class CheckAccount(db.Model):
    __tablename__ = 'checks'
    id = db.Column(db.String(20), primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey('branches.name'))
    employee_id = db.Column(db.String(20), db.ForeignKey('employees.id'))
    balance = db.Column(db.Float)
    open_date = db.Column(db.DateTime, default=datetime.utcnow)
    over_draft = db.Column(db.Float)
    last_access_date = db.Column(db.DateTime, default=datetime.utcnow)

    clients = db.relationship(
        'ClientCheck',
        foreign_keys=[ClientCheck.check_id],
        backref=db.backref('check_account', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @staticmethod
    def on_changed_balance(target, value, oldvalue, initiator):
        target.last_access_date = datetime.utcnow()

db.event.listen(CheckAccount.balance, 'set', CheckAccount.on_changed_balance)

class CheckConstraint(db.Model):
    __tablename__ = 'checkconstraint'
    client_id = db.Column(db.String(20), db.ForeignKey(
        'clients.id'), primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey(
        'branches.name'), primary_key=True)
    check_id = db.Column(db.String(20), db.ForeignKey(
        'savings.id'), primary_key=True)

    __table_args__ = (
        db.UniqueConstraint('client_id', 'branch_name', name='con1'),
    )


class SystemUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return SystemUser.query.get(user_id)

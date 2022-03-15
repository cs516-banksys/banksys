from flask import render_template, redirect, url_for, make_response, request, current_app, flash
from .forms import BranchSearchForm, BranchEditForm, EmployeeEditForm, EmployeeSearchForm, ClientEditForm, ClientSearchForm, SavingAccountEditForm, SavingAccountSearchForm, LoanEditForm, LoanSearchForm, LoanLogEditForm
from . import main
from .. import db
from ..models import Branch, Employee, Client, SavingAccount, ClientSaving, SavingConstraint,  ClientCheck,  HasLoan, Loan, LoanLog, BranchRecords
from datetime import date
from flask_login import login_required
from sqlalchemy import extract
import datetime

@main.route('/')
def index():
    return render_template('index.html')



### Chengyu Wu
@main.route('/client', methods=['GET', 'POST'])
@login_required
def client():
    form = ClientSearchForm()
    if form.validate_on_submit():
        resp = make_response(redirect(url_for('.client')))
        resp.set_cookie('search_client_id', form.id.data, max_age=10*60)
        resp.set_cookie('search_client_name', form.name.data, max_age=10*60)
        resp.set_cookie('search_client_phone', form.phone.data, max_age=10*60)
        resp.set_cookie('search_client_address',
                        form.address.data, max_age=10*60)
        resp.set_cookie('search_client_contact_name',
                        form.contact_name.data, max_age=10*60)
        return resp

    query = Client.query

    search_client_id = request.cookies.get('search_client_id', '')
    search_client_name = request.cookies.get('search_client_name', '')
    search_client_phone = request.cookies.get('search_client_phone', '')
    search_client_address = request.cookies.get('search_client_address', '')
    search_client_contact_name = request.cookies.get(
        'search_client_contact_name', '')

    if search_client_id != '':
        query = query.filter_by(id=search_client_id)
        form.id.data = search_client_id
    if search_client_name != '':
        query = query.filter(Client.name.like('%' + search_client_name + '%'))
        form.name.data = search_client_name
    if search_client_phone != '':
        query = query.filter_by(phone=search_client_phone)
        form.phone.data = search_client_phone
    if search_client_address != '':
        query = query.filter(Client.address.like(
            '%' + search_client_address + '%'))
        form.address.data = search_client_address
    if search_client_contact_name != '':
        query = query.filter(Client.contact_name.like(
            '%' + search_client_contact_name + '%'))
        form.contact_name.data = search_client_contact_name

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    clients = pagination.items

    return render_template('client.html', form=form, clients=clients, pagination=pagination)


@main.route('/client_edit/<string:client_id>', methods=['GET', 'POST'])
@login_required
def client_edit(client_id):
    form = ClientEditForm()
    if form.validate_on_submit():
        if client_id == 'create':
            if Client.query.filter_by(id=form.id.data).first():
                flash('SSN already exist!')
                return render_template('client_edit.html', form=form)
            client = Client(
                id=form.id.data,
                name=form.name.data,
                phone=form.phone.data,
                address=form.address.data,
                contact_name=form.contact_name.data,
            )
            if form.contact_phone.data != '':
                client.contact_phone = form.contact_phone.data
            if form.contact_email.data != '':
                client.contact_email = form.contact_email.data
            if form.contact_relation.data != '':
                client.contact_relation = form.contact_relation.data
            db.session.add(client)
            db.session.commit()
            flash('Successfully add client')
            return redirect(url_for('.client_edit', client_id=client.id))
        else:
            client = Client.query.filter_by(id=client_id).first_or_404()
            if client.id != form.id.data:
                if Client.query.filter_by(id=form.id.data).first():
                    flash("SSN already exist!")
                    return render_template('client_edit.html', form=form)
            client.id = form.id.data
            client.name = form.name.data
            client.phone = form.phone.data
            client.address = form.address.data
            client.contact_name = form.contact_name.data
            if form.contact_phone.data != '':
                client.contact_phone = form.contact_phone.data
            if form.contact_email.data != '':
                client.contact_email = form.contact_email.data
            if form.contact_relation.data != '':
                client.contact_relation = form.contact_relation.data
            db.session.add(client)
            db.session.commit()
            flash('Successfully Update Client')
            return redirect(url_for('.client_edit', client_id=client.id))

    if client_id != 'create':
        client = Client.query.filter_by(id=client_id).first_or_404()
        form.id.data = client.id
        form.name.data = client.name
        form.phone.data = client.phone
        form.address.data = client.address
        form.contact_name.data = client.contact_name
        form.contact_phone.data = client.contact_phone
        form.contact_email.data = client.contact_email
        form.contact_relation = client.contact_relation

    return render_template('client_edit.html', form=form)


@main.route('/client_all')
@login_required
def client_show_all():
    resp = make_response(redirect(url_for('.client')))
    resp.set_cookie('search_client_id', '', max_age=10*60)
    resp.set_cookie('search_client_name', '', max_age=10*60)
    resp.set_cookie('search_client_phone', '', max_age=10*60)
    resp.set_cookie('search_client_address', '', max_age=10*60)
    resp.set_cookie('search_client_contact_name', '', max_age=10*60)
    return resp
    return render_template('client_edit.html', form=form)


@main.route('/client_delete/<string:id>')
@login_required
def client_delete(id):
    client = Client.query.filter_by(id=id).first_or_404()
    if client.loans.first():
        flash('Client has loans，cannot delete!')
        return redirect(url_for('.client_show_all'))
    if client.saving_accounts.first():
        flash('Client has saving account，cannot delete!')
        return redirect(url_for('.client_show_all'))
    db.session.delete(client)
    db.session.commit()
    flash('Successfully delete')
    return redirect(url_for('.client_show_all'))


@main.route('/saving_account_edit/<string:account_id>', methods=['GET', 'POST'])
@login_required
def saving_account_edit(account_id):
    form = SavingAccountEditForm()
    if form.validate_on_submit():
        if account_id == 'create':
            if SavingAccount.query.filter_by(id=form.id.data).first():
                flash('Account already exist!')
                return render_template('saving_account_edit.html', form=form)
            saving_account = SavingAccount(
                id=form.id.data,
                branch_name=form.branch_name.data,
                employee_id=form.employee_id.data,
                balance=form.balance.data,
                interest_rate=form.interest_rate.data,
                currency_type=form.currency_type.data
            )
            db.session.add(saving_account)
            for c_id in form.clients.data:
                client = Client.query.filter_by(id=c_id).first_or_404()
                client_saving = ClientSaving(client=client, saving_account=saving_account)
                db.session.add(client_saving)
                if SavingConstraint.query.filter_by(client_id=client.id, branch_name=saving_account.branch_name).first():
                    db.session.rollback()
                    flash('Each client could only have one saving account!')
                    return render_template('saving_account_edit.html', form=form)
                saving_constraint = SavingConstraint(
                    client_id=client.id,
                    branch_name=saving_account.branch_name,
                    saving_id=saving_account.id
                )
                db.session.add(saving_constraint)
            db.session.commit()
            flash('Successfully add saving account!')
            return redirect(url_for('.saving_account_edit', account_id=saving_account.id))
        else:
            saving_account = SavingAccount.query.filter_by(id=account_id).first_or_404()
            if saving_account.id != form.id.data:
                if SavingAccount.query.filter_by(id=form.id.data).first():
                    flash('Account already exist!')
                    return render_template('saving_account_edit.html', form=form)
            orig_account_id = saving_account.id
            saving_account.id = form.id.data
            saving_account.branch_name = form.branch_name.data
            saving_account.employee_id = form.employee_id.data
            saving_account.balance = form.balance.data
            saving_account.interest_rate = form.interest_rate.data
            saving_account.currency_type = form.currency_type.data
            db.session.add(saving_account)

            ClientSaving.query.filter_by(saving_id=orig_account_id).delete()
            SavingConstraint.query.filter_by(saving_id=orig_account_id).delete()
            db.session.commit()

            for c_id in form.clients.data:
                client = Client.query.filter_by(id=c_id).first_or_404()
                client_saving = ClientSaving(client=client, saving_account=saving_account)
                db.session.add(client_saving)
                if SavingConstraint.query.filter_by(client_id=client.id, branch_name=saving_account.branch_name).first():
                    db.session.rollback()
                    flash('Each client could only have one saving account!')
                    return render_template('saving_account_edit.html', form=form)
                saving_constraint = SavingConstraint(
                    client_id=client.id,
                    branch_name=saving_account.branch_name,
                    saving_id=saving_account.id
                )
                db.session.add(saving_constraint)

            db.session.commit()
            flash('Successfully update account!')
            return redirect(url_for('.saving_account_edit', account_id=saving_account.id))

    if account_id != 'create':
        saving_account = SavingAccount.query.filter_by(id=account_id).first_or_404()
        clients = [c.client.id for c in saving_account.clients.all()]
        form.id.data = saving_account.id
        form.branch_name.data = saving_account.branch_name
        form.employee_id.data = saving_account.employee_id
        form.balance.data = saving_account.balance
        form.interest_rate.data = saving_account.interest_rate
        form.currency_type.data = saving_account.currency_type
        form.clients.data = clients

    return render_template('saving_account_edit.html', form=form)



@main.route('/saving_account', methods=['GET', 'POST'])
@login_required
def saving_account():
    form = SavingAccountSearchForm()
    if form.validate_on_submit():
        resp = make_response(redirect(url_for('.saving_account')))
        resp.set_cookie('search_sa_id', form.id.data, max_age=10*60)
        resp.set_cookie('search_sa_branch_name', form.branch_name.data, max_age=10*60)
        resp.set_cookie('search_sa_employee_id', form.employee_id.data, max_age=10*60)
        resp.set_cookie('search_sa_clients', ','.join(form.clients.data), max_age=10*60)
        return resp

    query = SavingAccount.query

    search_sa_id = request.cookies.get('search_sa_id', '')
    search_sa_branch_name = request.cookies.get('search_sa_branch_name', '')
    search_sa_employee_id = request.cookies.get('search_sa_employee_id', '')
    search_sa_clients = request.cookies.get('search_sa_clients', '')
    if search_sa_clients != '':
        search_sa_clients = search_sa_clients.split(',')
    else:
        search_sa_clients = []

    if search_sa_id != '':
        query = query.filter_by(id=search_sa_id)
        form.id.data = search_sa_id
    if search_sa_branch_name != '':
        query = query.filter_by(branch_name=search_sa_branch_name)
        form.branch_name.data = search_sa_branch_name
    if search_sa_employee_id != '':
        query = query.filter_by(employee_id=search_sa_employee_id)
        form.employee_id.data = search_sa_employee_id
    if search_sa_clients != []:
        for c_id in search_sa_clients:
            query = query.filter(SavingAccount.clients.any(client_id=c_id))
        form.clients.data = search_sa_clients

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    saving_accounts = pagination.items

    return render_template('saving_account.html', form=form, saving_accounts=saving_accounts, pagination=pagination)


@main.route('/saving_account_all')
@login_required
def saving_account_show_all():
    resp = make_response(redirect(url_for('.saving_account')))
    resp.set_cookie('search_sa_id', '', max_age=10*60)
    resp.set_cookie('search_sa_branch_name', '', max_age=10*60)
    resp.set_cookie('search_sa_employee_id', '', max_age=10*60)
    resp.set_cookie('search_sa_clients', '', max_age=10*60)
    return resp


@main.route('/saving_account_delete/<string:account_id>')
@login_required
def saving_account_delete(account_id):
    saving_account = SavingAccount.query.filter_by(id=account_id).first_or_404()
    ClientSaving.query.filter_by(saving_id=saving_account.id).delete()
    SavingConstraint.query.filter_by(saving_id=saving_account.id).delete()
    db.session.delete(saving_account)
    db.session.commit()
    flash('Successfully delete!')
    return redirect(url_for('.saving_account_show_all'))





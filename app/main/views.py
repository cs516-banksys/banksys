from flask import render_template, redirect, url_for, make_response, request, current_app, flash
from .forms import BranchSearchForm, BranchEditForm, EmployeeSearchForm, EmployeeEditForm, LoanSearchForm
from . import main
from .. import db
from ..models import Branch, Employee, Loan
from flask_login import login_required

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/branch', methods=['GET', 'POST'])
@login_required
def branch():
    form = BranchSearchForm()
    if form.validate_on_submit():
        resp = make_response(redirect(url_for('.branch')))
        resp.set_cookie('search_branch_name', form.name.data, max_age=10*60)
        resp.set_cookie('search_branch_city', form.city.data, max_age=10*60)
        return resp
    query = Branch.query
    search_branch_name = request.cookies.get('search_branch_name', '')
    search_branch_city = request.cookies.get('search_branch_city', '')
    if search_branch_name != '':
        query = query.filter(Branch.name.like('%' + search_branch_name + '%'))
        form.name.data = search_branch_name
    if search_branch_city != '':
        query = query.filter(Branch.city.like('%' + search_branch_city + '%'))
        form.city.data = search_branch_city

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    branches = pagination.items

    return render_template('branch.html', form=form, branches=branches, pagination=pagination)


@main.route('/branch_all')
@login_required
def branch_show_all():
    resp = make_response(redirect(url_for('.branch')))
    resp.set_cookie('search_branch_name', '', max_age=10*60)
    resp.set_cookie('search_branch_city', '', max_age=10*60)
    return resp


@main.route('/branch_edit/<string:branch_name>', methods=['GET', 'POST'])
@login_required
def branch_edit(branch_name):
    form = BranchEditForm()
    if form.validate_on_submit():
        if branch_name == 'create':
            if Branch.query.filter_by(name=form.name.data).first():
                flash('This branch name already exists.')
                return render_template('branch_edit.html', form=form)
            branch = Branch(
                name=form.name.data,
                city=form.city.data,
                asset=form.asset.data
            )
            db.session.add(branch)
            db.session.commit()
            flash('New branch name is added sucessfully.')
            return redirect(url_for('.branch_edit', branch_name=branch.name))
        else:
            branch = Branch.query.filter_by(name=branch_name).first_or_404()
            if branch.name != form.name.data:
                if Branch.query.filter_by(name=form.name.data).first():
                    flash("This branch name already exists.")
                    return render_template('branch_edit.html', form=form)
            branch.name = form.name.data
            branch.city = form.city.data
            branch.asset = form.asset.data
            db.session.add(branch)
            db.session.commit()
            flash('This branch information is updated sucessfully.')
            return redirect(url_for('.branch_edit', branch_name=branch.name))

    if branch_name != 'create':
        branch = Branch.query.filter_by(name=branch_name).first_or_404()
        form.name.data = branch.name
        form.city.data = branch.city
        form.asset.data = branch.asset

    return render_template('branch_edit.html', form=form)


@main.route('/branch_delete/<string:id>')
@login_required
def branch_delete(id):
    branch = Branch.query.filter_by(name=id).first_or_404()
    if branch.loans.first():
        flash('The branch still has loans that can not be deleted.')
        return redirect(url_for('.branch_show_all'))
    if branch.saving_accounts.first():
        flash('The branch still has saving accounts that can not be deleted.')
        return redirect(url_for('.branch_show_all'))
    if branch.check_accounts.first():
        flash('The branch still has checking accounts and can not be deleted.')
        return redirect(url_for('.branch_show_all'))
    if branch.employees.first():
        flash('The branch still has emplyees that can not be deleted.')
        return redirect(url_for('.branch_show_all'))
    db.session.delete(branch)
    db.session.commit()
    flash('Delete sucessfully')
    return redirect(url_for('.branch_show_all'))

@main.route('/employee', methods=['GET', 'POST'])
@login_required
def employee():
    form = EmployeeSearchForm()
    if form.validate_on_submit():
        resp = make_response(redirect(url_for('.employee')))
        resp.set_cookie('search_employee_id', form.id.data, max_age=10*60)
        resp.set_cookie('search_employee_name', form.name.data, max_age=10*60)
        resp.set_cookie('search_employee_branch_name',
                        form.branch_name.data, max_age=10*60)
        resp.set_cookie('search_employee_phone',
                        form.phone.data, max_age=10*60)
        resp.set_cookie('search_employee_address',
                        form.address.data, max_age=10*60)
        return resp

    query = Employee.query

    search_employee_id = request.cookies.get('search_employee_id', '')
    search_employee_name = request.cookies.get('search_employee_name', '')
    search_employee_branch_name = request.cookies.get(
        'search_employee_branch_name', '')
    search_employee_phone = request.cookies.get('search_employee_phone', '')
    search_employee_address = request.cookies.get(
        'search_employee_address', '')

    if search_employee_id != '':
        query = query.filter_by(id=search_employee_id)
        form.id.data = search_employee_id
    if search_employee_name != '':
        query = query.filter(Employee.name.like(
            '%' + search_employee_name + '%'))
        form.name.data = search_employee_name
    if search_employee_branch_name != '':
        query = query.filter_by(branch_name=search_employee_branch_name)
        form.branch_name.data = search_employee_branch_name
    if search_employee_phone != '':
        query = query.filter_by(phone=search_employee_phone)
        form.phone.data = search_employee_phone
    if search_employee_address != '':
        query = query.filter(Employee.address.like(
            '%' + search_employee_address + '%'))
        form.address.data = search_employee_address

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    employees = pagination.items

    return render_template('employee.html', form=form, employees=employees, pagination=pagination)

@main.route('/employee_edit/<string:employee_id>', methods=['GET', 'POST'])
@login_required
def employee_edit(employee_id):
    form = EmployeeEditForm()
    if form.validate_on_submit():
        if employee_id == 'create':
            if Employee.query.filter_by(id=form.id.data).first():
                flash('This SSN is already registered')
                return render_template('employee_edit.html', form=form)
            employee = Employee(
                id=form.id.data,
                name=form.name.data,
                branch_name=form.branch_name.data,
                phone=form.phone.data,
                address=form.address.data,
                enroll_date=form.enroll_date.data
            )
            db.session.add(employee)
            db.session.commit()
            flash('Staff added')
            return redirect(url_for('.employee_edit', employee_id=employee.id))
        else:
            employee = Employee.query.filter_by(id=employee_id).first_or_404()
            if employee.id != form.id.data:
                if Employee.query.filter_by(id=form.id.data).first():
                    flash("This SSN is already registered")
                    return render_template('employee_edit.html', form=form)
            employee.id = form.id.data
            employee.name = form.name.data
            employee.branch_name = form.branch_name.data
            employee.phone = form.phone.data
            employee.address = form.address.data
            employee.enroll_date = form.enroll_date.data
            db.session.add(employee)
            db.session.commit()
            flash('Staff information updated')
            return redirect(url_for('.employee_edit', employee_id=employee.id))

    if employee_id != 'create':
        employee = Employee.query.filter_by(id=employee_id).first_or_404()
        form.id.data = employee.id
        form.name.data = employee.name
        form.branch_name.data = employee.branch_name
        form.phone.data = employee.phone
        form.address.data = employee.address
        form.enroll_date.data = employee.enroll_date

    return render_template('employee_edit.html', form=form)

@main.route('/employee_all')
@login_required
def employee_show_all():
    resp = make_response(redirect(url_for('.employee')))
    resp.set_cookie('search_employee_id', '', max_age=10*60)
    resp.set_cookie('search_employee_name', '', max_age=10*60)
    resp.set_cookie('search_employee_branch_name', '', max_age=10*60)
    resp.set_cookie('search_employee_phone', '', max_age=10*60)
    resp.set_cookie('search_employee_address', '', max_age=10*60)
    return resp


@main.route('/employee_delete/<string:id>')
@login_required
def employee_delete(id):
    employee = Employee.query.filter_by(id=id).first_or_404()
    if employee.loans_managed.first():
        flash('Unable to delete: The staff is a manager of a loan')
        return redirect(url_for('.employee_show_all'))
    if employee.saving_accounts_managed.first():
        flash('Unable to delete: The staff is a manager of a checking account')
        return redirect(url_for('.employee_show_all'))
    if employee.check_account_managed.first():
        flash('Unable to delete: The staff is a manager of a saving account')
        return redirect(url_for('.employee_show_all'))
    db.session.delete(employee)
    db.session.commit()
    flash('Staff deleted')
    return redirect(url_for('.employee_show_all'))

@main.route('/loan', methods=['GET', 'POST'])
@login_required
def loan():
    form = LoanSearchForm()
    if form.validate_on_submit():
        resp = make_response(redirect(url_for('.loan')))
        resp.set_cookie('search_loan_id', form.id.data, max_age=10*60)
        resp.set_cookie('search_loan_branch_name', form.branch_name.data, max_age=10*60)
        resp.set_cookie('search_loan_employee_id', form.employee_id.data, max_age=10*60)
        resp.set_cookie('search_loan_clients', ','.join(form.clients.data), max_age=10*60)
        return resp

    query = Loan.query

    search_loan_id = request.cookies.get('search_loan_id', '')
    search_loan_branch_name = request.cookies.get('search_loan_branch_name', '')
    search_loan_employee_id = request.cookies.get('search_loan_employee_id', '')
    search_loan_clients = request.cookies.get('search_loan_clients', '')
    if search_loan_clients != '':
        search_loan_clients = search_loan_clients.split(',')
    else:
        search_loan_clients = []

    if search_loan_id != '':
        query = query.filter_by(id=search_loan_id)
        form.id.data = search_loan_id
    if search_loan_branch_name != '':
        query = query.filter_by(branch_name=search_loan_branch_name)
        form.branch_name.data = search_loan_branch_name
    if search_loan_employee_id != '':
        query = query.filter_by(employee_id=search_loan_employee_id)
        form.employee_id.data = search_loan_employee_id
    if search_loan_clients != []:
        for c_id in search_loan_clients:
            query = query.filter(Loan.clients.any(client_id=c_id))
        form.clients.data = search_loan_clients

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    loans = pagination.items

    return render_template('loan.html', form=form, loans=loans, pagination=pagination)

@main.route('/loan_all')
@login_required
def loan_show_all():
    resp = make_response(redirect(url_for('.loan')))
    resp.set_cookie('search_loan_id', '', max_age=10*60)
    resp.set_cookie('search_loan_branch_name', '', max_age=10*60)
    resp.set_cookie('search_loan_employee_id', '', max_age=10*60)
    resp.set_cookie('search_loan_clients', '', max_age=10*60)
    return resp


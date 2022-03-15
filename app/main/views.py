from flask import render_template, redirect, url_for, make_response, request, current_app, flash
from .forms import BranchSearchForm, BranchEditForm
from . import main
from .. import db
from ..models import Branch
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


#!/usr/bin/env bash

## database create and migration
flask db init
flask db migrate
flask db upgrade

## initial records to database   # username for log in is admin; password is 1234567
sqlite3 data-dev.sqlite -cmd ".mode csv" \
"delete from clients" \
".import db/Users.csv clients" \
"delete from branches" \
".import db/Branch.csv branches" \
"delete from employees" \
".import db/Employee.csv employees" \
"delete from checks" \
".import db/Checking.csv checks" \
"delete from savings" \
".import db/Saving.csv savings" \
"delete from loans" \
".import db/Loan.csv loans" \
"delete from system_user" \
"insert into system_user values(1,'admin','pbkdf2:sha256:260000\$cWVvrPVgMXzn8I6E\$9cf23719edcb252f928ef52fe95fd6ca94beb5c50580e088e789cb01c1204d0b')" \
"delete from hasloans" \
"insert into hasloans select a.id, b.id from (select row_number() over(order by id) as rm, id from clients) a join (select row_number() over(order by id) as rm, id from loans) b on a.rm=b.rm " \
"delete from clientsavings" \
"insert into clientsavings select a.id, b.id from (select row_number() over(order by id) as rm, id from clients) a join (select row_number() over(order by id) as rm, id from savings) b on a.rm=b.rm " \
"delete from clientchecks" \
"insert into clientchecks select a.id, b.id from (select row_number() over(order by id) as rm, id from clients) a join (select row_number() over(order by id) as rm, id from checks) b on a.rm=b.rm " \
"delete from savingconstraints" \
"insert into savingconstraints select a.id, b.branch_name, b.id from (select row_number() over(order by id) as rm, id from clients) a join (select row_number() over(order by id) as rm, id,branch_name from savings) b on a.rm=b.rm " \
"delete from checkconstraint" \
"insert into checkconstraint select a.id, b.branch_name, b.id from (select row_number() over(order by id) as rm, id from clients) a join (select row_number() over(order by id) as rm, id,branch_name from checks) b on a.rm=b.rm " \
"delete from branchrecords" \
".import db/Branch_records.csv branchrecords" \
"delete from loanlogs" \
".import db/Loan_log.csv loanlogs" \

from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_branch = 20
num_users = 100
num_employee= 100
num_saving=100
num_checking=100
num_loan=10
num_branch_records=100

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_branch(num_branch):
    branch = []
    with open('Branch.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Branches...', end=' ', flush=True)
        for uid in range(num_branch):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            name= fake.street_name()
            branch.append(name)
            city= fake.city()
            asset=f'{str(fake.random_int(min=500,max=100000000000))}.{fake.random_int(max=99):02}'
            writer.writerow([name,city,asset])
        print(f'{num_branch} generated')
    return branch

def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            contact_profile= fake.simple_profile()
            id=profile['ssn']
            name = profile['name']
            phone= fake.random_int(min=1000000000,max=9999999999)
            address=profile['address']
            email = profile['mail']
            contact_name= contact_profile['name']
            contact_phone=fake.random_int(min=1000000000,max=9999999999)
            contact_email=  contact_profile['mail']
            contact_relation=fake.random_element(elements=('parent', 'friend','brother','sister','uncle'))
            writer.writerow([id, name, phone, address, email,contact_name,contact_phone,contact_email,contact_relation])
        print(f'{num_users} generated')
    return

def gen_employee(num_employee,branch):
    employee=[]
    with open('Employee.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_employee):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            id= fake.ssn()
            employee.append(id)
            branch_name=fake.random_element(elements=branch)
            name = fake.name()
            phone= fake.random_int(min=1000000000,max=9999999999)
            address= fake.address()
            enroll_date= fake.date_between()
            writer.writerow([id,branch_name,name,phone,address,enroll_date])
        print(f'{num_employee} generated')
    return employee

def gen_saving(num_saving,branch,employee):
    with open('Saving.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Saving...', end=' ', flush=True)
        for uid in range(num_saving):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            id =  fake.random_int(min=100000,max=999999)
            branch_name = fake.random_element(elements=branch)
            employee_id = fake.random_element(elements=employee)
            balance = f'{str(fake.random_int(min=1,max=9999999999))}.{fake.random_int(max=99):02}'
            open_date =  fake.date_time_between(start_date='-2y',end_date='-1y')
            interest_rate = f'{str(fake.random_int(min=0,max=10))}.{fake.random_int(max=99):02}'
            currency_type = fake.random_element(elements=('USD', 'RMB','EUR'))
            last_access_date = fake.date_time_between(start_date='-1y',end_date='now')
            writer.writerow([id,branch_name,employee_id,balance, open_date,interest_rate,currency_type,last_access_date])
        print(f'{num_saving} generated')
    return

def gen_checking(num_checking,branch,employee):
    with open('Checking.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Checking...', end=' ', flush=True)
        for uid in range(num_checking):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            id =  fake.random_int(min=100000,max=999999)
            branch_name = fake.random_element(elements=branch)
            employee_id = fake.random_element(elements=employee)
            balance = f'{str(fake.random_int(min=10000,max=1000000))}.{fake.random_int(max=99):02}'
            open_date = fake.date_time_between(start_date='-2y',end_date='-1y')
            over_draft = f'{str(fake.random_int(min=0,max=9999))}.{fake.random_int(max=99):02}'
            last_access_date = fake.date_time_between(start_date='-1y',end_date='now')
            writer.writerow([id,branch_name,employee_id,balance, open_date,over_draft,last_access_date])
        print(f'{num_checking} generated')
    return

def gen_loan(num_loan,branch,employee):
    loan=[]
    with open('Loan.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Loan...', end=' ', flush=True)
        for uid in range(num_loan):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            id =   f'{str("LOAN")}{fake.random_int(min=100000,max=999999)}'
            branch_name = fake.random_element(elements=branch)
            employee_id = fake.random_element(elements=employee)
            amount= f'{str(fake.random_int(min=1,max=100000))}.{fake.random_int(max=99):02}'
            status=fake.random_element(elements=('Not started to issue', 'Releasing','All loans are released'))
            if status=='Releasing' or status=='All loans are released':
                loan.append(id)
            writer.writerow([id,branch_name,employee_id,amount,status])
        print(f'{num_loan} generated')
    return loan

def Branch_records(num_branch_records,branch):
    with open('Branch_records.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('branch_records...', end=' ', flush=True)
        for uid in range(num_branch_records):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            id =  fake.random_int(min=100000,max=999999)
            branch_name = fake.random_element(elements=branch)
            OpType = fake.random_element(elements=('Deposit', 'Withdrawl','Loan issuance'))
            OpTime= fake.date_time_between(start_date='-2y',end_date='now')
            OpMoney= f'{str(fake.random_int(min=100,max=100000))}.{fake.random_int(max=99):02}'
            writer.writerow([id,branch_name,OpType,OpTime,OpMoney])
        print(f'{num_branch_records} generated')
    return


gen_users(num_users)
branch=gen_branch(num_branch)
employee=gen_employee(num_employee,branch)
gen_saving(num_saving,branch,employee)
gen_checking(num_checking,branch,employee)
loan=gen_loan(num_loan,branch,employee)
Branch_records(num_branch_records,branch)

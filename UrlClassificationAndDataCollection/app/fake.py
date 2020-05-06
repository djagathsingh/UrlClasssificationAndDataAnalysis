import pymongo
from faker import Faker
import time
import random
from pycountry import countries as ci
import datetime

client = pymongo.MongoClient('localhost', 27017)
db = client.URLdb
userprofile = db.app_userprofileinfo
user = db.auth_user

c = list(ci)
name = []
for i in c:
    name.append(i.name)
country_choice = [x for x in name]

def makefake(fake):
    for x in range(100000):
        fname = fake.first_name()
        lname = fake.last_name()
        uname = fname+lname
        #validate username
        flag = 0
        while flag == 0:
            if user.count_documents({'username':uname}) == 0:
                flag = 1
            else:
                fname = fake.first_name()
                lname = fake.last_name()
                uname = fname+lname
        user_id = x+3
        password = 'argon2$argon2i$v=19$m=512,t=2,p=2$dlg0a2VjZElvNmo3$Tlby8F/J0qra4lQHJv86uQ'
        email = fake.email()
        date = fake.date_of_birth()
        id = x+2
        age = random.randrange(5,110)
        gender = random.choice(['M','F','O'])
        country = random.choice(country_choice)
        occupation = fake.job()
        social = random.randrange(0,10000)
        entertainment = random.randrange(0,10000)
        ecommerce = random.randrange(0,10000)
        education = random.randrange(0,10000)
        transport = random.randrange(0,10000)
        food = random.randrange(0,10000)
        mail = random.randrange(0,10000)
        docuser = {'id':user_id,'password':password,'last_login':None,'is_superuser':False,'username':uname,'first_name':fname,'last_name':lname,'email':email,'is_staff':False,'is_active':True,'date_joined':datetime.datetime(date.year,date.month,date.day,random.randrange(0,24),random.randrange(0,60),random.randrange(0,60),random.randrange(0,1000000))}
        docprofile = {'id':id,'user_id':user_id,'age':age,'gender':gender,'country':country,'occupation':occupation,'social':social,'entertainment':entertainment,'ecommerce':ecommerce,'education':education,'transport':transport,'food':food,'mail':mail}
        user.insert_one(docuser)
        userprofile.insert_one(docprofile)

fake = Faker()
makefake(fake)

from django.shortcuts import render
from app.forms import UserForm
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
import os
from app import test
import pymongo
import validators
from bson import ObjectId
from app.models import feedbackmod as f,whitelist as w,blacklist as b
from app.forms import UserProfileInfoForm,graph as gr
from urllib.parse import urlparse
import tldextract
import pandas as pd
from pycountry import countries as ci

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
app = os.path.abspath(os.path.join(__file__, os.pardir))
PROJ_PATH = os.path.abspath(os.path.join(app, os.pardir))
TEMPLATES_DIR = os.path.join(PROJ_PATH,'templates')
APP_DIR = os.path.join(TEMPLATES_DIR,'app')


def graph(request):
    if request.method == 'POST':
        input = request.POST.get('option')

        c = list(ci)
        name = []
        for i in c:
            name.append(i.name)
        country_choices = [x for x in name]

        gender_choices = ['M','F','O']

        csv = os.path.join(APP_DIR,'job.csv')
        df = pd.read_csv(csv)
        occupation_choices = list(df['jobs'])

        age_choices = ['1','2','3','4','5','6','7','8']

        flag = 0
        if input in country_choices:
            flag = 1
        elif input in gender_choices:
            flag = 2
        elif input in occupation_choices:
            flag = 3
        else:
            flag = 4

        client = pymongo.MongoClient('localhost', 27017)
        db = client.URLdb
        profile = db.app_userprofileinfo

        def returndic(dictn):
            dic = {}
            social = 0
            entertainment = 0
            ecommerce = 0
            education = 0
            transport = 0
            food = 0
            mail = 0
            for x in profile.find(dictn):
                social += x['social']
                entertainment += x['entertainment']
                ecommerce += x['ecommerce']
                education += x['education']
                transport += x['transport']
                food += x['food']
                mail += x['mail']
            dic['social'] = social
            dic['entertainment'] = entertainment
            dic['ecommerce'] = ecommerce
            dic['education'] = education
            dic['transport'] = transport
            dic['food'] = food
            dic['mail'] = mail
            return dic

        dic = {}

        if flag == 1:
            querydic = {'country':input}
            dic = returndic(querydic)

        elif flag == 2:
            querydic = {'gender':input}
            dic = returndic(querydic)
        elif flag == 3:
            querydic = {'occupation':input}
            dic = returndic(querydic)
        else:
            if input == '1':
                querydic = {'age':{'$lt':11,'$gt':4}}
                dic = returndic(querydic)
            elif input == '2':
                querydic = {'age':{'$lt':17,'$gt':10}}
                dic = returndic(querydic)
            elif input == '3':
                querydic = {'age':{'$lt':23,'$gt':16}}
                dic = returndic(querydic)
            elif input == '4':
                querydic = {'age':{'$lt':31,'$gt':22}}
                dic = returndic(querydic)
            elif input == '5':
                querydic = {'age':{'$lt':41,'$gt':30}}
                dic = returndic(querydic)
            elif input == '6':
                querydic = {'age':{'$lt':51,'$gt':39}}
                dic = returndic(querydic)
            elif input == '7':
                querydic = {'age':{'$lt':61,'$gt':49}}
                dic = returndic(querydic)
            else:
                querydic = {'age':{"$gt":60}}
                dic = returndic(querydic)
        graph_form = gr(data = request.POST)
        labels = []
        data = []
        for key in dic:
            labels.append(key)
            data.append(dic[key])
        return render(request,'app/graph.html',{'graph_form':graph_form,'dic':dic,'posted':True,'labels':labels,'data':data})

    else:
        graph_form = gr()
        return render(request,'app/graph.html',{'graph_form':graph_form,'posted':False})





def index(request):
    return render(request,'app/index.html')

def email(request):
    return render(request,'app/email.html')

def social(request):
    return render(request,'app/social.html')

@csrf_exempt
@login_required
def analyze(request):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.URLdb
    info = db.app_userprofileinfo
    username = request.user.username
    userdb = db.auth_user
    for x in userdb.find({'username':username}):
        id = x['id']
    url = request.POST.get('url')
    urlinfo = tldextract.extract(url)
    domain = urlinfo.domain
    ods = os.path.join(APP_DIR,'ins.ods')
    df = pd.read_excel(ods,engine="odf")
    count = 0
    if(domain in list(df['Social Media'])):
        response = 'social'
        for x in info.find({'user_id':id}):
            count = x['social']
        count += 1
        info.update_one({'user_id':id},{ "$set": { "social": count } })
    elif domain in list(df['Entertainment']):
        response = 'entertainment'
        for x in info.find({'user_id':id}):
            count = x['entertainment']
        count += 1
        info.update_one({'user_id':id},{ "$set": { "entertainment": count } })
    elif domain in list(df['Educational']):
        response = 'education'
        for x in info.find({'user_id':id}):
            count = x['education']
        count += 1
        info.update_one({'user_id':id},{ "$set": { "education": count } })
    elif domain in list(df['Transportation']):
        response = 'transportation'
        for x in info.find({'user_id':id}):
            count = x['transport']
        count += 1
        info.update_one({'user_id':id},{ "$set": { "transport": count } })
    elif domain in list(df['Food & Beverages']):
        response = 'food'
        for x in info.find({'user_id':id}):
            count = x['food']
        count += 1
        info.update_one({'user_id':id},{ "$set": { "food": count } })
    elif domain in list(df['Mail Services']):
        response = 'mail'
        for x in info.find({'user_id':id}):
            count = x['mail']
        count += 1
        info.update_one({'user_id':id},{ "$set": { "mail": count } })
    elif domain in list(df['E-commerce']):
        response = 'ecommerce'
        for x in info.find({'user_id':id}):
            count = x['ecommerce']
        count += 1
        info.update_one({'user_id':id},{ "$set": { "ecommerce": count } })
    else:
        response = 'unknown'
    xml = "<root><urlType>%s</urlType></root>" %response
    return HttpResponse(xml)

@csrf_exempt
@login_required
def xml(request):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.URLdb
    whitelist = db.app_whitelist
    blacklist = db.app_blacklist
    url = request.POST.get('url')
    flag = 0
    if whitelist.count_documents({'url':url,'status':'confirmed'}) > 0:
        flag = 1
    elif whitelist.count_documents({'url':url,'status':{'$ne':'confirmed'}}) > 0:
        flag = 2
    if blacklist.count_documents({'url':url,'status':'confirmed'}) > 0:
        flag = -1
    elif blacklist.count_documents({'url':url,'status':{'$ne':'confirmed'}}) > 0:
        flag =-2
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
    #APP_DIR = os.path.join(TEMPLATE_DIR,'app')
    #XML_PATH = os.path.join(APP_DIR,'url.xml')
    #tree = ET.parse(XML_PATH)
    #tree.find('url').text = url
    if flag == 1:
        #tree.find('safe').text = 'yes'
        safe = 'yes'
    elif flag == -1:
        #tree.find('safe').text = 'no'
        safe = 'no'
    elif flag == 2:
        #tree.find('safe').text = 'yescaution'
        safe = 'yescaution'
    elif flag == -2:
        #tree.find('safe').text = 'caution'
        safe = 'caution'
    else:
        pred = test.predictions(url)
        if(pred == 1):
            #tree.find('safe').text = 'yes'
            safe = 'yes'
            #whitelist.insert_one({'_id':ObjectId(),'url':url,'status':'confirmed'})
            insert = w(url = url, status = 'confirmed')
            insert.save()
        else:
            #tree.find('safe').text = 'no'
            safe = 'no'
            #blacklist.insert_one({'_id':ObjectId(),'url':url,'status':'confirmed'})
            insert = b(url = url, status = 'confirmed')
            insert.save()
    #tree.write(XML_PATH)
    #return render(request,'app/url.xml')
    xml = '<root><url>{}</url><safe>{}</safe></root>'.format(url,safe)
    return HttpResponse(xml)

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        # Check to see if form valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            # Registration Successful!
            profile.save()
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                log = True
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                log = False
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            log = False
            return render(request, 'app/login.html', {'log':log})

    else:
        #Nothing has been provided for username or password.
        return render(request, 'app/login.html', {'log':True})

@login_required
def whatTampermonkey(request):
    return render(request,'app/whatTM.html')

@login_required
def missed(request):
    if request.method == 'POST':
        client = pymongo.MongoClient('localhost', 27017)
        db = client.URLdb
        whitelist = db.app_whitelist
        blacklist = db.app_blacklist

        url1 = request.POST.get('MalNotMal')
        url2 = request.POST.get('NotMalMal')

        no1 = 'no'
        no2 = 'no'

        count1 = 0
        count2 = 0

        valid1 = True
        valid2 = True

        mistake1 = False
        mistake2 = False
        print(url1+' ' + url2)

        if url1 != 'no':
            no1 = 'yes'
            valid1=validators.url(url1)
            if valid1:
                if whitelist.count_documents({'url':url1}) > 0:
                    mistake1 = False
                else:
                    mistake1 = True
                if not mistake1:
                    try:
                        for x in whitelist.find({'url':url1}):
                            count1 = x['count']
                    except:
                        count1 = 0
                    count1 += 1
                    whitelist.update_one({'url':url1}, {'url':url1,'count':count1})
                    if count1 > 50:
                        whitelist.update_one({'url':url1}, {'url':url1,'count':count1,'status':'check'})

        if url2 != 'no':
            no2 = 'yes'
            valid2=validators.url(url2)
            if valid2:
                if blacklist.count_documents({'url':url2}) > 0:
                    mistake2 = False
                else:
                    mistake2 = True
                if not mistake2:
                    try:
                        for x in whitelist.find({'url':url2}):
                            count2 = x['count']
                    except:
                        count1 = 0
                    count1 += 1
                    whitelist.update_one({'url':url2}, {'url':url2,'count':count2})
                    if count2 > 50:
                        whitelist.update_one({'url':url2}, {'url':url2,'count':count2,'status':'check'})

        return render(request,'app/missedURL.html',{'valid1':valid1,'valid2':valid2,'mistake1':mistake1,'mistake2':mistake2,'no1':no1,'no2':no2})
    else:
        no1 = 'no'
        no2 = 'no'

        count1 = 0
        count2 = 0

        valid1 = True
        valid2 = True

        mistake1 = False
        mistake2 = False
        return render(request,'app/missedURL.html',{'valid1':valid1,'valid2':valid2})

@login_required
def feedback(request):
    if request.method == 'POST':
        username = request.user.username
        feedback = request.POST.get('feedback')
        client = pymongo.MongoClient('localhost', 27017)
        db = client.URLdb
        feedbackmod = db.app_feedbackmod
        #feedbackmod.insert_one({'_id':ObjectId(),'user_id':id,'feedback':feedback})
        insert = f(username = username, feedback = feedback)
        insert.save()
        return render(request,'app/feedback.html',{'feeded':True})
    else:
        return render(request,'app/feedback.html',{'feeded':False})

@login_required
def safe(request):
    post = False
    safe = True
    caution = False
    if request.method == 'POST':
        url = request.POST.get('url')
        valid=validators.url(url)
        client = pymongo.MongoClient('localhost', 27017)
        db = client.URLdb
        whitelist = db.app_whitelist
        blacklist = db.app_blacklist
        flag = 0
        if whitelist.count_documents({'url':url,'status':'confirmed'}) > 0:
            flag = 1
        elif whitelist.count_documents({'url':url,'status':{'$ne':'confirmed'}}) > 0:
            flag =2
        if blacklist.count_documents({'url':url,'status':'confirmed'}) > 0:
            flag = -1
        elif blacklist.count_documents({'url':url,'status':{'$ne':'confirmed'}}) > 0:
            flag =-2

        caution = False
        if flag == 1:
            safe = True
            caution = False
        elif flag == -1:
            safe = False
            caution = True
        elif flag == 2:
            safe = True
            caution = True
        elif flag == -2:
            safe = False
            caution = False
        else:
            pred = test.predictions(url)
            if(pred == 1):
                safe = True
                caution = False
                #whitelist.insert_one({'_id':ObjectId(),'url':url,'status':'confirmed'})
                insert = w(url = url, status = "confirmed")
                insert.save()
            else:
                safe = False
                caution = True
                #blacklist.insert_one({'_id':ObjectId(),'url':url,'status':'confirmed'})
                insert = b(url = url, status = "confirmed")
                insert.save()
        return render(request,'app/checkSafe.html',{'post':True,'safe':safe, 'caution':caution,'valid':valid})
    else:
        return render(request,'app/checkSafe.html',{'post':False,'safe':True,'caution':caution})

from django import forms
from django.contrib.auth.models import User
from app.models import UserProfileInfo
from pycountry import countries as ci
import pandas as pd
import os

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('age','gender','country','occupation')

class graph(forms.Form):

    c = list(ci)
    name = []
    for i in c:
        name.append(i.name)
    country_choices = [(x,x) for x in name]

    gender_choices = [('M','Male'),('F','Female'),('O','Others')]

    app = os.path.abspath(os.path.join(__file__, os.pardir))
    PROJ_PATH = os.path.abspath(os.path.join(app, os.pardir))
    TEMPLATES_DIR = os.path.join(PROJ_PATH,'templates')
    APP_DIR = os.path.join(TEMPLATES_DIR,'app')
    csv = os.path.join(APP_DIR,'job.csv')
    df = pd.read_csv(csv)
    occupation_choices = [(x,x) for x in list(df['jobs'])]

    age_choices = [('1','5-10'),('2','11-16'),('3','17-22'),('4','23-30'),('5','31-40'),('6','40-50'),('7','50-60'),('8','60+')]

    init_choices = [('Country',country_choices),('Gender',gender_choices),('Occupation',occupation_choices),('Age',age_choices)]

    option = forms.ChoiceField(choices = init_choices)

    class Meta():
        fields = ('option')

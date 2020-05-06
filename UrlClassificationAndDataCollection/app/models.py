#from django.db import models
from djongo import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from pycountry import countries as ci
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    gender_choice = [('M','Male'),('F','Female'),('O','Other')]
    c = list(ci)
    name = []
    for i in c:
        name.append(i.name)
    country_choice = [(x,x) for x in name]
    gender = models.CharField(max_length = 1,choices=gender_choice)
    country = models.CharField(max_length = 100,choices=country_choice)
    occupation = models.CharField(max_length = 100)
    social = models.IntegerField(default = 0)
    entertainment = models.IntegerField(default = 0)
    ecommerce = models.IntegerField(default = 0)
    education = models.IntegerField(default = 0)
    transport = models.IntegerField(default = 0)
    food = models.IntegerField(default = 0)
    mail = models.IntegerField(default = 0)
    def __str__(self):
        return self.user.username


class feedbackmod(models.Model):
    username = models.CharField(max_length=100)
    feedback = models.TextField()
    def __str__(self):
        return self.username+':'+self.feedback

class whitelist(models.Model):
    url = models.CharField(max_length=500)
    status = models.CharField(max_length=15,default = '')
    count = models.IntegerField(default = 0)
    def __str__(self):
        return self.url

class blacklist(models.Model):
    url = models.CharField(max_length=500)
    status = models.CharField(max_length=15,default = '')
    count = models.IntegerField(default = 0)
    def __str__(self):
        return self.url

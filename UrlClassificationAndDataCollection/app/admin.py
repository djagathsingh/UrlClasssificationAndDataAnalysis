from django.contrib import admin
from app.models import feedbackmod,whitelist,blacklist,UserProfileInfo
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfileInfo
# Register your models here.
#eg:admin.site.register(User)

admin.site.register(feedbackmod)
admin.site.register(whitelist)
admin.site.register(blacklist)
admin.site.register(UserProfileInfo)

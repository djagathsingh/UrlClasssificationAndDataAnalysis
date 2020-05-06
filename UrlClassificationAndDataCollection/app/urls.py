from django.conf.urls import url
from app import views

# SET THE NAMESPACE!
app_name = 'app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^whatTampermonkey/$',views.whatTampermonkey,name = 'whatTampermonkey'),
    url(r'^missed/$',views.missed,name='missed'),
    url(r'^feedback/$',views.feedback,name='feedback'),
    url(r'^safe/$',views.safe,name='safe'),
    url(r'^analyze/$',views.analyze,name = 'analyze'),
    url(r'^email/$',views.email,name = 'email'),
    url(r'^social/$',views.social,name = 'social'),
    url(r'^graph/$',views.graph,name = 'graph'),
]

from django.urls import path
from . import views

app_name = 'user'

urlpatterns =[
    path('login',views.Login,name='Login'),
    path('logout',views.Logout,name='Logout'),
    path('signup',views.Signup,name='Signup'),
]
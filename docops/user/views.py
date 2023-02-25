from django.shortcuts import render
 

# Create your views here.

def Signup(request):
    return render(request,'signup.html',{})
def Login(request):
    return render(request,'login.html',{})
def Logout(request):
    return render(request,'Logout.html',{})
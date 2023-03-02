from django.shortcuts import render
from . forms import SignupForm
from . models import User
# Create your views here.

def Signup(request):
    my_form = SignupForm()
    if request.method == "POST":
        my_form = SignupForm(request.POST)
        if my_form.is_valid():
            email = my_form.cleaned_data['email']
            pswd1 = my_form.cleaned_data['password1']
            pswd2 = my_form.cleaned_data['password2']
            if pswd1 == pswd2:
                User.objects.create(email=email,password=pswd1)
                print("sucessfully signed up")
            else :
                print("error in pswd")    
        else:
            print(my_form.errors)
    content ={
        'form':my_form,
    }            
    return render(request,'signup.html',content)

def Login(request):
    return render(request,'login.html',{})
def Logout(request):
    return render(request,'Logout.html',{})
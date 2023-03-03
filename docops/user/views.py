from django.shortcuts import render,redirect,reverse
from . forms import SignupForm,LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

def Signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': True,
            })
    return render(request,'signup.html',{
        'form': form,
        'error': False
    })

def Login(request):
    if request.user.is_authenticated:
        return redirect(reverse('coreapp:home'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect(reverse('coreapp:home'))
        else:
            print("login error")
            form = LoginForm()
            return render(request,'login.html',{'form':form})
     
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

def Logout(request):
    logout(request)
    return redirect(reverse('coreapp:home'))
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html',{})

def doctor(request):
    return render(request,'doctor.html',{})


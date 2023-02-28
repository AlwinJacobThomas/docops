from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html',{})

def file(request):
    if request.method == 'POST':
        print(request.FILE)

def doctor(request):
    return render(request,'doctor.html',{})


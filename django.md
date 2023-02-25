# Django

1. Create a folder
2. Create  Virutal evnvironment
    > python -m venv venv

    > venv/Sources/activate
3. Install Django
    > pip install django
4. Start project
    >django-admin startproject Project

    >cd Project

5. Start App
    >django-admin startapp App

    add appname in *settings.py* in project
6. setup URLs
    
    add this line for linking app url in project *urls.py*
    >path('',include('coreapp.urls')),
7. create a *templates* folder in App
8. create a new view in app folder

    > def home(request):

    >  >return render(request,'home.html',{})
9. create models
10. register models in admin
11. add views 
12. html and statics

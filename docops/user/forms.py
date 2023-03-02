from django import forms
from . models import User


class SignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
                            attrs={
                                "class":"input",
                                "placeholder":"email"
                            })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
                            attrs={
                                "class":"password",
                                "placeholder":"password"
                            })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
                            attrs={
                                "class":"password",
                                "placeholder":"confirm password"
                            })
    )
    
    # class Meta:
    #     model = User
    #     fields = ['email', 'password','re_password']

    
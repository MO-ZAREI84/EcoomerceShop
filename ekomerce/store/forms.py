from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class SignUpform(UserCreationForm):
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)
    email = forms.EmailField(max_length=50,help_text='salam@gmail.com')

    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2','email')
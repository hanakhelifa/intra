from django import forms

class NameForm(forms.Form):
		login = forms.CharField(label='login', max_length=50)
		password = forms.CharField(widget=forms.PasswordInput(),label='password', max_length=50)

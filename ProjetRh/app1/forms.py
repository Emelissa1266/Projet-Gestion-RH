from django import forms

class AuthentificationForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control"}))

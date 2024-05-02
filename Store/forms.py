from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="e-mail", required=True)
    password = forms.CharField(label="Password",required=True, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    name = forms.CharField(label="Name", required=True)
    email = forms.CharField(label="e-Mail",required=True, widget=forms.EmailInput)
    phone = forms.CharField(label="Phone", required=True)
    address = forms.CharField(label="Address", required=True)
    password = forms.CharField(label="Password",required=True, widget=forms.PasswordInput)
    # retype_password = forms.CharField(label="Retype Password",required=True, widget=forms.PasswordInput)


    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("Email already registered!")
        return data

    # def clean_retype_password(self):
    #     return self.cleaned_data["retype_password"]
    def clean_password(self):
        password = self.cleaned_data["password"]
        # retype_password = self.cleaned_data["retype_password"]

        if len(password) < 6:
            raise forms.ValidationError("length of password is less than 6")
        # if password != retype_password:
        #     raise forms.ValidationError("Password and retype password did not matched.")
        else:
            return password
        

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if len(data) != 10 or data.isdigit() != True:
            raise forms.ValidationError("Invalid mobile no.")
        else:
            return data

class UserEditForm(forms.Form):
    full_name = forms.CharField(label="Full Name", required=True)
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'readonly': 'readonly'}))
    phone = forms.CharField(label="Phone no", required=True)
    address = forms.CharField(label="Address", widget=forms.Textarea, required=True)

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if len(data) != 10 or data.isdigit() != True:
            raise forms.ValidationError("Invalid mobile no.")
        else:
            return data
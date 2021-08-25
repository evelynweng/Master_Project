#from .models import Store
from apidatabase.models import Store
from django.forms import ModelForm
from django import forms

class StoreRegistrationForm(ModelForm):
    # confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Store
        fields = ['store_name', 'owner_first_name', 'owner_last_name', 'store_phone',
            'email', 'store_url', 'store_address', 'store_capacity', 'password']
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput()
        } 

"""         def clean(self):
            #cleaned_data = super(UserForm, self).clean()
            cleaned_data = super(StoreRegistrationForm,self).clean()
            password = cleaned_data.get("password")           
            confirm_password = cleaned_data.get("confirm_password")         
            if password != confirm_password:
                raise forms.ValidationError("Passwords mismatch")
                #self.add_error('confirm_password', "Password does not match")
            return cleaned_data  """


class LoginForm(ModelForm):
     class Meta:
         model = Store
         fields = ['email', 'password']
         labels = {
            "Email": "email",
            "P assword": "password"
         }    
         widgets = {
            "email":  forms.TextInput(attrs={'placeholder':'example@gmail.com','autocomplete': 'off'}), 
            "password": forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
         }
         
      

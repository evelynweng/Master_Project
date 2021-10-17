#from .models import Store
from apidatabase.models import Store,Advertisement,PromoCode
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
            'password': forms.PasswordInput(),
            'store_phone':forms.TextInput(attrs={'placeholder':'xxx-xxx-xxxx'})
        } 


class LoginForm(ModelForm):
     class Meta:
         model = Store
         fields = ['email', 'password']
         labels = {
            "Email": "email",
            "Password": "password"
         }    
         widgets = {
            "email":  forms.TextInput(attrs={'placeholder':'example@gmail.com','autocomplete': 'off'}), 
            "password": forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
         }
         
      
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'owner_first_name', 'owner_last_name', 'store_phone',
            'store_address', 'store_capacity','profile_pic']


class GenerateAdCouponForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields =['discount', "ad_code",'ad_image','ad_description','start_date','end_date']
        widgets = {
            #'end_date': forms.SelectDateWidget()
            #'discount':forms.IntegerField(attrs={'placeholder':"Discount in percentage."}),
            #'ad_code':forms.CharField(attrs={'placeholder':"Max 20 characters."}),
            #'ad_description':forms.CharField(attrs={'placeholder':'Max 100 characters.'}),
            'start_date':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            "end_date":forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }

    def clean_dates(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        print("checking")
        if start_date and end_date: 
            if not end_date > start_date:
                print("validating")
                raise forms.ValidationError(
                    "End date should be greater than start date."
                    )    
        return        

class GeneratePromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields =['discount', "promo_code",'promo_description','wait_time','is_active','start_date','end_date']
        widgets = {
            #'end_date': forms.SelectDateWidget()
            'start_date':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            "end_date":forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }
    def clean_dates(self):
        #cleaned_data = super().clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        print("checking")
        if start_date and end_date: 
            if not end_date > start_date:
                print("validating")
                raise forms.ValidationError(
                    "End date should be greater than start date."
                    )    
        return        
 

class ResetPassword_EmailForm(forms.Form):
    email = forms.EmailField(max_length=100) 
    widgets = {
            "email":  forms.TextInput(attrs={'placeholder':'example@gmail.com'})
    }

class ResetPassword_PasswordForm(forms.Form):
    password = forms.CharField(label='Password', max_length=30)  
    confirm_password = forms.CharField(label='Confirm Password', max_length=30) 
    widgets = {
            'password': forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
            'confirm_password': forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
            }

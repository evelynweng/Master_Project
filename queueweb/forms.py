from django import forms
from apidatabase.models import Customer



class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs={'placeholder':'Enter First Name'}))
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs={'placeholder':'Enter Last Name'}))
    phone = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs={'placeholder':'Enter Phone Number'}))
    number_of_people = forms.IntegerField()

    Customerueue_id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    join_time = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    current_waiting_time_individual = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    potential_wait_time = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    real_wait_time = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


    class Meta:
        # provide an association between the ModelForm and a model
        model = Customer
         # some fields we may not want to include them, eg: foreign key
        exclude = ('store','queue',)
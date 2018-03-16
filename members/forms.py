from django import forms

class AddMemberForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    mobile_number = forms.IntegerField()
     = forms.EmailField()

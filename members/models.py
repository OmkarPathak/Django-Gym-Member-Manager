from django.db import models
from django.forms import ModelForm
from django import forms
import datetime

SUBSCRIPTION_TYPE_CHOICES = (
    ('gym', 'Gym'),
    ('cross_fit', 'Cross Fit'),
    ('gym_and_cross_fit', 'Gym + Cross Fit'),
)

SUBSCRIPTION_PERIOD_CHOICES = (
    ('1', '1 Month'),
    ('3', '3 Months'),
    ('6', '6 Months'),
    ('12', '12 Months'),
)

class Member(models.Model):
	member_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	mobile_number = models.IntegerField(unique=True)
	email = models.EmailField(null=True, blank=True)
	address = models.CharField(max_length=300, blank=True)
	admitted_on = models.DateField(auto_now_add=True)
	registration_date = models.DateField()
	registration_upto = models.DateField()
	subscription_type  = models.CharField(max_length=30, choices=SUBSCRIPTION_TYPE_CHOICES)
	subscription_period = models.CharField(max_length=30, choices=SUBSCRIPTION_PERIOD_CHOICES)
	amount = models.IntegerField()
	photo = models.FileField(upload_to='photos/', blank=True)
	notification = models.IntegerField(default=2, blank=True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name


class AddMemberForm(ModelForm):
	class Meta:
		model = Member
		# fields = ['first_name', 'last_name', 'mobile_number', 'email', 'address', 'subscription_type', 'subscription_period', 'amount']
		fields = '__all__'
		exclude = ['registration_upto']
		widgets = {
			'registration_date': forms.DateInput(attrs={'type': 'date'}),
			'registration_upto': forms.DateInput(attrs={'type': 'date'}),
		}

	def clean_mobile_number(self, *args, **kwargs):
		mobile_number = self.cleaned_data.get('mobile_number')
		if Member.objects.filter(mobile_number=mobile_number).exists():
			raise forms.ValidationError('This mobile number has already been registered.')
		else:
			return mobile_number

class SearchForm(forms.Form):
		search = forms.CharField(label='Search Member', max_length=100)

class UpdateMemberForm(forms.Form):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	registration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	registration_upto = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	subscription_type  = forms.ChoiceField(choices=SUBSCRIPTION_TYPE_CHOICES)
	subscription_period = forms.ChoiceField(choices=SUBSCRIPTION_PERIOD_CHOICES)
	amount = forms.IntegerField()
	photo = forms.FileField(label='Update Photo', required=False)

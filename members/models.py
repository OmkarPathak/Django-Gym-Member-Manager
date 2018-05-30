from django.db import models
from django.forms import ModelForm
from django import forms
import datetime

SUBSCRIPTION_TYPE_CHOICES = (
    ('gym', 'Gym'),
    ('cross_fit', 'Cross Fit'),
    ('gym_and_cross_fit', 'Gym + Cross Fit'),
    ('pt', 'Personal Training')
)

SUBSCRIPTION_PERIOD_CHOICES = (
    ('1', '1 Month'),
    ('2', '2 Months'),
    ('3', '3 Months'),
    ('4', '4 Months'),
    ('5', '5 Months'),
    ('6', '6 Months'),
    ('7', '7 Months'),
    ('8', '8 Months'),
    ('9', '9 Months'),
    ('10', '10 Months'),
    ('11', '11 Months'),
    ('12', '12 Months'),
)

FEE_STATUS = (
    ('paid', 'Paid'),
    ('pending', 'Pending'),
)

STATUS = (
    (0, 'Start'),
    (1, 'Stop'),
)

BATCH = (
    ('morning', 'Morning'),
    ('evening', 'Evening'),
)

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(('First Name'), max_length=50)
    last_name = models.CharField(('Last Name'), max_length=50)
    mobile_number = models.CharField(('Mobile Number'), max_length=10, unique=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=300, blank=True)
    medical_history = models.CharField(('Medical History'), max_length=300, blank=True, default='None')
    admitted_on = models.DateField(auto_now_add=True)
    registration_date = models.DateField(('Registration Date'), default='dd/mm/yyyy')
    registration_upto = models.DateField()
    dob = models.DateField(default='dd/mm/yyyy')
    subscription_type  = models.CharField(
                                ('Subscription Type'),
                                max_length=30,
                                choices=SUBSCRIPTION_TYPE_CHOICES,
                                default=SUBSCRIPTION_TYPE_CHOICES[0][0]
                            )
    subscription_period = models.CharField(
                                ('Subscription Period'),
                                max_length=30,
                                choices=SUBSCRIPTION_PERIOD_CHOICES,
                                default=SUBSCRIPTION_PERIOD_CHOICES[0][0]
                            )
    amount = models.CharField(max_length=30)
    fee_status = models.CharField(
                                ('Fee Status'),
                                max_length=30,
                                choices=FEE_STATUS,
                                default=FEE_STATUS[0][0]
                            )
    batch = models.CharField(
                                max_length=30,
                                choices=BATCH,
                                default=BATCH[0][0]
                            )
    photo = models.FileField(upload_to='photos/', blank=True)
    notification = models.IntegerField(default=2, blank=True)
    stop = models.IntegerField(('Status'), choices=STATUS, default=STATUS[0][0], blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class AddMemberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].error_messages = {'required': 'Please enter first name'}
        self.fields['last_name'].error_messages = {'required': 'Please enter last name'}

    class Meta:
        model = Member
        # fields = ['first_name', 'last_name', 'mobile_number', 'email', 'address', 'subscription_type', 'subscription_period', 'amount']
        fields = '__all__'
        exclude = ['registration_upto']
        widgets = {
        'registration_date': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
        'address': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        'medical_history': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        'dob': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
        'photo': forms.FileInput(attrs={'accept': 'image/*;capture=camera'})
        }

    def clean_mobile_number(self, *args, **kwargs):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number.isdigit():
            raise forms.ValidationError('Mobile number should be a number')
        if Member.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError('This mobile number has already been registered.')
        else:
            if len(str(mobile_number)) == 10:
                return mobile_number
            else:
                raise forms.ValidationError('Mobile number should be 10 digits long.')
        return mobile_number

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount.isdigit():
            raise forms.ValidationError('Amount should be a number')
        return amount

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        first_name = cleaned_data.get('first_name').capitalize()
        last_name = cleaned_data.get('last_name').capitalize()
        queryset = Member.objects.filter(
                        first_name=first_name,
                        last_name=last_name,
                        dob=dob
                    ).count()
        if queryset > 0:
            raise forms.ValidationError('This member already exists!')


class SearchForm(forms.Form):
    search = forms.CharField(label='Search Member', max_length=100, required=False)

    def clean_search(self, *args, **kwargs):
        search = self.cleaned_data.get('search')
        if search == '':
            raise forms.ValidationError('Please enter a name in search box')
        return search

class UpdateMemberGymForm(forms.Form):
    registration_date   = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker        form-control', 'type': 'date'}),)
    registration_upto = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),)
    subscription_type  = forms.ChoiceField(choices=SUBSCRIPTION_TYPE_CHOICES)
    subscription_period = forms.ChoiceField(choices=SUBSCRIPTION_PERIOD_CHOICES)
    fee_status = forms.ChoiceField(choices=FEE_STATUS)
    amount = forms.CharField()
    batch = forms.ChoiceField(choices=BATCH)
    stop = forms.ChoiceField(label='Status', choices=STATUS)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount.isdigit():
            raise forms.ValidationError('Amount should be a number')
        return amount

class UpdateMemberInfoForm(forms.Form):
    first_name     = forms.CharField(max_length=50)
    last_name      = forms.CharField(max_length=50)
    photo          = forms.FileField(label='Update Photo', required=False)
    dob            = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker        form-control', 'type': 'date'}),)

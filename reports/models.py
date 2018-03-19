from django.db import models
from members.models import Member
from django.forms import ModelForm
from django.db import models
import datetime, calendar

YEAR_CHOICES = []
for year in range(2016, (datetime.datetime.now().year + 5)):
    YEAR_CHOICES.append((year, year))


MONTHS_CHOICES = tuple(zip(range(1,13), (calendar.month_name[i] for i in range(1,13))))

# Create your models here.
class GenerateReports(models.Model):
    month = models.IntegerField(choices=MONTHS_CHOICES, default=datetime.datetime.now().year, blank=True)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

class GenerateReportForm(ModelForm):
    class Meta:
        model = GenerateReports
        fields = '__all__'

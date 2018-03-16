from django.shortcuts import render
from django.http import HttpResponse
from members.models import Member
import csv
import datetime

# Create your views here.
def export_all(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Email address', 'Subscription Type'])
    members = Member.objects.all().values_list('first_name', 'last_name', 'email', 'subscription_type')
    # print(Member.objects.filter(registration_upto__lte=datetime.datetime.now()).values_list('first_name', 'last_name', 'email', 'subscription_type'))
    for user in members:
        writer.writerow(user)

    return response

def reports(request):
    return render(request, 'reports.html')

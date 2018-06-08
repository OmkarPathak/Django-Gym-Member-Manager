from django.shortcuts import render, redirect
from django.http import HttpResponse
from members.models import Member
import csv
import datetime
from .models import GenerateReportForm
from django.db.models import Q
from notifications.config import get_notification_count

# Create your views here.
def export_all(user_obj):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'DOB', 'Mobile', 'Admission Date', 'Subscription Type', 'Batch'])
    members = user_obj.values_list('first_name', 'last_name', 'dob', 'mobile_number', 'admitted_on', 'subscription_type', 'batch')
    for user in members:
        writer.writerow(user)

    return response

def reports(request):
    if request.method == 'POST':
        form = GenerateReportForm(request.POST)
        if form.is_valid():
            if request.POST.get('month') and request.POST.get('year') and request.POST.get('batch'):
                query = Q(
                    registration_date__month=request.POST.get('month'),
                    registration_date__year=request.POST.get('year'),
                    batch=request.POST.get('batch')
                )
            elif request.POST.get('month') and request.POST.get('year'):
                query = Q(
                    registration_date__month=request.POST.get('month'),
                    registration_date__year=request.POST.get('year')
                )
            elif request.POST.get('month') and request.POST.get('batch'):
                query = Q(
                    registration_date__month=request.POST.get('month'),
                    batch=request.POST.get('batch')
                )
            elif request.POST.get('year') and request.POST.get('batch'):
                query = Q(
                    registration_date__year=request.POST.get('year'),
                    batch=request.POST.get('batch')
                )
            else:
                query = Q(
                    registration_date__year=request.POST.get('year'),
                )
            users = Member.objects.filter(query)
            # aggregate_amount = 0
            # for member in users:
            #     aggregate_amount += member.amount
            if 'export' in request.POST:
                return export_all(users)
            context = {
                'users': users,
                'form': form,
                # 'aggregate_amount': aggregate_amount,
                # 'students_registered': len(reg_users),
                'subs_end_today_count': get_notification_count(),
            }
            return render(request, 'reports.html', context)
    else:
        form = GenerateReportForm()
    return render(request, 'reports.html', {'form': form, 'subs_end_today_count': get_notification_count(),})

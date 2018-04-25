from django.shortcuts import render, redirect
from django.http import HttpResponse
from members.models import Member
import csv
import datetime
from .models import GenerateReportForm

# Create your views here.
def export_all(user):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Email address', 'Admission Date'])
    members = user.values_list('first_name', 'last_name', 'email', 'admitted_on')
    # print(Member.objects.filter(registration_upto__lte=datetime.datetime.now()).values_list('first_name', 'last_name', 'email', 'subscription_type'))
    for user in members:
        writer.writerow(user)

    return response

def reports(request):
    subs_end_today_count = Member.objects.filter(
                                                registration_upto=datetime.datetime.now(),
                                                notification=1).count()
    if request.method == 'POST':
        form = GenerateReportForm(request.POST)
        if form.is_valid():
            if request.POST.get('month') and request.POST.get('year'):
                users = Member.objects.filter(
                                                registration_date__month=request.POST.get('month'),
                                                registration_date__year=request.POST.get('year')
                                              )
                reg_users = Member.objects.filter(
                                                admitted_on__month=request.POST.get('month'),
                                                admitted_on__year=request.POST.get('year')
                                              )
            elif request.POST.get('month'):
                users = Member.objects.filter(registration_date__month=request.POST.get('month'))
                reg_users = Member.objects.filter(admitted_on__month=request.POST.get('month'))
            else:
                users = Member.objects.filter(registration_date__year=request.POST.get('year'))
                reg_users = Member.objects.filter(admitted_on__year=request.POST.get('year'))
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
                'subs_end_today_count': subs_end_today_count,
            }
            return render(request, 'reports.html', context)
    else:
        form = GenerateReportForm()
    return render(request, 'reports.html', {'form': form, 'subs_end_today_count': subs_end_today_count,})

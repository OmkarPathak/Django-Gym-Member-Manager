from django.shortcuts import render, redirect
from members.models import Member, FEE_STATUS
import datetime
from django.db.models import Q
from .config import get_notification_count, run_notifier

# Create your views here.
def notifications(request):
    run_notifier()
    members_before = Member.objects.filter(
                                        registration_upto__lte=datetime.datetime.now(),
                                        notification=1)
    members_today = Member.objects.filter(
                                        registration_upto__gte=datetime.datetime.now(),
                                        registration_upto__lte=datetime.date.today() + datetime.timedelta(days=1),
                                        notification=1)
    pending = Member.objects.filter(fee_status='pending', notification=1)
    context = {
        'subs_end_today_count': get_notification_count(),
        'members_today': members_today,
        'members_before': members_before | pending,
    }
    # Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
    return render(request, 'notifications.html', context)

def notification_delete(request, id):
    member = Member.objects.get(pk=id)
    member.notification = 0
    member.save()
    members_before = Member.objects.filter(
                registration_upto__lte=datetime.datetime.now(),
                notification=1)
    members_today = Member.objects.filter(
                registration_upto__gte=datetime.datetime.now(),
                registration_upto__lte=datetime.date.today() + datetime.timedelta(days=1),
                notification=1)
    pending = Member.objects.filter(fee_status='pending')

    context = {
        'subs_end_today_count': get_notification_count(),
        'members_today': members_today,
        'members_before': members_before,
    }
    return redirect('/notifications/')

from django.shortcuts import render
from members.models import Member
import datetime

# Create your views here.
def notifications(request):
    last_5_days = datetime.date.today() - datetime.timedelta(days=5)
    members_before = Member.objects.filter(
                                        registration_upto__lte=datetime.datetime.now(),
                                        registration_upto__gte=last_5_days,
                                        notification=2)
    subs_end_today_count = Member.objects.filter(registration_upto=datetime.datetime.now(),
                                        notification=2).count()
    members_today = Member.objects.filter(registration_upto=datetime.datetime.now(),
                                        notification=2)

    # make notification flag to 1
    for member in members_today:
        if member.notification != 0:
            member.notification = 1

    for member in members_before:
        if member.notification != 0:
            member.notification = 1

    context = {
        'subs_end_today_count': subs_end_today_count,
        'members_today': members_today,
        'members_before': members_before,
    }
    # Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
    return render(request, 'notifications.html', context)

def notification_delete(request, id):
    member = Member.objects.get(pk=id)
    member.notification = 0
    member.save()
    last_5_days = datetime.date.today() - datetime.timedelta(days=5)
    members_before = Member.objects.filter(
                                        registration_upto__lte=datetime.datetime.now(),
                                        registration_upto__gte=last_5_days,
                                        notification=2)
    subs_end_today_count = Member.objects.filter(
                                            registration_upto=datetime.datetime.now(),
                                            notification=1).count()
    members_today = Member.objects.filter(registration_upto=datetime.datetime.now(),
                                        notification=2)

    context = {
        'subs_end_today_count': subs_end_today_count,
        'members_today': members_today,
        'members_before': members_before,
    }
    return render(request, 'notifications.html', context)

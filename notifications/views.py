from django.shortcuts import render, redirect
from members.models import Member, FEE_STATUS
import datetime
from django.db.models import Q

query = Q(
        Q(registration_upto__lte=datetime.datetime.now()),
        Q(notification=2))
query.add = Q(
        Q(registration_upto__lte=datetime.datetime.now()),
        Q(notification=0),
        Q.OR)

# Create your views here.
def notifications(request):
    # last_5_days = datetime.date.today() - datetime.timedelta(days=5)
    members_before = Member.objects.filter(query)
    members_today = Member.objects.filter(query)

    # make notification flag to 1
    for member in members_today:
        if member.notification != 0:
            member.notification = 1
            member.fee_status = 'pending'
            member.save()

    for member in members_before:
        if member.notification != 0:
            member.notification = 1
            member.fee_status = 'pending'
            member.save()

    members_before = Member.objects.filter(
                                        registration_upto__lt=datetime.datetime.now(),
                                        notification=1)
    members_today = Member.objects.filter(
                                        registration_upto=datetime.datetime.now(),
                                        notification=1)

    subs_end_today_count = Member.objects.filter(
                                        registration_upto=datetime.datetime.now(),
                                        notification=1).count()
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
    members_before = Member.objects.filter(
                                        registration_upto__lt=datetime.datetime.now(),
                                        notification=2)
    subs_end_today_count = Member.objects.filter(
                                            registration_upto=datetime.datetime.now(),
                                            notification=1).count()
    members_today = Member.objects.filter(
                                        registration_upto__lte=datetime.datetime.now(),
                                        notification=2)

    context = {
        'subs_end_today_count': subs_end_today_count,
        'members_today': members_today,
        'members_before': members_before,
    }
    return redirect('/notifications/')

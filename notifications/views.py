from django.shortcuts import render, redirect
from members.models import Member, FEE_STATUS
import datetime
from django.db.models import Q
from .config import get_notification_count
import dateutil.relativedelta as delta
import dateutil.parser as parser
import datetime
from django.db.models.signals import post_save

# Create your views here.
def notifications(request):
    # run_notifier()
    members_before = Member.objects.filter(
                                        Q(registration_upto__lte=datetime.datetime.now(),
                                        notification=1) |
                                        Q(fee_status='pending', notification=1)
                                        ).order_by('first_name')
    members_today = Member.objects.filter(
                                        registration_upto__gte=datetime.datetime.now(),
                                        registration_upto__lte=datetime.date.today() + datetime.timedelta(days=1),
                                        notification=1).order_by('first_name')

    context = {
        'subs_end_today_count': get_notification_count(),
        'members_today': members_today,
        'members_before': members_before,
    }
    # Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
    return render(request, 'notifications.html', context)

def notification_delete(request, id):
    member = Member.objects.get(pk=id)
    member.notification = 0
    post_save.disconnect(my_handler, sender=Member)
    member.save()
    post_save.connect(my_handler, sender=Member)
    return redirect('/notifications/')

def my_handler(sender, instance, created, **kwargs):
    query = Q(
            Q(registration_upto__gte=datetime.datetime.today()),
            Q(registration_upto__lte=datetime.datetime.today() + datetime.timedelta(days=1)),
            Q(Q(notification=2) | Q(notification=0)))

    # last_5_days = datetime.date.today() - datetime.timedelta(days=5)
    members_before = Member.objects.filter(
        registration_upto__lte=datetime.datetime.today())
    members_today = Member.objects.filter(query)

    count = 0
    # make notification flag to 1
    for member in members_today | members_before:
        if member.notification != 0:
            member.notification = 1
            member.fee_status = 'pending'
            member.save()
    return

post_save.connect(my_handler, sender=Member)

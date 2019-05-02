from django.shortcuts import render, redirect
from members.models import Member, FEE_STATUS
import datetime
from django.db.models import Q
from .config import get_notification_count, run_notifier
import dateutil.relativedelta as delta
import dateutil.parser as parser
import datetime
from django.db.models.signals import post_save, pre_save
from .config import my_handler

# Create your views here.
def notifications(request):
    # run_notifier()
    morning_members_before = Member.objects.filter(
                                        Q(registration_upto__lte=datetime.datetime.now(),
                                        notification=1, batch='morning') |
                                        Q(fee_status='pending', notification=1, batch='morning')
                                        ).exclude(stop=1).order_by('first_name')
    morning_members_today = Member.objects.filter(
                                        registration_upto__gte=datetime.datetime.now(),
                                        registration_upto__lte=datetime.date.today() + datetime.timedelta(days=2),
                                        notification=1, batch='morning').exclude(stop=1).order_by('first_name')

    evening_members_before = Member.objects.filter(
                                        Q(registration_upto__lte=datetime.datetime.now(),
                                        notification=1, batch='evening') |
                                        Q(fee_status='pending', notification=1, batch='evening')
                                        ).exclude(stop=1).order_by('first_name')
    evening_members_today = Member.objects.filter(
                                        registration_upto__gte=datetime.datetime.now(),
                                        registration_upto__lte=datetime.date.today() + datetime.timedelta(days=2),
                                        notification=1, batch='evening').exclude(stop=1).order_by('first_name')

    context = {
        'subs_end_today_count': get_notification_count(),
        'morning_members_today': morning_members_today,
        'morning_members_before': morning_members_before,
        'evening_members_today': evening_members_today,
        'evening_members_before': evening_members_before,
    }
    # Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
    return render(request, 'notifications.html', context)

def notification_delete(request, id):
    member = Member.objects.get(pk=id)
    member.notification = 0
    member.stop = 1
    post_save.disconnect(my_handler, sender=Member)
    member.save()
    post_save.connect(my_handler, sender=Member)
    return redirect('/notifications/')

# post_save.connect(my_handler, sender=Member)
# pre_save.connect(run_notifier, sender=Member)

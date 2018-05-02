# Notification Count
from members.models import Member
import datetime

def run_notifier():
    from django.db.models import Q

    query = Q(
            Q(registration_upto__gte=datetime.datetime.now()),
            Q(registration_upto__lte=datetime.datetime.now() + datetime.timedelta(days=1)),
            Q(notification=2))
    query.add = Q(
            Q(registration_upto__gte=datetime.datetime.now()),
            Q(registration_upto__lte=datetime.datetime.now() + datetime.timedelta(days=1)),
            Q(notification=0),
            Q.OR)

    # last_5_days = datetime.date.today() - datetime.timedelta(days=5)
    members_before = Member.objects.filter(
        registration_upto__lte=datetime.datetime.now())
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

def get_notification_count():
    NOTIF_COUNT = Member.objects.filter(
        registration_upto__gte=datetime.datetime.now(),
        registration_upto__lte=datetime.date.today() + datetime.timedelta(days=2),
        notification=1).count()
    PENDING_COUNT = Member.objects.filter(fee_status='pending', notification=1).count()
    return NOTIF_COUNT + PENDING_COUNT

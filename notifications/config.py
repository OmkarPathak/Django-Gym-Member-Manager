# Notification Count
from members.models import Member
import datetime
from django.db.models import Q
from django.db.models.signals import post_save

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

def run_notifier(**kwargs):
    query = Q(
            Q(registration_upto__gte=datetime.datetime.today()),
            Q(registration_upto__lte=datetime.datetime.today() + datetime.timedelta(days=1)),
            Q(Q(notification=2) | Q(notification=0)))

    # last_5_days = datetime.date.today() - datetime.timedelta(days=5)
    members_before = Member.objects.filter(
        registration_upto__lte=datetime.datetime.today()).exclude(stop=1)
    members_today = Member.objects.filter(query).exclude(stop=1)

    count = 0
    # make notification flag to 1
    for member in members_today | members_before:
        if member.notification != 0:
            member.notification = 1
            member.fee_status = 'pending'
            post_save.disconnect(my_handler, sender=Member)
            member.save()
            post_save.connect(my_handler, sender=Member)
    return

def get_notification_count():
    NOTIF_COUNT = Member.objects.filter(
        registration_upto__gte=datetime.datetime.now(),
        registration_upto__lte=datetime.date.today() + datetime.timedelta(days=1),
        notification=1).exclude(stop=1)
    PENDING_COUNT = Member.objects.filter(fee_status='pending', notification=1).exclude(stop=1)
    return (NOTIF_COUNT | PENDING_COUNT).distinct().count()

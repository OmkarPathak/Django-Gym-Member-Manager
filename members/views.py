from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from .models import AddMemberForm, Member, SearchForm, UpdateMemberForm
import datetime
import dateutil.relativedelta as delta
import dateutil.parser as parser
from django.core.files.storage import FileSystemStorage
from payments.models import Payments

# Get the count of notification (notification will be incremented if the user's fee due date is today!)
subs_end_today_count = Member.objects.filter(
                                            registration_upto=datetime.datetime.now(),
                                            notification=2
                                            ).count()

def members(request):
    view_all = Member.objects.all()
    form = AddMemberForm()
    search_form = SearchForm()
    # get all members according to their batches
    evening = Member.objects.filter(batch='evening')
    morning = Member.objects.filter(batch='morning')
    context = {
        'form': form,
        'morning': morning,
        'evening': evening,
        'search_form': search_form,
        'subs_end_today_count': subs_end_today_count,
    }
    return render(request, 'tab_base.html', context)

def add_member(request):
    view_all = Member.objects.all()
    subs_end_today_count = Member.objects.filter(
                                            registration_upto=datetime.datetime.now(),
                                            notification=2).count()
    search_form = SearchForm()
    success = 0
    if request.method == 'POST':
        form = AddMemberForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.registration_upto = parser.parse(request.POST.get('registration_date')) + delta.relativedelta(months=int(request.POST.get('subscription_period')))
            temp.save()
            success = 'Successfully Added Member'

            # Add payments if payment is 'paid'
            if temp.fee_status == 'paid':
                payments = Payments(
                                    user=temp,
                                    payment_date=temp.registration_date,
                                    payment_period=temp.subscription_period,
                                    payment_amount=temp.amount)
                payments.save()

            form = AddMemberForm()
        # get all members according to their batches
        evening = Member.objects.filter(batch='evening')
        morning = Member.objects.filter(batch='morning')

        context = {
            'add_success': success,
            'form': form,
            'morning': morning,
            'evening': evening,
            'search_form': search_form,
            'subs_end_today_count': subs_end_today_count,
        }
        return render(request, 'tab_base.html', context)
    else:
        # get all members according to their batches
        evening = Member.objects.filter(batch='evening')
        morning = Member.objects.filter(batch='morning')
        form = AddMemberForm()
        context = {
            'form': form,
            'morning': morning,
            'evening': evening,
            'search_form': search_form,
            'subs_end_today_count': subs_end_today_count,
        }
    return render(request, 'tab_base.html', context)

def search_member(request):
    if request.method == 'POST':
        # search_form = SearchForm(request.POST)
        first_name = request.POST.get('search')
        check = Member.objects.filter(first_name__contains=first_name)
        check = serializers.serialize('json', check)
        context = {}
        context['search'] = check
        return JsonResponse(data=context, safe=False)
    else:
        search_form = SearchForm()
    return render(request, 'tab_base.html', {'search_form': search_form})

def delete_member(request, id):
    Member.objects.filter(pk=id).delete()
    view_all = Member.objects.all()
    form = AddMemberForm()
    search_form = SearchForm()

    # get all members according to their batches
    evening = Member.objects.filter(batch='evening')
    morning = Member.objects.filter(batch='morning')
    context = {
        'form': form,
        'morning': morning,
        'evening': evening,
        'search_form': search_form,
        'deleted': 'User Deleted Successfully',
        'subs_end_today_count': subs_end_today_count,
    }
    return render(request, 'tab_base.html', context)

def update_member(request, id):
    if request.method == 'POST':
        object = Member.objects.get(pk=id)
        object.first_name = request.POST.get('first_name')
        object.last_name = request.POST.get('last_name')
        object.registration_date =  request.POST.get('registration_date')
        object.registration_upto =  parser.parse(request.POST.get('registration_date')) + delta.relativedelta(months=int(request.POST.get('subscription_period')))
        object.subscription_type =  request.POST.get('subscription_type')
        object.fee_status = request.POST.get('fee_status')
        object.amount =  request.POST.get('amount')
        object.notification =  2

        # for updating photo
        if 'photo' in request.FILES:
            myfile = request.FILES['photo']
            fs = FileSystemStorage(base_url="")
            photo = fs.save(myfile.name, myfile)
            object.photo = fs.url(photo)
        object.save()

        # Add payments if payment is 'paid'
        if object.fee_status == 'paid':
            payments = Payments(
                                user=object,
                                payment_date=object.registration_date,
                                payment_period=object.subscription_period,
                                payment_amount=object.amount)
            payments.save()

        user = Member.objects.get(pk=id)
        form = UpdateMemberForm(initial={
                                'registration_date': user.registration_date,
                                'registration_upto': user.registration_upto,
                                'subscription_type': user.subscription_type,
                                'subscription_period': user.subscription_period,
                                'amount': user.amount,
                                'fee_status': user.fee_status,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                })

        try:
            payments = Payments.objects.filter(user=user)
        except Payments.DoesNotExist:
            payments = 'No Records'

        return render(request,
            'update.html',
            {
                'payments': payments,
                'form': form,
                'user': user,
                'updated': 'Record Updated Successfully',
                'subs_end_today_count': subs_end_today_count,
            })
    else:
        user = Member.objects.get(pk=id)

        if len(Payments.objects.filter(user=user)) > 0:
            payments = Payments.objects.filter(user=user)
        else:
            payments = 'No Records'
        form = UpdateMemberForm(initial={
                                'registration_date': user.registration_date,
                                'registration_upto': user.registration_upto,
                                'subscription_type': user.subscription_type,
                                'subscription_period': user.subscription_period,
                                'amount': user.amount,
                                'fee_status': user.fee_status,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                })
    return render(request,
                    'update.html',
                    {
                        'payments': payments,
                        'form': form,
                        'user': user,
                        'subs_end_today_count': subs_end_today_count,
                    }
                )

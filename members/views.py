from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from .models import AddMemberForm, Member, SearchForm, UpdateMemberGymForm, UpdateMemberInfoForm
import datetime, csv
from django.http import HttpResponse
import dateutil.relativedelta as delta
import dateutil.parser as parser
from django.core.files.storage import FileSystemStorage
from payments.models import Payments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Export user information.
def export_all(user_obj):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Mobile', 'Admission Date', 'Subscription Type', 'Batch'])
    members = user_obj.values_list('first_name', 'last_name', 'mobile_number', 'admitted_on', 'subscription_type', 'batch')
    for user in members:
        first_name = user[0]
        last_name = user[1]
        writer.writerow(user)

    response['Content-Disposition'] = 'attachment; filename="' + first_name + ' ' + last_name + '.csv"'
    return response

# Get the count of notification (notification will be incremented if the user's fee due date is today!)
subs_end_today_count = Member.objects.filter(
                                            registration_upto__lte=datetime.datetime.now(),
                                            registration_upto__gte=datetime.date.today() - datetime.timedelta(days=2),
                                            notification=1
                                            ).count()

def members(request):
    # Get the count of notification (notification will be incremented if the user's fee due date is today!)
    subs_end_today_count = Member.objects.filter(
                                            registration_upto__lte=datetime.datetime.now(),
                                            registration_upto__gte=datetime.date.today() - datetime.timedelta(days=2),
                                            notification=1
                                            ).count()
    form = AddMemberForm()
    context = {
        'form': form,
        'subs_end_today_count': subs_end_today_count,
    }
    return render(request, 'add_member.html', context)

def view_member(request):
    # Get the count of notification (notification will be incremented if the user's fee due date is today!)
    subs_end_today_count = Member.objects.filter(
                                            registration_upto__lte=datetime.datetime.now(),
                                            registration_upto__gte=datetime.date.today() - datetime.timedelta(days=2),
                                            notification=1
                                            ).count()
    view_all = Member.objects.all()
    paginator = Paginator(view_all, 100)
    try:
        page = request.GET.get('page', 1)
        view_all = paginator.page(page)
    except PageNotAnInteger:
        view_all = paginator.page(1)
    except EmptyPage:
        view_all = paginator.page(paginator.num_pages)
    search_form = SearchForm()
    # get all members according to their batches
    evening = Member.objects.filter(batch='evening')
    morning = Member.objects.filter(batch='morning')
    context = {
        'all': view_all,
        'morning': morning,
        'evening': evening,
        'search_form': search_form,
        'subs_end_today_count': subs_end_today_count,
    }
    return render(request, 'view_member.html', context)

def add_member(request):
    view_all = Member.objects.all()
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

        context = {
            'add_success': success,
            'form': form,
            'subs_end_today_count': subs_end_today_count,
        }
        return render(request, 'add_member.html', context)
    else:
        form = AddMemberForm()
        context = {
            'form': form,
            'subs_end_today_count': subs_end_today_count,
        }
    return render(request, 'add_member.html', context)

def search_member(request):
    if request.method == 'POST':
        # search_form = SearchForm(request.POST)
        # first_name = request.POST.get('search')
        # check = Member.objects.filter(first_name__contains=first_name)
        # check = serializers.serialize('json', check)
        # context = {}
        # context['search'] = check
        if 'clear' in request.POST:
            return redirect('view_member')
        search_form = SearchForm(request.POST)
        result = 0
        if search_form.is_valid():
            first_name = request.POST.get('search')
            result = Member.objects.filter(first_name__contains=first_name)

        view_all = Member.objects.all()
        # get all members according to their batches
        evening = Member.objects.filter(batch='evening')
        morning = Member.objects.filter(batch='morning')

        context = {
            'all': view_all,
            'morning': morning,
            'evening': evening,
            'search_form': search_form,
            'result': result,
            'subs_end_today_count': subs_end_today_count,
        }
        return render(request, 'view_member.html', context)
    else:
        search_form = SearchForm()
    return render(request, 'view_member.html', {'search_form': search_form})

def delete_member(request, id):
    Member.objects.filter(pk=id).delete()
    return redirect('view_member')

def update_member(request, id):
    subs_end_today_count = Member.objects.filter(
                                            registration_upto__lte=datetime.datetime.now(),
                                            registration_upto__gte=datetime.date.today() - datetime.timedelta(days=2),
                                            notification=1
                                            ).count()
    if request.method == 'POST' and request.POST.get('export'):
        return export_all(Member.objects.filter(pk=id))
    if request.method == 'POST' and request.POST.get('gym_membership'):
        object = Member.objects.get(pk=id)
        object.registration_date =  request.POST.get('registration_date')
        day = parser.parse(request.POST.get('registration_date')).day
        last_day = parser.parse(str(object.registration_upto)).day

        month = parser.parse(request.POST.get('registration_date')).month
        last_month = parser.parse(str(object.registration_upto)).month
        # check if user has modified only the date
        if (day != last_day and month == last_month) or (request.POST.get('fee_status') == 'pending'):
            object.registration_upto =  parser.parse(request.POST.get('registration_date'))
            object.fee_status = request.POST.get('fee_status')
            object.amount = request.POST.get('amount')
            object.save()
        else:
            object.registration_upto =  parser.parse(request.POST.get('registration_date')) + delta.relativedelta(months=int(request.POST.get('subscription_period')))
            object.subscription_type =  request.POST.get('subscription_type')
            object.subscription_period =  request.POST.get('subscription_period')
            object.fee_status = request.POST.get('fee_status')
            object.amount =  request.POST.get('amount')
            object.notification =  2
            object.save()

            # Add payments if payment is 'paid'
            if object.fee_status == 'paid':
                check = Payments.objects.filter(
                    payment_date=object.registration_date,
                    user__pk=object.pk).count()
                if check == 0:
                    payments = Payments(
                                        user=object,
                                        payment_date=object.registration_date,
                                        payment_period=object.subscription_period,
                                        payment_amount=object.amount)
                    payments.save()
        subs_end_today_count = Member.objects.filter(
                                            registration_upto=datetime.datetime.now(),
                                            notification=1
                                            ).count()
        user = Member.objects.get(pk=id)
        gym_form = UpdateMemberGymForm(initial={
                                'registration_date': user.registration_upto,
                                'registration_upto': user.registration_upto,
                                'subscription_type': user.subscription_type,
                                'subscription_period': user.subscription_period,
                                'amount': user.amount,
                                'fee_status': user.fee_status,
                                })

        info_form = UpdateMemberInfoForm(initial={
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
                'gym_form': gym_form,
                'info_form': info_form,
                'user': user,
                'updated': 'Record Updated Successfully',
                'subs_end_today_count': subs_end_today_count,
            })
    elif request.method == 'POST' and request.POST.get('info'):
        object = Member.objects.get(pk=id)
        object.first_name = request.POST.get('first_name')
        object.last_name = request.POST.get('last_name')

        # for updating photo
        if 'photo' in request.FILES:
            myfile = request.FILES['photo']
            fs = FileSystemStorage(base_url="")
            photo = fs.save(myfile.name, myfile)
            object.photo = fs.url(photo)
        object.save()

        user = Member.objects.get(pk=id)
        gym_form = UpdateMemberGymForm(initial={
                                'registration_date': user.registration_upto,
                                'registration_upto': user.registration_upto,
                                'subscription_type': user.subscription_type,
                                'subscription_period': user.subscription_period,
                                'amount': user.amount,
                                'fee_status': user.fee_status,
                                })

        info_form = UpdateMemberInfoForm(initial={
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
                'gym_form': gym_form,
                'info_form': info_form,
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
        gym_form = UpdateMemberGymForm(initial={
                                'registration_date': user.registration_upto,
                                'registration_upto': user.registration_upto,
                                'subscription_type': user.subscription_type,
                                'subscription_period': user.subscription_period,
                                'amount': user.amount,
                                'fee_status': user.fee_status,
                                })

        info_form = UpdateMemberInfoForm(initial={
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                })
    return render(request,
                    'update.html',
                    {
                        'payments': payments,
                        'gym_form': gym_form,
                        'info_form': info_form,
                        'user': user,
                        'subs_end_today_count': subs_end_today_count,
                    }
                )

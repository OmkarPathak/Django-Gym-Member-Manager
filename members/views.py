from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from .models import AddMemberForm, Member, SearchForm, UpdateMemberForm
import datetime

# Create your views here.
def members(request):
    subs_end_today_count = Member.objects.filter(registration_upto=datetime.datetime.now()).count()
    view_all = Member.objects.all()
    form = AddMemberForm()
    search_form = SearchForm()
    context = {
        'form': form,
        'view_all': view_all,
        'search_form': search_form,
        'subs_end_today_count': subs_end_today_count,
    }
    return render(request, 'tab_base.html', context)

def add_member(request):
    view_all = Member.objects.all()
    subs_end_today_count = Member.objects.filter(registration_upto=datetime.datetime.now()).count()
    search_form = SearchForm()
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            form.save()
            form = AddMemberForm()
        context = {
            'add_success': 'Successfully Added Member',
            'form': form,
            'view_all': view_all,
            'search_form': search_form,
            'subs_end_today_count': subs_end_today_count,
        }
        return render(request, 'tab_base.html', context)
    else:
        form = AddMemberForm()
        context = {
            'form': form,
            'view_all': view_all,
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
    subs_end_today_count = Member.objects.filter(registration_upto=datetime.datetime.now()).count()
    Member.objects.filter(pk=id).delete()
    view_all = Member.objects.all()
    form = AddMemberForm()
    search_form = SearchForm()
    context = {
        'form': form,
        'view_all': view_all,
        'search_form': search_form,
        'deleted': 'User Deleted Successfully',
        'subs_end_today_count': subs_end_today_count,
    }
    return render(request, 'tab_base.html', context)

def update_member(request, id):
    if request.method == 'POST':
        object = Member.objects.get(pk=id)
        object.registration_date =  request.POST.get('registration_date')
        object.registration_upto =  request.POST.get('registration_upto')
        object.subscription_type =  request.POST.get('subscription_type')
        object.subscription_period =  request.POST.get('subscription_period')
        object.amount =  request.POST.get('amount')
        object.save()
        user = Member.objects.get(pk=id)
        subs_end_today_count = Member.objects.filter(registration_upto=datetime.datetime.now()).count()
        form = UpdateMemberForm(initial={
                                'registration_date': user.registration_date,
                                'registration_upto': user.registration_upto,
                                'subscription_type': user.subscription_type,
                                'subscription_period': user.subscription_period,
                                'amount': user.amount
                                })
        return render(request,
            'update.html',
            {
                'form': form,
                'user': user,
                'updated': 'Record Updated Successfully',
                'subs_end_today_count': subs_end_today_count,
            })
    else:
        user = Member.objects.get(pk=id)
        subs_end_today_count = Member.objects.filter(registration_upto=datetime.datetime.now()).count()
        form = UpdateMemberForm(initial={
                                'registration_date': user.registration_date,
                                'registration_upto': user.registration_upto,
                                'subscription_type': user.subscription_type,
                                'subscription_period': user.subscription_period,
                                'amount': user.amount
                                })
    return render(request,
                    'update.html',
                    {
                        'form': form,
                        'user': user,
                        'subs_end_today_count': subs_end_today_count,
                    }
                )

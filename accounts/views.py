from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from .models import Wallpaper, WallpaperForm
from django.conf import settings
from notifications.config import get_notification_count, run_notifier

def homepage(request):
    return render(request, 'homepage.html')

def homepage_after_login(request):
    # run_notifier()
    if not Wallpaper.objects.filter()[:1].exists():
        return render(request, 'homepage_after_login.html')
    else:
        wallpaper = Wallpaper.objects.filter()[:1].get()
        return render(request, 'homepage_after_login.html', {'wallpaper': wallpaper, 'subs_end_today_count': get_notification_count()})

def set_wallpaper(request):
    if request.method == 'POST':
        form = WallpaperForm(request.POST, request.FILES)
        if form.is_valid():
            if Wallpaper.objects.filter()[:1].exists():
                object = Wallpaper.objects.filter()[:1].get()
                # for updating photo
                if 'photo' in request.FILES:
                    myfile = request.FILES['photo']
                    fs = FileSystemStorage(base_url=settings.WALLPAPER_URL, location=settings.WALLPAPER_FILES)
                    photo = fs.save(myfile.name, myfile)
                    object.photo = fs.url(photo)
                object.save()
            else:
                form.save()
        return render(request, 'set_wallpaper.html', {'form': WallpaperForm(), 'success':'Successfully Changed the Wallpaper!'})
    else:
        return render(request, 'set_wallpaper.html', {'form': WallpaperForm()})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,
        'subs_end_today_count': get_notification_count()
    })

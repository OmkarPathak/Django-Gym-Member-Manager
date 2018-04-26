from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.core.files.storage import FileSystemStorage
from .models import Wallpaper, WallpaperForm
from django.conf import settings

def homepage(request):
    return render(request, 'homepage.html')

def homepage_after_login(request):
    if not Wallpaper.objects.filter()[:1].exists():
        return render(request, 'homepage_after_login.html')
    else:
        wallpaper = Wallpaper.objects.filter()[:1].get()
        return render(request, 'homepage_after_login.html', {'wallpaper': wallpaper})

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

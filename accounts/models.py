from django.db import models
from django.forms import ModelForm

# Create your models here.
class Wallpaper(models.Model):
    photo = models.FileField(upload_to='wallpaper/')

class WallpaperForm(ModelForm):
    class Meta:
        model = Wallpaper
        fields = '__all__'

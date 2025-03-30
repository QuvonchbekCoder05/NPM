from django.contrib import admin
from .models import UploadedFile, ImageFile, MP3File

admin.site.register(UploadedFile)
admin.site.register(ImageFile)
admin.site.register(MP3File)

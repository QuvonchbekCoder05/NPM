from django.db import models


class UploadedFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ImageFile(models.Model):
    parent = models.ForeignKey(
        UploadedFile, related_name="images", on_delete=models.CASCADE
    )
    img_url = models.URLField()


class MP3File(models.Model):
    parent = models.ForeignKey(
        UploadedFile, related_name="mp3s", on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="mp3/")

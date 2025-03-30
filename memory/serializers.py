from rest_framework import serializers
from .models import UploadedFile, ImageFile, MP3File


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = "__all__"


class MP3FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MP3File
        fields = "__all__"


class UploadedFileSerializer(serializers.ModelSerializer):
    images = ImageFileSerializer(many=True, read_only=True)
    mp3s = MP3FileSerializer(many=True, read_only=True)

    class Meta:
        model = UploadedFile
        fields = "__all__"

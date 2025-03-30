import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UploadedFile, ImageFile, MP3File
from .serializers import UploadedFileSerializer
from django.conf import settings  # settings-modulni import qilamiz


class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        uploaded_post = UploadedFile.objects.create()
        img_files = request.FILES.getlist("image")
        mp3_files = request.FILES.getlist("MP3")

        # Yuklanishi kerak bo'lgan tasvirlar va MP3 fayllari ro'yxatini saqlash
        successfully_uploaded_images = []
        errors = []

        # Rasmlarni ImageBB'ga yuklash va URL'larni saqlash
        for img in img_files:
            try:
                response = requests.post(
                    "https://api.imgbb.com/1/upload",
                    params={
                        "key": settings.IMGBB_API_KEY
                    },  # settings yordamida API kalitini olish
                    files={"image": img},
                )
                if response.status_code == 200:
                    img_url = response.json().get("data", {}).get("url", "")
                    ImageFile.objects.create(parent=uploaded_post, img_url=img_url)
                    successfully_uploaded_images.append(img_url)
                else:
                    errors.append(
                        f"Failed to upload image {img.name}: {response.json().get('error', 'Unknown error')}"
                    )
            except Exception as e:
                errors.append(f"Error uploading image {img.name}: {str(e)}")

        # MP3 fayllarni yuklash
        for mp3 in mp3_files:
            try:
                MP3File.objects.create(parent=uploaded_post, file=mp3)
            except Exception as e:
                errors.append(f"Error uploading MP3 {mp3.name}: {str(e)}")

        if errors:
            return Response(
                {"message": "Some files failed to upload", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Files uploaded successfully",
                "post_id": uploaded_post.id,
                "images": successfully_uploaded_images,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, post_id=None):
        if post_id:
            post = get_object_or_404(UploadedFile, id=post_id)
            serializer = UploadedFileSerializer(post)
        else:
            posts = UploadedFile.objects.all()
            serializer = UploadedFileSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        post = get_object_or_404(UploadedFile, id=post_id)
        post.delete()
        return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)

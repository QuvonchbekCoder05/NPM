from django.urls import path
from .views import UploadFileView

urlpatterns = [
    path("upload/", UploadFileView.as_view(), name="file-upload"),
    path("upload/<int:post_id>/", UploadFileView.as_view(), name="file-detail"),
]

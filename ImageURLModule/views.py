from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.conf import settings
from .serializers import ImageUploadSerializer


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if files are included in the request
        if 'image' not in request.FILES:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        files = request.FILES.getlist('image')  # Get all uploaded images under the 'image' field

        image_urls = []
        for file in files:
            # Save each image to the media folder
            file_path = default_storage.save(f"images/{file.name}", file)
            file_url = settings.MEDIA_URL + file_path
            image_urls.append(file_url)

        return Response({"image_urls": image_urls}, status=status.HTTP_201_CREATED)

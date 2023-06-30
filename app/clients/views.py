from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .serializers import ClientSerializer

from PIL import Image


@api_view(['POST'])
def client_create(request):
    if request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            avatar = client.avatar
            if avatar:
                image = Image.open(avatar.path)

                watermark = Image.open('clients/watermark.png').convert('RGBA')

                watermark = watermark.resize((100, 100))

                image.paste(watermark, (0, 0), watermark)

                image.save(avatar.path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

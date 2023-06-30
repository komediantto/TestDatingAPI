from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import Client, Match
from .serializers import ClientSerializer

from PIL import Image
from django.core.mail import send_mail


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


@api_view(['POST'])
def match(request, pk):
    if request.method == 'POST':
        try:
            client = Client.objects.get(id=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        current_client = request.user
        client.liked_by.add(current_client)
        if mutual_sympathy(client, current_client):
            send_mail(
                'Взаимная симпатия',
                f'Вы понравились {current_client.first_name}! \
                    Почта участника: {current_client.email}',
                'from@example.com', [client.email], fail_silently=False,
            )
            send_mail(
                'Взаимная симпатия',
                f'Вы понравились {client.first_name}! \
                    Почта участника: {client.email}',
                'from@example.com', [current_client.email],
                fail_silently=False,
            )

            return Response(
                {'message': 'Mutual sympathy! Email has been sent.'},
                status=200)

        return Response({'message': 'Sympathy not mutual.'},
                        status=status.HTTP_200_OK)


def mutual_sympathy(client1, client2):
    if client1.liked_by.filter(id=client2.id).exists() and \
            client2.liked_by.filter(id=client1.id).exists():
        Match.objects.create(client1=client1, client2=client2)
        return True

    return False

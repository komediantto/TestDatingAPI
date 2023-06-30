from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import Client, Match
from .serializers import ClientSerializer

from PIL import Image
from django.core.mail import send_mail
from math import radians, sin, cos, sqrt, atan2


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


@api_view(['GET'])
def client_list(request):
    if request.method == 'GET':
        filters = {}

        sex = request.GET.get('sex')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        distance = request.GET.get('distance')

        if sex:
            filters['sex'] = sex
        if first_name:
            filters['first_name__icontains'] = first_name
        if last_name:
            filters['last_name__icontains'] = last_name

        if distance:
            central_latitude, central_longitude = get_central_coordinates(request)
            clients = Client.objects.all()
            clients = filter_by_distance(clients, central_latitude,
                                         central_longitude, float(distance))
        else:
            clients = Client.objects.filter(**filters)

        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
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
                'from@example.com', [current_client.email], fail_silently=False,
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


def filter_by_distance(queryset, central_latitude,
                       central_longitude, distance):
    filtered_queryset = []
    for client in queryset:
        if client.is_superuser:
            continue
        client_distance = haversine_distance(client.latitude,
                                             client.longitude,
                                             central_latitude,
                                             central_longitude)
        print(client_distance)
        if client_distance <= distance:
            filtered_queryset.append(client)
    return filtered_queryset


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # радиус Земли в километрах

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = R * c
    return distance


def get_central_coordinates(request):
    user = request.user
    central_latitude = user.latitude
    central_longitude = user.longitude
    return central_latitude, central_longitude

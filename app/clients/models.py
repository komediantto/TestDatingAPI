from django.contrib.auth.models import AbstractUser
from django.db import models


class Client(AbstractUser):
    class Sex(models.TextChoices):
        MALE = 'М'
        FEMALE = 'Ж'

    avatar = models.ImageField(verbose_name='Аватар',
                               upload_to='clients/avatars/',
                               null=True,
                               default=None)
    sex = models.CharField(max_length=1, choices=Sex.choices)
    first_name = models.CharField(verbose_name='Имя', max_length=20)
    last_name = models.CharField(verbose_name='Фамилия', max_length=40)
    email = models.EmailField(verbose_name='Почта')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    liked_by = models.ManyToManyField('self', related_name='liked',
                                      through='Match', symmetrical=False)

    def __str__(self):
        return self.username


class Match(models.Model):
    client1 = models.ForeignKey(Client,
                                related_name='client1',
                                on_delete=models.CASCADE)
    client2 = models.ForeignKey(Client,
                                related_name='client2',
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

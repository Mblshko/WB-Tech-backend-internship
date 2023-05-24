from django.db import models
from rest_framework.authtoken.admin import User


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Автор')
    subscriber = models.BooleanField(default=True)
    date_sub = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


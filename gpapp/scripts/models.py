from django.db import models
from django.utils import timezone
from datetime import datetime


class Script(models.Model):
    """
    Модель для хранения скриптов
    """
    name = models.CharField(max_length=255, verbose_name='Название скрипта')
    code = models.TextField(verbose_name='Код скрипта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Скрипт'
        verbose_name_plural = 'Скрипты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

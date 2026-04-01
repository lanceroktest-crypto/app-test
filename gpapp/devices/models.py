from django.db import models
from django.utils import timezone


class Device(models.Model):
    """
    Модель для хранения информации об устройствах
    """
    udid = models.CharField(max_length=255, unique=True, verbose_name='UDID устройства')
    name = models.CharField(max_length=255, verbose_name='Имя устройства')
    status = models.CharField(max_length=50, default='offline', choices=[
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('busy', 'Busy'),
    ], verbose_name='Статус устройства')
    is_active = models.BooleanField(default=True, verbose_name='Активное устройство')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.udid})"


class Account(models.Model):
    """
    Модель для хранения аккаунтов
    """
    email = models.EmailField(unique=True, verbose_name='Email аккаунта')
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name='Пароль')
    is_active = models.BooleanField(default=True, verbose_name='Активный аккаунт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['email']

    def __str__(self):
        return self.email


class DeviceAccount(models.Model):
    """
    Модель связи устройств и аккаунтов
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Аккаунт')
    
    class Meta:
        verbose_name = 'Связь устройства и аккаунта'
        verbose_name_plural = 'Связи устройств и аккаунтов'
        unique_together = ('device', 'account')

    def __str__(self):
        return f"{self.device.name} - {self.account.email}"

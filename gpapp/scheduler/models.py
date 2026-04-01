from django.db import models
from apps.models import AppTestProfile
from devices.models import Device


class Schedule(models.Model):
    """
    Модель для хранения расписания тестирования
    """
    profile = models.ForeignKey(AppTestProfile, on_delete=models.CASCADE, verbose_name='Профиль тестирования')
    start_date = models.DateTimeField(verbose_name='Дата начала тестирования')
    end_date = models.DateTimeField(verbose_name='Дата окончания тестирования')
    is_active = models.BooleanField(default=True, verbose_name='Активное расписание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['-created_at']

    def __str__(self):
        return f"Расписание для {self.profile.name}"


class DeviceSchedule(models.Model):
    """
    Модель для привязки устройств к расписанию
    """
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='Расписание')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата назначения')
    
    class Meta:
        verbose_name = 'Назначение устройства'
        verbose_name_plural = 'Назначения устройств'
        unique_together = ('schedule', 'device')

    def __str__(self):
        return f"{self.device.name} - {self.schedule.profile.name}"

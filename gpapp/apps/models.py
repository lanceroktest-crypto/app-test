from django.db import models
from django.utils import timezone
from devices.models import Account
from scripts.models import Script


class AppTestProfile(models.Model):
    """
    Модель для хранения профилей тестирования приложений
    """
    name = models.CharField(max_length=255, verbose_name='Название профиля')
    package_name = models.CharField(max_length=255, verbose_name='Имя пакета приложения')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    
    # Скрипты для каждого этапа
    install_script = models.TextField(verbose_name='Скрипт установки', blank=True)
    test_script = models.TextField(verbose_name='Скрипт теста', blank=True)
    uninstall_script = models.TextField(verbose_name='Скрипт удаления', blank=True)
    
    # Выбор из готовых скриптов
    install_script_template = models.ForeignKey(
        Script, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='install_profiles',
        verbose_name='Шаблон скрипта установки'
    )
    test_script_template = models.ForeignKey(
        Script, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='test_profiles',
        verbose_name='Шаблон скрипта теста'
    )
    uninstall_script_template = models.ForeignKey(
        Script, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='uninstall_profiles',
        verbose_name='Шаблон скрипта удаления'
    )
    
    # Аккаунт для тестирования
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Аккаунт для тестирования')
    
    is_active = models.BooleanField(default=True, verbose_name='Активный профиль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль тестирования приложения'
        verbose_name_plural = 'Профили тестирования приложений'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.package_name})"


class ScheduledTask(models.Model):
    """
    Модель для запланированных задач тестирования
    """
    TASK_TYPE_CHOICES = [
        ('install', 'Установка'),
        ('test', 'Тестирование'),
        ('uninstall', 'Удаление'),
    ]
    
    profile = models.ForeignKey(AppTestProfile, on_delete=models.CASCADE, verbose_name='Профиль тестирования')
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, verbose_name='Тип задачи')
    scheduled_time = models.DateTimeField(verbose_name='Время выполнения')
    executed = models.BooleanField(default=False, verbose_name='Выполнено')
    executed_at = models.DateTimeField(null=True, blank=True, verbose_name='Время выполнения')
    result = models.TextField(blank=True, null=True, verbose_name='Результат выполнения')
    
    class Meta:
        verbose_name = 'Запланированная задача'
        verbose_name_plural = 'Запланированные задачи'
        ordering = ['scheduled_time']

    def __str__(self):
        return f"{self.profile.name} - {self.get_task_type_display()} - {self.scheduled_time}"


class DeviceTestSession(models.Model):
    """
    Модель для сессии тестирования на устройстве
    """
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, verbose_name='Устройство')
    profile = models.ForeignKey(AppTestProfile, on_delete=models.CASCADE, verbose_name='Профиль тестирования')
    start_date = models.DateTimeField(verbose_name='Дата начала тестирования')
    end_date = models.DateTimeField(verbose_name='Дата окончания тестирования')
    current_task = models.CharField(max_length=20, choices=ScheduledTask.TASK_TYPE_CHOICES, verbose_name='Текущая задача')
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Ожидает'),
        ('running', 'Выполняется'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
    ], verbose_name='Статус сессии')
    
    class Meta:
        verbose_name = 'Сессия тестирования'
        verbose_name_plural = 'Сессии тестирования'
        unique_together = ('device', 'profile')

    def __str__(self):
        return f"{self.device.name} - {self.profile.name}"

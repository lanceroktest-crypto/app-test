from celery import shared_task
import subprocess
import os
from django.utils import timezone
from .models import Script
from apps.models import ScheduledTask, AppTestProfile
from devices.models import Device
import logging

logger = logging.getLogger(__name__)


@shared_task
def execute_script(script_id, device_udid, profile_id, task_type):
    """
    Выполнение скрипта на устройстве
    """
    try:
        script = Script.objects.get(id=script_id)
        device = Device.objects.get(udid=device_udid)
        profile = AppTestProfile.objects.get(id=profile_id)
        
        # Обновляем статус устройства
        device.status = 'busy'
        device.save()
        
        # Подготовка контекста для выполнения скрипта
        local_vars = {
            'androidid': device_udid,
            'package_name': profile.package_name,
            'gmail': profile.account.email if profile.account else '',
            'appium_port': '4723',  # Порт по умолчанию, можно настроить динамически
        }
        
        # Добавляем переменные в скрипт
        script_code = script.code
        for var_name, var_value in local_vars.items():
            script_code = script_code.replace(f'{{{{ {var_name} }}}}', str(var_value))
        
        # Выполняем скрипт
        exec(script_code, {"__builtins__": __builtins__}, local_vars)
        
        # Обновляем статус задачи
        scheduled_task = ScheduledTask.objects.filter(
            profile=profile, 
            task_type=task_type,
            scheduled_time__lte=timezone.now()
        ).order_by('-scheduled_time').first()
        
        if scheduled_task:
            scheduled_task.executed = True
            scheduled_task.executed_at = timezone.now()
            scheduled_task.result = "Успешно выполнено"
            scheduled_task.save()
        
        # Обновляем статус устройства
        device.status = 'online'
        device.save()
        
        logger.info(f"Скрипт {script.name} успешно выполнен на устройстве {device.name}")
        return f"Скрипт {script.name} успешно выполнен на устройстве {device.name}"
        
    except Exception as e:
        logger.error(f"Ошибка при выполнении скрипта: {str(e)}")
        
        # Обновляем статус устройства
        try:
            device = Device.objects.get(udid=device_udid)
            device.status = 'online'
            device.save()
        except:
            pass
        
        # Обновляем статус задачи
        try:
            scheduled_task = ScheduledTask.objects.filter(
                profile=profile, 
                task_type=task_type,
                scheduled_time__lte=timezone.now()
            ).order_by('-scheduled_time').first()
            
            if scheduled_task:
                scheduled_task.executed = False
                scheduled_task.executed_at = timezone.now()
                scheduled_task.result = f"Ошибка: {str(e)}"
                scheduled_task.save()
        except:
            pass
        
        return f"Ошибка при выполнении скрипта: {str(e)}"
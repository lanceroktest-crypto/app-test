from celery import shared_task
from django.utils import timezone
from datetime import timedelta, datetime
from apps.models import AppTestProfile, ScheduledTask, DeviceTestSession
from devices.models import Device, DeviceAccount
from scripts.models import Script
from scripts.tasks import execute_script
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_schedule_for_profile(profile_id):
    """
    Генерация расписания для профиля тестирования
    """
    try:
        profile = AppTestProfile.objects.get(id=profile_id)
        
        # Удаляем старые задачи для этого профиля
        ScheduledTask.objects.filter(profile=profile).delete()
        
        # Определяем даты начала и окончания тестирования
        now = timezone.now()
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)  # Начало сегодняшнего дня
        end_date = start_date + timedelta(days=15)  # 15 дней тестирования
        
        # Создаем задачу установки (выполняется 1 раз)
        install_time = start_date.replace(hour=22, minute=0)  # Установка в 22:00
        install_task = ScheduledTask.objects.create(
            profile=profile,
            task_type='install',
            scheduled_time=install_time
        )
        
        # Создаем задачи тестирования (ежедневно с 00:00 до 22:00 в течение 15 дней)
        for day in range(15):
            test_day = start_date + timedelta(days=day)
            # Тестирование с 00:00 до 22:00 (всего 22 часа)
            for hour in range(22):  # с 00:00 до 21:00
                test_time = test_day.replace(hour=hour, minute=0)
                ScheduledTask.objects.create(
                    profile=profile,
                    task_type='test',
                    scheduled_time=test_time
                )
        
        # Создаем задачу удаления (после 15 дней тестирования)
        uninstall_time = end_date.replace(hour=22, minute=0)  # Удаление в 22:00
        uninstall_task = ScheduledTask.objects.create(
            profile=profile,
            task_type='uninstall',
            scheduled_time=uninstall_time
        )
        
        logger.info(f"Расписание сгенерировано для профиля {profile.name}")
        return f"Расписание сгенерировано для профиля {profile.name}"
        
    except Exception as e:
        logger.error(f"Ошибка при генерации расписания: {str(e)}")
        return f"Ошибка при генерации расписания: {str(e)}"


@shared_task
def check_and_execute_scheduled_tasks():
    """
    Проверка и выполнение запланированных задач
    """
    try:
        now = timezone.now()
        
        # Получаем все задачи, которые должны быть выполнены в данный момент и еще не выполнены
        tasks_to_execute = ScheduledTask.objects.filter(
            scheduled_time__lte=now,
            executed=False
        )
        
        executed_tasks = []
        
        for task in tasks_to_execute:
            # Находим доступные устройства для выполнения задачи
            # Сначала получаем устройства, связанные с аккаунтами, которые связаны с профилем
            if task.profile.account:
                device_accounts = DeviceAccount.objects.filter(account=task.profile.account)
                available_devices = Device.objects.filter(
                    deviceaccount__in=device_accounts,
                    is_active=True,
                    status='online'
                ).exclude(devicetestsessions__isnull=False)  # Исключаем устройства, уже занятые в сессиях
            else:
                # Если аккаунт не назначен, используем любые доступные устройства
                available_devices = Device.objects.filter(
                    is_active=True,
                    status='online'
                ).exclude(devicetestsessions__isnull=False)
            
            if available_devices.exists():
                device = available_devices.first()
                
                # Определяем скрипт для выполнения задачи
                script = None
                if task.task_type == 'install':
                    script = task.profile.install_script_template
                elif task.task_type == 'test':
                    script = task.profile.test_script_template
                elif task.task_type == 'uninstall':
                    script = task.profile.uninstall_script_template
                
                if script:
                    # Выполняем задачу
                    execute_script.delay(
                        script_id=script.id,
                        device_udid=device.udid,
                        profile_id=task.profile.id,
                        task_type=task.task_type
                    )
                    
                    # Обновляем статус задачи
                    task.executed = True
                    task.executed_at = now
                    task.result = "Задача отправлена на выполнение"
                    task.save()
                    
                    executed_tasks.append(f"{task.profile.name} - {task.task_type} на {device.name}")
                else:
                    task.executed = False
                    task.executed_at = now
                    task.result = f"Нет скрипта для задачи типа {task.task_type}"
                    task.save()
            else:
                # Нет доступных устройств
                task.executed = False
                task.executed_at = now
                task.result = "Нет доступных устройств для выполнения задачи"
                task.save()
        
        logger.info(f"Выполнено задач: {len(executed_tasks)}")
        return f"Выполнено задач: {len(executed_tasks)}"
        
    except Exception as e:
        logger.error(f"Ошибка при проверке и выполнении задач: {str(e)}")
        return f"Ошибка при проверке и выполнении задач: {str(e)}"


@shared_task
def create_test_sessions():
    """
    Создание сессий тестирования для активных профилей
    """
    try:
        # Находим активные профили, для которых еще не созданы сессии
        active_profiles = AppTestProfile.objects.filter(is_active=True)
        
        for profile in active_profiles:
            # Проверяем, есть ли уже активная сессия для этого профиля
            if not DeviceTestSession.objects.filter(profile=profile).exists():
                # Находим доступные устройства
                if profile.account:
                    device_accounts = DeviceAccount.objects.filter(account=profile.account)
                    available_devices = Device.objects.filter(
                        deviceaccount__in=device_accounts,
                        is_active=True,
                        status='online'
                    )
                else:
                    available_devices = Device.objects.filter(
                        is_active=True,
                        status='online'
                    )
                
                # Создаем сессии для доступных устройств
                for device in available_devices:
                    # Проверяем, занято ли устройство в другой сессии
                    if not DeviceTestSession.objects.filter(device=device).exists():
                        start_date = timezone.now()
                        end_date = start_date + timedelta(days=15)
                        
                        DeviceTestSession.objects.create(
                            device=device,
                            profile=profile,
                            start_date=start_date,
                            end_date=end_date,
                            current_task='install',
                            status='pending'
                        )
        
        logger.info("Сессии тестирования созданы")
        return "Сессии тестирования созданы"
        
    except Exception as e:
        logger.error(f"Ошибка при создании сессий тестирования: {str(e)}")
        return f"Ошибка при создании сессий тестирования: {str(e)}"
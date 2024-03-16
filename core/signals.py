import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AnalystTask, Sample, AgronomistTask, LabManagerTask, ChangeLog


@receiver(post_save, sender=AnalystTask)
def update_sample_status_analyst(sender, instance, created, **kwargs):
    if created:
        instance.sample.stage = Sample.ANALYST_TASK
        instance.sample.save()

@receiver(post_save, sender=AgronomistTask)
def update_sample_status_agronomist(sender, instance, created, **kwargs):
    if created:
        instance.sample.stage = Sample.AGRONOMIST_TASK
        instance.sample.save()

@receiver(post_save, sender=LabManagerTask)
def update_sample_status_lab_manager(sender, instance, created, **kwargs):
    if created:
        instance.sample.stage = Sample.LAB_MANAGER_TASK
        instance.sample.save()


logger = logging.getLogger(__name__)

@receiver(post_save, sender=[Sample, AnalystTask, AgronomistTask, LabManagerTask])
def log_model_changes(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    user = kwargs.get('request').user if 'request' in kwargs else None  # Fetching user from kwargs if available
    model_name = sender.__name__
    object_id = instance.pk
    details = f'{action.capitalize()} {model_name} instance: {object_id}'
    
    log_entry = ChangeLog(user=user, model_name=model_name, object_id=object_id, action=action, details=details)
    log_entry.save()

@receiver(post_delete, sender=[Sample, AnalystTask, AgronomistTask, LabManagerTask])
def log_model_deletions(sender, instance, **kwargs):
    user = kwargs.get('request').user if 'request' in kwargs else None  # Fetching user from kwargs if available
    model_name = sender.__name__
    object_id = instance.pk
    details = f'Deleted {model_name} instance: {object_id}'
    
    log_entry = ChangeLog(user=user, model_name=model_name, object_id=object_id, action='delete', details=details)
    log_entry.save()

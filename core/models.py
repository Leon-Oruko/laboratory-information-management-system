from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,AbstractUser
from django.conf import settings
from django.utils import timezone
from .manager import CustomUserManager


class CustomUsers(AbstractUser):
    ADMIN = 'Admin'
    ANALYST = 'Analyst'
    AGRONOMIST = 'Agronomist'
    LAB_MANAGER = 'Lab Manager'

    POSTS = [
        (ADMIN, 'Admin'),
        (ANALYST, 'Analyst'),
        (AGRONOMIST, 'Agronomist'),
        (LAB_MANAGER, 'Lab Manager')
    ]

    email = models.EmailField(unique=True)
    post = models.CharField(max_length=20, choices=POSTS, default=ANALYST)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150,unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username","first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        permissions = [
            ('admin', 'Can access admin features'),
            ('analyst', 'Can access analyst features'),
            ('agronomist', 'Can access agronomist features'),
            ('labmanager', 'Can access lab manager features'),
        ]

    # Add unique related_name arguments for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',
        related_query_name='custom_user_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user_permission',
    )

    def __str__(self):
        return self.email
# class User(AbstractUser):
#     ADMIN = 'Admin'
#     ANALYST = 'Analyst'
#     AGRONOMIST = 'Agronomist'
#     LAB_MANAGER = 'Lab Manager'

#     POSTS = [
#         (ADMIN, 'Admin'),
#         (ANALYST, 'Analyst'),
#         (AGRONOMIST, 'Agronomist'),
#         (LAB_MANAGER, 'Lab Manager')
#     ]
#     post = models.CharField(max_length=20, choices=POSTS)    

#     # Add unique related names for the groups and user_permissions fields
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name='groups',
#         blank=True,
#         related_name='custom_user_groups',
#         related_query_name='custom_user_group',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name='user permissions',
#         blank=True,
#         related_name='custom_user_permissions',
#         related_query_name='custom_user_permission',
#     )

#     class Meta:
#         swappable = 'AUTH_USER_MODEL'

#     def __str__(self): 
#         return f'{self.first_name}~{self.post}'

class Industry(models.Model):
    Industry_id=models.IntegerField(auto_created=True)
    Industry_type=models.CharField(max_length=150)
    class Meta:
        ordering = ['Industry_type']
    def __str__(self):
        return self.Industry_type
class Clients(models.Model):
    name=models.CharField(max_length=150)
    contact=models.CharField(max_length=150)
    email=models.EmailField()
    industry=models.ForeignKey(Industry,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
class Sample(models.Model):
    REGISTRATION = 'registration'
    ANALYST_TASK = 'analysis'
    AGRONOMIST_TASK = 'recommendation'
    LAB_MANAGER_TASK = 'processing'
    COMPLETE='complete'
    STAGE_CHOICES = [
        (REGISTRATION, 'Registration stage'),
        (ANALYST_TASK, 'Analysis stage'),
        (AGRONOMIST_TASK, 'Recommendation stage'),
        (LAB_MANAGER_TASK, 'Processing stage'),
        (COMPLETE,'Complete')
    ]

    CHEMICAL='Chemical'
    MICROBIO='Microbiology'
    FULL='Full'
    TEST_CHOICES=[
        (CHEMICAL,'Chemical Analysis'),
        (MICROBIO,'Microbiology'),
        (FULL,'Full analysis')
    ]

    sample_id = models.CharField(max_length=20, unique=True)
    sample_name = models.CharField(max_length=100)
    test_id = models.CharField(max_length=100,choices=TEST_CHOICES,default=CHEMICAL)
    customer = models.ForeignKey(Clients,on_delete=models.SET_NULL,null=True)
    date_of_registration = models.DateField(default=timezone.now)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default=REGISTRATION)
    
    def __str__(self):
        return f'{self.sample_id}~{self.test_id}'

class SampleRegistration(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    registration_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.sample.sample_id}~{self.registration_date}'

class AnalystTask(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Incomplete', 'Incomplete'), ('Complete', 'Complete')])
    analysis = models.TextField(blank=True, null=True)
    analysis_date = models.DateField(blank=True, null=True)
    analyzed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyst_tasks')
    picked=models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.sample.sample_id}~{self.analyzed_by}'

class AgronomistTask(models.Model):
    sample = models.OneToOneField(
        Sample, 
        on_delete=models.CASCADE, 
        limit_choices_to={'analysttask__status': 'Complete'}, 
        related_name='agronomist_task'
    )
    interpretation = models.TextField()
    recommendation = models.TextField()
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agronomist_tasks')

    def __str__(self):
        return f'{self.sample.sample_id}~{self.reviewed_by}'

class LabManagerTask(models.Model):
    sample = models.OneToOneField(
        Sample, 
        on_delete=models.CASCADE, 
        limit_choices_to={'agronomist_task__isnull': False}, 
        related_name='lab_manager_task'
    )
    status = models.CharField(max_length=20, choices=[('Picked', 'Picked'), ('Invoiced', 'Invoiced')])
    invoice = models.FileField(upload_to='invoices/', blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_manager_tasks')


    def __str__(self):
        return f'{self.sample.sample_id}~{self.processed_by}'
    

class ChangeLog(models.Model):
    class Meta:
        managed = False  # This prevents Django from creating tables for this model
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUsers, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    action = models.CharField(max_length=20)  # 'create', 'update', 'delete'
    details = models.TextField()

    def __str__(self):
        return f'{self.timestamp}~{self.user}'


class Microbio(models.Model):
    sample=models.OneToOneField(Sample,on_delete=models.CASCADE,null=False)
    # other records
    analysis=models.TextField(default='ANALYISIS')
    recommendation=models.TextField(default='RECOMMENDATION')
    def __str__(self):
        return self.sample.sample_id
class Full(models.Model):
    sample=models.OneToOneField(Sample,on_delete=models.CASCADE,null=False)
    # other records
    analysis=models.TextField(default='ANALYISIS')
    recommendation=models.TextField(default='RECOMMENDATION')
    def __str__(self):
        return self.sample.sample_id
class Chemical(models.Model):
    sample=models.OneToOneField(Sample,on_delete=models.CASCADE,null=False)
    recommendation=models.TextField(default='RECOMMENDATION')
    # other records`
    analysis=models.TextField(default='ANALYISIS')
    def __str__(self):
        return self.sample.sample_id
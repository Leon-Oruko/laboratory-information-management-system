from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from core.models import CustomUser
def create_custom_permissions():
    # Define the list of permissions
    permissions = [
        ('admin', 'Can access admin features'),
        ('analyst', 'Can access analyst features'),
        ('agronomist', 'Can access agronomist features'),
        ('labmanager', 'Can access lab manager features'),
    ]

    # Get the content type for the CustomUser model
    content_type = ContentType.objects.get_for_model(CustomUser)

    # Create permissions for each role
    for codename, name in permissions:
        permission, _ = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type,
        )

        # Create a group for the role and assign the permission to it
        group, _ = Group.objects.get_or_create(name=codename)
        group.permissions.add(permission)

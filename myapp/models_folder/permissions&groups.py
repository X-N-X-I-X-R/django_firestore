from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_migrate)
def add_users_to_groups(sender, **kwargs):
  user_group, _ = Group.objects.get_or_create(name='user')
  admin_group, _ = Group.objects.get_or_create(name='admin')
  staff_group, _ = Group.objects.get_or_create(name='staff')

  # Assign permissions to each group:

  # Admin Group (Grant all permissions)
  admin_group.permissions.set(Permission.objects.all())

  # Staff Group (Grant user and content management permissions)
  staff_group.permissions.set(Permission.objects.filter(
    content_type__app_label='myapp',
    content_type__model__in=['post', 'like', 'comment', 'follow', 'user', 'group', 'content type', 'response'],
    codename__in=['add', 'change', 'delete', 'view']
  ))

  # User Group (Grant permissions for their own content)
  user_group.permissions.set(Permission.objects.filter(
    content_type__app_label='myapp',
    content_type__model__in=['post', 'like', 'comment', 'follow'],
    codename__in=['add', 'change', 'delete', 'view']
  ))

  try:
    user = UserProfile.objects.get(username='username')
    user.groups.add(user_group)
  except UserProfile.DoesNotExist:
    print("User 'username' does not exist")

  try:
    admin = UserProfile.objects.get(username='admin')
    admin.groups.add(admin_group)
  except UserProfile.DoesNotExist:
    print("User 'admin' does not exist")

  try:
    staff = UserProfile.objects.get(username='staff')
    staff.groups.add(staff_group)
  except UserProfile.DoesNotExist:
    print("User 'staff' does not exist")
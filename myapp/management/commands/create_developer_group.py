from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from myapp.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates the developer group with appropriate permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force execution even in production',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username of the superuser running the command',
            required=True
        )

    def get_model_permissions(self, model, actions=None):
        """Get permissions for a specific model"""
        if actions is None:
            actions = ['view', 'change']  # Default actions
            
        content_type = ContentType.objects.get_for_model(model)
        permissions = []
        
        for action in actions:
            perm_codename = f'{action}_{model._meta.model_name}'
            try:
                perm = Permission.objects.get(content_type=content_type, codename=perm_codename)
                permissions.append(perm)
                self.stdout.write(f'Added {action} permission for {model._meta.model_name}')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'Permission {perm_codename} does not exist for {model._meta.model_name}'
                ))
                
        return permissions

    def handle(self, *args, **options):
        # Security checks
        if not options['force'] and not settings.DEBUG:
            raise CommandError(
                'This command can only be run in DEBUG mode or with --force flag. '
                'Running this command in production without --force is prohibited.'
            )

        # Check if running user is superuser
        if not self.stdout.isatty():
            raise CommandError('This command can only be run from a terminal')

        # Get the running user
        try:
            running_user = User.objects.get(username=options['username'])
            if not running_user.is_superuser:
                raise CommandError(f'User {options["username"]} is not a superuser')
        except User.DoesNotExist:
            raise CommandError(f'User {options["username"]} not found in database')

        # Get the superuser
        try:
            superuser = User.objects.get(username='n@n.com')
            if not superuser.is_superuser:
                raise CommandError('User n@n.com is not a superuser')
        except User.DoesNotExist:
            raise CommandError('Superuser n@n.com not found in database')

        # Create developer group if it doesn't exist
        developer_group, created = Group.objects.get_or_create(name='developer')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created developer group'))
        else:
            self.stdout.write('Developer group already exists')
            
        # Get all models from myapp
        myapp_models = apps.get_app_config('myapp').get_models()
        
        # Collect all permissions
        developer_permissions = []
        
        # Add permissions for each model in myapp
        for model in myapp_models:
            # For User model, only allow view and change
            if model == User:
                developer_permissions.extend(self.get_model_permissions(model, ['view', 'change']))
            # For other models, allow view, add, change (but not delete)
            else:
                developer_permissions.extend(self.get_model_permissions(model, ['view', 'add', 'change']))
        
        # Set permissions for developer group
        developer_group.permissions.set(developer_permissions)
        
        self.stdout.write(self.style.SUCCESS('Successfully set developer group permissions'))
        
        # Ensure superuser is not in developer group
        if superuser.groups.filter(name='developer').exists():
            superuser.groups.remove(developer_group)
            self.stdout.write(self.style.SUCCESS('Removed superuser from developer group')) 
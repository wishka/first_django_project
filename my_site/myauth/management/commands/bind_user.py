from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Получаем пользователя
        user = User.objects.get(pk=2)
        # Создадим группу, если ее не существует
        group, created = Group.objects.get_or_create(
            name='profile-manager'
        )
        permission_profile = Permission.objects.get(
            codename="view_profile"
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry"
        )
        # Свяжем permissions с группой profile-manager
        group.permissions.add(permission_profile)
        # Так как связь Many to Many добавление выполняется через add()
        user.groups.add(group)
        # Также можно связать пользователя напрямую с Permissions
        user.user_permissions.add(permission_logentry)
        group.save()
        user.save()
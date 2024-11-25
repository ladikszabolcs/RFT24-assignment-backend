from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = "Create an API User"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help="Username of the API user")
        parser.add_argument('password', type=str, help="Password for the API user")
        parser.add_argument('email', type=str, help="Email for the API user")
        parser.add_argument('role', type=str, choices=['student', 'teacher', 'admin'], help="Role for the API user")

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        email = kwargs['email']
        role = kwargs['role']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"User '{username}' already exists!"))
        else:
            user = User.objects.create_user(username=username, password=password, email=email, role=role)
            self.stdout.write(self.style.SUCCESS(f"Successfully created user '{username}' with role '{role}'."))
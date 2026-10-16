from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = "Cria um administrador de demonstração se ainda não existir."

    def handle(self, *args, **options):
        email = "a@a.com"
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Usuário {email} já existe; nenhuma alteração feita."))
            return
        User.objects.create_superuser(
            username="admin",
            email=email,
            password="teste.123",
            first_name="Administrador",
        )
        self.stdout.write(self.style.SUCCESS("Administrador de demonstração criado: a@a.com"))

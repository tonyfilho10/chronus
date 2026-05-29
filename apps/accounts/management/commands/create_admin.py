import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Cria o usuario administrador CSHUB se nao existir"

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.environ.get("ADMIN_EMAIL", "lourival.cshub@gmail.com")
        password = os.environ.get("ADMIN_PASSWORD", "@Oten2026en")
        username = "lourivalpinheiro"

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"Admin ja existe: {email}")
            return

        try:
            from allauth.account.models import EmailAddress
            u = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                is_active=True,
                plan="pro",
                monthly_quota=9999,
            )
            EmailAddress.objects.get_or_create(
                user=u, email=email,
                defaults={"primary": True, "verified": True},
            )
            EmailAddress.objects.filter(user=u).update(verified=True, primary=True)
            self.stdout.write(f"Admin criado: {email}")
        except Exception as e:
            self.stderr.write(f"Erro ao criar admin: {e}")

        # Garante que o Site ID=1 existe (necessario para allauth)
        try:
            from django.contrib.sites.models import Site
            site, _ = Site.objects.get_or_create(
                id=1,
                defaults={"domain": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"), "name": "CHRONUS CSHUB"},
            )
            if site.domain == "example.com":
                site.domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "chronus.railway.app")
                site.name = "CHRONUS CSHUB"
                site.save()
        except Exception as e:
            self.stderr.write(f"Erro ao configurar Site: {e}")

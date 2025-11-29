from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from app_site.models import Colaboradores

@receiver(post_save, sender=CustomUser)
def criar_colaborador_automatico(sender, instance, created, **kwargs):
    if created:
        Colaboradores.objects.create(
            user=instance,
            email=instance.email,
            cpf=instance.cpf,
            nome_colaborador=instance.first_name or ""
        )

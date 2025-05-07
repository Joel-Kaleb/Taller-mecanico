from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Reparacion
from django.core.mail import EmailMessage

@receiver(pre_save, sender=Reparacion)
def notificar_cambio_estado(sender, instance, **kwargs):
    if not instance.pk:
        return  # No hay objeto previo, se está creando

    try:
        instancia_anterior = Reparacion.objects.get(pk=instance.pk)
    except Reparacion.DoesNotExist:
        return

    # Comparar el estado anterior con el nuevo
    if instancia_anterior.estado != instance.estado:
        cliente = instance.vehiculo.cliente
        correo = cliente.correo_electronico

        if correo:
            asunto = "Actualización del estado de la reparación"
            mensaje = f"""
            Hola {cliente.nombre_cliente},

            El estado de la reparación de tu vehículo con matrícula {instance.vehiculo.matricula} ha cambiado de:
            '{instancia_anterior.estado}' a '{instance.estado}'.

            Gracias por confiar en nuestro taller.
            """
            email = EmailMessage(asunto, mensaje, to=[correo])
            email.send()

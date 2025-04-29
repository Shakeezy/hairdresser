from .models import TimeSlot
from datetime import date, time, timedelta
def generar_slots_por_defecto(fecha):
    """ Genera los tramos horarios automáticamente según si es sábado o no. """
    horarios_base = [
        (10, 0), (10, 30), (11, 0), (11, 30),
        (12, 0), (12, 30)
    ]

    # Si NO es sábado, agregamos los horarios de la tarde
    if fecha.weekday() != 5:
        horarios_base.extend([
            (17, 0), (17, 30), (18, 0), (18, 30),
            (19, 0), (19, 30), (20, 0)
        ])

    # Crear los slots si no existen ya
    for hora, minuto in horarios_base:
        TimeSlot.objects.get_or_create(
            date=fecha,
            time=time(hora, minuto)
        )
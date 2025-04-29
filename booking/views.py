from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.contrib import messages
from .models import CloseDay, TimeSlot, Appointment, Service
from .utils import generar_slots_por_defecto
from .validations import validation_form
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _


def home(request):
    return render(request, 'home.html', {})

def citaFecha(request):
    return render(request, 'cita_fecha.html', {})

def citaFormulario(request):
    if request.method == 'POST':
        try:
            date_str = request.POST.get('date')
            date_selected = datetime.strptime(date_str, "%Y-%m-%d").date()
            close_days = CloseDay.objects.all().values_list('date', flat=True)
        except:
            message_format = _('Invalid date format')
            messages.error(request, message_format)
            return redirect('cita_fecha')
        
        if date_selected < date.today():
            message_pass = _('The appointment date has expired. Please take another one')
            messages.error(request, message_pass)
            return redirect('cita_fecha')
        
        elif date_selected > date.today() + timedelta(days=60): 
            message_format = _('Appointments cannot be scheduled so far in advance. For more information, please call the following number: 4353456546')
            messages.error(request, message_format)
            return redirect('cita_fecha')
        
        elif date_selected in close_days:
            date_motive = CloseDay.objects.get(date=date_selected)
            motive = date_motive.motive
            message_close = _('Close for')
            messages.error(request, f'{message_close} {motive}')
            return redirect('cita_fecha')
        
        elif date_selected.weekday() == 6:
            message_close = _('Close for sunday')
            messages.error(request, message_close)
            return redirect('cita_fecha')
        
        else:
            # Comprobar si hay timeslots para esa fecha
            timeslots = TimeSlot.objects.filter(date=date_selected)

            # Si no hay slots, generamos los predeterminados
            if not timeslots.exists():
                generar_slots_por_defecto(date_selected)
            
            now = timezone.localtime().replace(second=0, microsecond=0)

            # Filtrar solo los horarios disponibles
            if date_selected == timezone.now().date():
                timeslots_disponibles = TimeSlot.objects.filter(date=date_selected, is_booked=False, time__gte=now.time()).order_by('time')
            else:
                timeslots_disponibles = TimeSlot.objects.filter(date=date_selected, is_booked=False).order_by('time')

            # Obtener servicios
            services = Service.objects.all()

            # Contexto para renderizar
            context = {
                'date': date_selected,
                'services': services,
                'timeslotsavaible': timeslots_disponibles,
                'mensaje': "Not appointments avaible for this date." if not timeslots_disponibles.exists() else ""
                }
            return render(request, 'cita_formulario.html', context)
    else:
        return redirect('cita_fecha')

def confirmarCita(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        slot_id = request.POST.get('timeslot')
        client_name = request.POST.get('client_name')
        client_last_name = request.POST.get('client_last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        validation_message = validation_form(phone_number, email)

        try:
            service = Service.objects.get(id=service_id)
        except:
            validation_message += '- Invalid service selected\n'

        try:
            slot = TimeSlot.objects.get(id=slot_id)
        except:
            validation_message += '- Invalid time slot selected\n'
        
        if validation_message != '':
            messages.error(request, validation_message)
            return redirect('cita_fecha')

        appointment = Appointment(
            service=service,
            slot=slot,
            client_name=client_name,
            client_last_name=client_last_name,
            phone_number=phone_number,
            email=email,
        )

        appointment.save()

        slot.is_booked = True
        slot.save()

        cancel_url= reverse('cancel_appointment', kwargs={'cancel_id': appointment.cancel_token})
        full_cancel_url = f'{request.scheme}://{request.get_host()}{cancel_url}'

        email_body = (   
            '--Español--\n'
            f'Cita confirmada para: {appointment.slot.date}\n'
            f'Hora: {appointment.slot.time}\n'
            f'Servicio: {appointment.service}\n'
            f'Si desea cancelar la cita vaya al link al final de este mensaje\n\n'
            '--English--\n'
            f'Appointment confirmed to: {appointment.slot.date}\n'
            f'Hour: {appointment.slot.time}\n'
            f'Service: {appointment.service}\n'
            f'If you wish to cancel your appointment, please go to the link at the end of this message.\n\n\n'
            f'CANCEL LINK: \n\n\n{full_cancel_url}'
        )
        email_message = EmailMessage(
            F'BARBERSHOP - Cita - Appointment',
            email_body,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email_message.fail_silently = True
        email_message.send()

        context = {
            'appointment' : appointment
        }

        return render(request, 'cita_confirmada.html', context)
    else:
        return redirect('cita_fecha')

def cancelAppointment(request, cancel_id):
    try:
        appointment_cancel_id = Appointment.objects.get(cancel_token=cancel_id)
    except:
            message_cancel_id = _('Invalid cancel id')
            messages.error(request, message_cancel_id)
            return redirect('cita_fecha')
    
    if request.method == 'POST':
        slot = appointment_cancel_id.slot
        slot.is_booked = False
        slot.save()
        appointment_cancel_id.delete()
        message_cancel = _('Appointment canceled succesfully')
        messages.success(request, message_cancel)
        return redirect('cita_fecha')
    return render(request, 'cancel.html', {'cancel_id': cancel_id})


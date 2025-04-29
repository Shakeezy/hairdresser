from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fecha/', views.citaFecha, name='cita_fecha'),
    path('cita_formulario/', views.citaFormulario, name='cita_formulario'),
    path('cita_confirmada', views.confirmarCita, name='cita_confirmada'),
    path('cancel_appointment/<str:cancel_id>/', views.cancelAppointment, name='cancel_appointment'),
]
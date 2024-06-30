from django.urls import path

from measurement.views import SensorsView, SensorView, MeasurementCreateView

urlpatterns = [
    path('sensors/', SensorsView.as_view(), name='create_sensor'),
    path('sensors/<int:pk>/', SensorView.as_view(), name='update_sensor'),
    path('measurements/', MeasurementCreateView.as_view(), name='create_measurement'),
]

# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer

def Image(request):
    template = 'photo.html'
    return render(request, template)

class SensorsView(ListAPIView, CreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request, *args, **kwargs):
        request.data['name'] = "Xiaomi"
        request.data['description'] = "Датчик в ванной"
        return self.create(request, *args, **kwargs)


class SensorView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def patch(self, request, *args, **kwargs):
        request.data['name'] = "ESP32"
        request.data['description'] = "Датчик перенесен за шкаф"
        return self.update(request, *args, **kwargs)


class MeasureCreate(ListAPIView, CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request, *args, **kwargs):
        request.data['sensor_id'] = 1
        request.data['temp'] = 32.7
        return self.create(request, *args, **kwargs)

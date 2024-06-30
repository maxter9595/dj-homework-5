from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer


def check_is_valid(serializer, good_status, bad_status):
    if serializer.is_valid():
        serializer.save()

        return Response(
            data=serializer.data,
            status=good_status
        )

    return Response(
        data=serializer.errors,
        status=bad_status
    )


class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        sensors_serializer = SensorSerializer(
            data=request.data
        )

        return check_is_valid(
            serializer=sensors_serializer,
            good_status=status.HTTP_201_CREATED,
            bad_status=status.HTTP_400_BAD_REQUEST
        )


class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def patch(self, request, *args, **kwargs):
        sensor_serializer = SensorSerializer(
            instance=self.get_object(),
            data=request.data,
            partial=True
        )

        return check_is_valid(
            serializer=sensor_serializer,
            good_status=status.HTTP_200_OK,
            bad_status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, *args, **kwargs):
        sensor_data = SensorSerializer(
            instance=self.get_object()
        ).data

        measurement_data = MeasurementSerializer(
            instance=self.get_object().measurements.all(),
            many=True,
        ).data

        for measurement in measurement_data:
            measurement.pop('sensor', None)
            measurement.pop('id', None)

            if not measurement.get('image'):
                measurement.pop('image', None)

        sensor_data['measurements'] = measurement_data

        return Response(
            data=sensor_data,
            status=status.HTTP_200_OK
        )


class MeasurementCreateView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

import re

from rest_framework import serializers

from .models import Asteroid, Device, Observatory, Sighting
from .services import MatrixService


class ObservatorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Observatory
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class SightingSerializer(serializers.ModelSerializer):
    fmt_matrix = serializers.SerializerMethodField(read_only=True)
    is_matrix_complete = serializers.ReadOnlyField()
    device = DeviceSerializer(read_only=True)
    observatory = ObservatorySerializer(read_only=True)

    class Meta:
        model = Sighting
        fields = '__all__'

    def get_fmt_matrix(self, obj):
        matrix = MatrixService(vectorized_matrix=obj.matrix, n_cols=obj.device.cols_rows[0])
        return matrix.as_array


class SightingCreateSerializer(serializers.Serializer):
    date = serializers.DateField(write_only=True)
    time = serializers.TimeField(write_only=True)
    observatory_code = serializers.CharField(write_only=True)
    device_code = serializers.CharField(write_only=True)
    device_resolution = serializers.CharField(write_only=True)
    device_matrix = serializers.CharField(write_only=True)

    def validate_observatory_code(self, value):
        if not value.startswith('ob_'):
            raise serializers.ValidationError("Observatory code must start with 'ob_'.")
        return value

    def validate_device_code(self, value):
        if not value.startswith('de_'):
            raise serializers.ValidationError("Device code must start with 'de_'.")
        return value

    def validate_device_resolution(self, value):
        if not re.match(r'^\d+x\d+$', value):
            raise serializers.ValidationError("Device resolution must be in the format 'NxM'.")
        return value

    def validate_device_matrix(self, value):
        if not re.match(r'^[01]+$', value):
            raise serializers.ValidationError("Device matrix must consist only of 0s and 1s.")
        return value


class AsteroidSerializer(serializers.ModelSerializer):
    matrix = serializers.SerializerMethodField()
    sightings = serializers.SerializerMethodField()

    class Meta:
        model = Asteroid
        fields = '__all__'

    def get_matrix(self, obj):
        matrix = MatrixService(vectorized_matrix=obj.normalized_matrix, n_cols=obj.cols)
        return matrix.as_array

    def get_sightings(self, obj):
        sightings = Sighting.objects.filter(asteroid=obj).order_by('-date', '-time')
        return SightingSerializer(sightings, many=True).data


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()

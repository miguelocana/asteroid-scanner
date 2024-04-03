import pandas as pd
from django.db import IntegrityError, transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Sighting, Observatory, Asteroid, Device
from .serializers import SightingSerializer, UploadFileSerializer, AsteroidSerializer, SightingCreateSerializer
from .services import MatrixService


class SightingViewSet(viewsets.ModelViewSet):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) |
                Q(date__icontains=search) |
                Q(time__icontains=search) |
                Q(device__code__icontains=search) |
                Q(observatory__code__icontains=search) |
                Q(asteroid__normalized_matrix__icontains=search) |
                Q(asteroid__id__icontains=search)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = SightingCreateSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            with transaction.atomic():
                observatory, _ = Observatory.objects.get_or_create(code=validated_data['observatory_code'])
                device, _ = Device.objects.get_or_create(
                    code=validated_data['device_code'],
                    defaults={'resolution': validated_data['device_resolution']}
                )

                try:
                    sighting = Sighting.objects.create(
                        date=validated_data['date'],
                        time=validated_data['time'],
                        device=device,
                        observatory=observatory,
                        matrix=validated_data['device_matrix']
                    )
                except IntegrityError:
                    return Response({'message': 'Some of the sightings are already uploaded.'},
                                    status.HTTP_400_BAD_REQUEST)

                if not sighting.is_matrix_complete:
                    cols, rows = device.cols_rows
                    return Response(
                        {'message': f"Device resolution ({device.resolution}={cols * rows}) and matrix length ({len(sighting.matrix)}) don't match"},
                        status=status.HTTP_400_BAD_REQUEST)

                if sighting.has_asteroid:
                    matrix_service = MatrixService(vectorized_matrix=sighting.matrix, n_cols=device.cols_rows[0])
                    matrix_service.normalize()

                    asteroid, created = Asteroid.objects.get_or_create(
                        normalized_matrix=matrix_service.as_vector,
                        defaults={'cols': matrix_service.cols, 'rows': matrix_service.rows}
                    )
                    sighting.asteroid = asteroid
                    sighting.save()
                return Response({"message": "Sighting created successfully"}, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AsteroidViewSet(viewsets.ModelViewSet):
    queryset = Asteroid.objects.all()
    serializer_class = AsteroidSerializer


class UploadFileViewSet(viewsets.ViewSet):
    serializer_class = UploadFileSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['file']
            try:
                data = pd.read_csv(csv_file, sep=',')

                for index, row in data.iterrows():
                    observatory, _ = Observatory.objects.get_or_create(code=row['observatory_code'])

                    device, _ = Device.objects.get_or_create(code=row['device_code'],
                                                             resolution=row['device_resolution'])

                    sighting = Sighting(
                        date=row['date'],
                        time=row['time'],
                        device=device,
                        observatory=observatory,
                        matrix=row['device_matrix']
                    )

                    if sighting.has_asteroid:
                        matrix = MatrixService(vectorized_matrix=sighting.matrix, n_cols=sighting.device.cols_rows[0])
                        matrix.normalize()

                        asteroid, created = Asteroid.objects.get_or_create(normalized_matrix=matrix.as_vector,
                                                                           cols=matrix.cols,
                                                                           rows=matrix.rows)
                        sighting.asteroid = asteroid
                    sighting.save()

                data = {"message": "File uploaded and processed successfully"}
                code = status.HTTP_200_OK
            except IntegrityError:
                data = {'message': 'Some of the sightings are already uploaded.'}
                code = status.HTTP_400_BAD_REQUEST
            except Exception as e:
                data = {'message': str(e)}
                code = status.HTTP_400_BAD_REQUEST
            finally:
                return Response(data, status=code)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

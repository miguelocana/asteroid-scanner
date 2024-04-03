import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Asteroid(BaseModel):
    normalized_matrix = models.TextField(unique=True)
    cols = models.IntegerField(null=True, blank=True)
    rows = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.normalized_matrix


class Observatory(BaseModel):
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.code


class Device(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    resolution = models.CharField(max_length=10)

    def __str__(self):
        return self.code

    @property
    def cols_rows(self) -> tuple[int, int]:
        cols, rows = map(lambda n: int(n), self.resolution.split('x'))
        return cols, rows


class Sighting(BaseModel):
    asteroid = models.ForeignKey(Asteroid, on_delete=models.CASCADE, related_name="sightings", null=True, blank=True)
    observatory = models.ForeignKey(Observatory, on_delete=models.CASCADE, related_name="sightings")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="sightings")
    matrix = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Sighting on {self.date} at {self.time}: {self.matrix}"

    class Meta:
        unique_together = ('date', 'time', 'device', 'observatory', 'matrix')

    @property
    def is_matrix_complete(self) -> bool:
        cols, rows = self.device.cols_rows
        return len(self.matrix) == cols * rows

    @property
    def has_asteroid(self) -> bool:
        return '1' in self.matrix

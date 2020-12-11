from django.db import models
from RealtimeAPS.models import Project

# Create your models here.
class Sensor(models.Model):
    serial = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sensors')
    up_lim_1 = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    up_lim_2 = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    up_lim_3 = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    low_lim_1 = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    low_lim_2 = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    low_lim_3 = models.DecimalField(max_digits=10, decimal_places=3, null=True)

    def __str__(self):
        return f"{self.serial} ({self.type})"

class ColorLog(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='logs')
    loggedtime = models.DateTimeField()
    Red = models.DecimalField(max_digits = 10, decimal_places = 3)
    Green = models.DecimalField(max_digits = 10, decimal_places = 3)
    Blue = models.DecimalField(max_digits = 10, decimal_places = 3)

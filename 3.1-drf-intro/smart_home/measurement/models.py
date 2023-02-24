from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=60, blank=True)
    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return self.name + " " + self.description

def user_directory_path(instance, imagename):
    return 'upload/sensor_{0}_{1}'.format(instance.sensor_id.id, imagename)
class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete = models.CASCADE, related_name='measurements')
    temp = models.FloatField(max_length=4, verbose_name='температура')
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(max_length=None, upload_to=user_directory_path, blank=True, null=True)#, allow_empty_file=False, blank=True use_url="./upload/photo"

    def update(self):
        created_date = models.DateTimeField(auto_now=True)
        super(models.Model, self).update()

    def __str__(self):
        datetime_created = self.created_date.strftime("%Y-%m-%d %H:%M")
        return 'время создания' + " " + str(datetime_created) + ",  " + str(self.temp) + " градусов"

    class Meta:
        verbose_name = 'Измерение температуры'
        verbose_name_plural = 'Измерения температуры'

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(TimeStampedModel):
    class Meta:
        ordering = ["title"]

    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class CityOrDistrict(TimeStampedModel):
    class Meta:
        ordering = ["title"]

    title = models.CharField(max_length=100)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

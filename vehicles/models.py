from django.db import models
from brands.models import Brand

class Vehicle(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles',
        verbose_name="Brand"
    )
    model_name = models.CharField(max_length=200, verbose_name="Model Name")
    model_year = models.PositiveIntegerField(verbose_name="Model Year")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(
        upload_to='vehicles/images/',
        null=True,
        blank=True,
        verbose_name="Image"
    )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.brand.name} {self.model_name} ({self.model_year})"

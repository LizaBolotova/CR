from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    category = models.CharField(max_length=50, blank=False, null=False)
    length = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    format = models.CharField(max_length=30, blank=False, null=False)
    cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], blank=False, null=False)
    sertificate = models.BooleanField(blank=False, null=False)
    stud_amount = models.IntegerField(default=0, validators=[MinValueValidator(0)], blank=False, null=False)
    avg_grade = models.FloatField(default=5.00, validators=[MinValueValidator(0)], blank=False, null=False)
    photo = models.ImageField(upload_to='course_photos/', blank=False)


    def __str__(self):
        return f'{self.name} - {self.category} - {self.length} - {self.format} - {self.cost} - {self.sertificate}'



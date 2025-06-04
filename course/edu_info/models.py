from django.db import models

# Create your models here.
class Page(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField(default=dict)
    show_in_nav = models.BooleanField(default=True)

    def __str__(self):
        return self.name
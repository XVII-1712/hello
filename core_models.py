from django.db import models

class LatticeDesign(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    optimal_use_case = models.TextField()

    def __str__(self):
        return self.name

from django.db import models

class LatticeDesign(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Application(models.Model):
    name = models.CharField(max_length=100)
    design = models.ForeignKey(LatticeDesign, on_delete=models.CASCADE)
    instructions = models.TextField()

from django.db import models

# This Model is for General Information
class GeneralInformation(models.Model):  
    topic = models.CharField(max_length=255)
    description = models.TextField()

# This Model is for Tutorials
class Tutorial(models.Model):  
    title = models.CharField(max_length=255)
    steps = models.TextField()
    info = models.ForeignKey(GeneralInformation, on_delete=models.CASCADE)

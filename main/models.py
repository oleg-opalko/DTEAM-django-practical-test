from django.db import models

class CV(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    projects = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    contacts = models.CharField(max_length=255)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    companyname = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 20, null = True)

    def __str__(self):
        return f"{self.user} {self.companyname} {self.phone}"

class Project(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return f"{self.user.username} {self.project.name}"

from django.db import models

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance,filename)

class TeamModel(models.Model):
    name=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    year=models.CharField(max_length=100)
    role=models.CharField(max_length=100)
    image=models.ImageField(upload_to=user_directory_path,default="default.png")
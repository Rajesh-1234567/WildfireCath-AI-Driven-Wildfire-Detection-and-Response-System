from django.db import models

class Map(models.Model):
    map_image = models.ImageField(upload_to='maps/')
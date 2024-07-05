from django.db import models

class Map(models.Model):
    map_image = models.ImageField(upload_to='maps/')
    created_at = models.DateTimeField(auto_now_add=True)
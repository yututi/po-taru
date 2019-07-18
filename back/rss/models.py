from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RssInfo(models.Model):
    user = models.ManyToManyField(User)
    site_name = models.CharField(max_length=40)
    url = models.URLField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.site_name

class Article(models.Model):
    site = models.ForeignKey(RssInfo, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    link = models.URLField()
    date = models.DateTimeField()
    img = models.URLField()

    def __str__(self):
        return self.description

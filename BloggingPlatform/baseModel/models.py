from django.db import models

class BlogPost(models.Model):
    # you must enter these 4 into the api request
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=15000)
    category = models.CharField(max_length=100)
    tags = models.JSONField(default=list)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    searchTitle = models.CharField(max_length=200, null=True)
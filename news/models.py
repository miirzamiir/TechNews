from django.db import models


class Tag(models.Model):
    tag_label = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.tag_label


class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(null=True)
    tags = models.ManyToManyField(to=Tag)
    resource = models.URLField(blank=False, unique=True)

    def __str__(self) -> str:
        return self.title
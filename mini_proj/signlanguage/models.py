from django.db import models

# Create your models here.

class Result(models.Model):
    image = models.ImageField(blank=True)
    answer = models.CharField(max_length=10)
    result = models.CharField(max_length=10)
    pub_date = models.DateTimeField('date published')

class AiModel(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=30)
    input_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    is_using = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
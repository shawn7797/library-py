from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)


class Publisher(models.Model):
    publisher_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    def __str__(self):
       return self.publisher_name
    def __unicode__(self):
       return self.publisher_name
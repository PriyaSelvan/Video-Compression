from django.db import models

# Create your models here.

class Video(models.Model):
	name = models.CharField(max_length = 140)
	mp4 = models.FileField(upload_to='uploads/')
	srt = models.FileField(upload_to='uploads/')
	scale = models.FloatField()
	
	def __str__(self):
		return (self.name)

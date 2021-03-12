from django.db import models
from PIL import Image
from django.core.validators import MaxValueValidator


class RplUsers(models.Model):
	UserName = models.CharField(max_length=30, unique=True)
	emailId = models.EmailField(unique=True)
	mobile = models.BigIntegerField(unique=True, validators=[MaxValueValidator(9999999999)])
	activeflag = models.BooleanField(default=False)
	pwd = models.CharField(max_length=1000)	
	UserImg = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default.jpg')
	
	def __str__(self): 
		return self.UserName
	
	def save(self):
		super().save()  # saving image first

		img = Image.open(self.UserImg.path)  # Open image using self

		if img.height > 300 or img.width > 300:
			new_img = (300, 300)
			img.thumbnail(new_img)
			img.save(self.UserImg.path)  # saving image at the same path


class PlayerList(models.Model):

	class Meta:
		unique_together = (('teamId', 'playerId'),)
		
	teamId = models.IntegerField(null=True, blank=True)
	teamDisName = models.CharField(max_length=100, null=True, blank=True)
	teamName = models.CharField(max_length=10, null=True, blank=True)
	playerId = models.IntegerField(null=True, blank=True)
	playerName = models.CharField(max_length=100, null=True, blank=True)
	
	def __str__(self): 
		return self.playerName


class Selected(models.Model):

	class Meta:
		unique_together = (('userName', 'matchId', 'seriesId'),)
	userName = models.CharField(max_length=30)
	seriesId = models.IntegerField(default=0)
	matchId = models.IntegerField()
	player1 = models.CharField(max_length=100)
	player2 = models.CharField(max_length=100)
	player3 = models.CharField(max_length=100)
	player4 = models.CharField(max_length=100)
	player5 = models.CharField(max_length=100)
	bat1 = models.FloatField(default=0)
	bat2 = models.FloatField(default=0)
	bowl1 = models.FloatField(default=0)
	bowl2 = models.FloatField(default=0)
	allround = models.FloatField(default=0)
	total = models.FloatField(default=0)
	point = models.DecimalField(default=0, max_digits=8, decimal_places=4)
	
	def __str__(self): 
		return self.userName + str(self.matchId)
	
	
class parmtable(models.Model):
	parm_id = models.CharField(max_length=4, unique=True)
	parm_key = models.CharField(max_length=35, unique=True)
	parm_data = models.CharField(max_length=100)
	parm_dsec = models.CharField(max_length=100)
	
	def __str__(self): 
		return self.parm_key
	

class Otptabl(models.Model):
	UserName = models.CharField(max_length=35, unique=True)
	Otp = models.IntegerField(default=0)
	
	def __str__(self): 
		return self.UserName

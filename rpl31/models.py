from django.db import models
from django.core.validators import MaxValueValidator


class RplUsers(models.Model):
	UserName = models.CharField(max_length=30, unique=True)
	emailId = models.EmailField(unique=True)
	mobile = models.BigIntegerField(unique=True, validators=[MaxValueValidator(9999999999)])
	activeflag = models.BooleanField(default=False)
	pwd = models.CharField(max_length=1000)
	image = models.FileField(null=True, editable=True, default='default.jpg')
	image_data = models.BinaryField(null=True, default=b'\x08')
	
	def __str__(self): 
		return self.UserName


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


class SelectedPlayers(models.Model):

	userName = models.CharField(max_length=30)
	seriesId = models.IntegerField(default=0)
	matchId = models.IntegerField()
	bat1 = models.CharField(max_length=100)
	bat2 = models.CharField(max_length=100)
	bowl1 = models.CharField(max_length=100)
	bowl2 = models.CharField(max_length=100)
	allrounder = models.CharField(max_length=100)

	def __str__(self):
		return self.userName + str(self.matchId)

	class Meta:
		managed = False
		db_table = "selected_players"
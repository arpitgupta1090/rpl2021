from django import forms
from django.utils.translation import gettext_lazy as _
from .models import RplUsers
from .config import Envariable
from .formatdata import getSeries

'''
#fetching parameters from parm_table
#parmdata = getparm()
#sid = parmdata.get('sid')
#sid = '19495'

#plist, dict = liveteam(sid)
#matchid = dict.get('matchid')
#matchdesc = dict.get('match_desc')

#if len(plist) == 0:
#	matchdesc = 'No upcoming matches'
#else:
#	matchdesc = dict.get('match_desc')

#plist = [('a','b'),('c','d'),('e','f')]
#matchid = 123
#matchdesc = 'Temp match'


#mlist = [(1,'b'),(2,'d'),(3,'f')]'''


class SelectForm(forms.Form):

	def __init__(self, *args, **kwargs):
		sid = Envariable().sid
		match_id, match_desc, plist = getSeries(sid, 'live')
		super(SelectForm, self).__init__(*args, **kwargs)
		self.fields['matchid'].initial = match_id
		self.fields['matchdesc'].initial = match_desc
		self.fields['player1'].choices = plist
		self.fields['player2'].choices = plist
		self.fields['player3'].choices = plist
		self.fields['player4'].choices = plist
		self.fields['player5'].choices = plist

	matchid = forms.DecimalField(widget=forms.HiddenInput())
	matchdesc = forms.CharField(label='Match', disabled=True, widget=forms.Textarea(attrs={'cols': 40, 'rows': 2}))
	player1 = forms.ChoiceField(label='Select 1st Batsman')
	player2 = forms.ChoiceField(label='Select 2nd Batsman')
	player3 = forms.ChoiceField(label='Select 1st Bowler')
	player4 = forms.ChoiceField(label='Select 2nd Bowler')
	player5 = forms.ChoiceField(label='Select All-rounder')
	
	
class ScoreForm(forms.Form):

	def __init__(self, *args, **kwargs):
		sid = Envariable().sid
		super(ScoreForm, self).__init__(*args, **kwargs)
		self.fields['matchid'].choices = getSeries(sid, 'past')
	
	matchid = forms.ChoiceField(label='Select match')
	

class UploadForm(forms.ModelForm):
	class Meta: 
		model = RplUsers
		fields = ['image']

		
class UpdateForm(forms.ModelForm): 
	class Meta: 
		model = RplUsers
		fields = ('emailId', 'mobile')
		help_texts = {'emailId': _('xxx@yyy.zz'), 'mobile': _('10 digit number')}


class PassForm(forms.ModelForm):

	new_password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = RplUsers
		fields = ['pwd']
		widgets = {'pwd': forms.PasswordInput(), }
		labels = {'pwd': 'Current Password', }
		
	def clean(self):
		cleaned_data = super(PassForm, self).clean()
		password = cleaned_data.get("new_password")
		confirm_password = cleaned_data.get("confirm_password")

		if password != confirm_password and password:
			raise forms.ValidationError("password and confirm_password does not match")
		return cleaned_data


class OtpForm(forms.Form):

	UserName = forms.CharField(label="Email or User name")
	new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
	otp = forms.DecimalField(required=False, widget=forms.Textarea(attrs={'cols': 6, 'rows': 1}))

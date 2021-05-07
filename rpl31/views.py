from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import RedirectView, View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rpl31.functions import *
from rpl31.forms import ScoreForm, UploadForm, UpdateForm, PassForm, OtpForm, SelectModelForm, RegisterForm, LoginForm
from rpl31.models import RplUsers, Selected, Otptabl, parmtable
from rpl31.profile import getSelect, getWin, getProfile
from rpl31.config import Envariable
from rpl31.formatdata import getSeries, getMatch
from rpl31.decorator import time_taken
from rpl31.mixins import UserMixin
import random


@csrf_exempt
def home(request):
	if 'username' in request.session:
		username = request.session['username']
		return render(request, 'login.html', {"username": username})
	sid = Envariable().sid
	series = getSeries(sid, 'name')
	return render(request, 'home.html', {'series': series})


class RegisterView(SuccessMessageMixin, CreateView):

	template_name = 'baseform.html'
	form_class = RegisterForm
	model = Selected
	success_url = 'home'
	success_message = "User created. Please contact admin for activation"

	def get_context_data(self, **kwargs):
		context = super(RegisterView, self).get_context_data(**kwargs)
		context['title'] = "Sign Up"
		return context


@method_decorator(csrf_exempt, name='post')
class LoginView(View):

	template_name = 'logging.html'
	form_class = LoginForm

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		context = {'form': form, 'title': "Login"}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		email = request.POST['emailId']
		try:
			instance = RplUsers.objects.get(emailId=email)
		except RplUsers.DoesNotExist:
			messages.error(request, 'Email id not registered')
			return redirect('home')

		form = LoginForm(request.POST, instance=instance)

		if form.is_valid():
			request.session['username'] = instance.UserName
			return render(request, 'login.html', {'username': instance.UserName})
		else:
			return render(request, self.template_name, {'form': form, 'title': "Login"})


@csrf_exempt
def logout(request):
	try:
		del request.session['username']
		msg = "Logged out"
	except Exception as e:
		msg = str(e)
	messages.info(request, msg)
	return redirect('home')


@csrf_exempt  
def updateTeam(request):
	sid = Envariable().sid
	result = parmtable.objects.get(parm_id='P005')
	team_fullname_list = result.parm_key.split('|')
	team_name_list = result.parm_data.split('|')
	res = update_team(sid, team_name_list, team_fullname_list)
	return HttpResponse(res)


@csrf_exempt  
def reloadTeam(request):
	sid = Envariable().sid
	res = getSeries(sid, 'players')
	return HttpResponse(res)


class SelectRedirectView(UserMixin, RedirectView):

	def get_redirect_url(self):
		sid = Envariable().sid
		match_id, match_desc, plist = getSeries(sid, 'live')
		try:
			player = Selected.objects.get(userName=self.request.session['username'], matchId=match_id, seriesId=sid)
			pk = player.id
			return reverse('update', args=(pk,))
		except Selected.DoesNotExist:
			return reverse('add')


class SelectPlayer(UserMixin, SuccessMessageMixin, CreateView):

	template_name = 'baseform.html'
	form_class = SelectModelForm
	model = Selected
	success_url = 'login'
	success_message = "Players added successfully"

	def get_initial(self, *args, **kwargs):
		initial = super(SelectPlayer, self).get_initial(**kwargs)
		initial['userName'] = self.request.session['username']
		return initial


class UpdatePlayer(UserMixin, SuccessMessageMixin, UpdateView):

	template_name = 'baseform.html'
	form_class = SelectModelForm
	model = Selected
	success_message = "Players updated successfully"

	def get_success_url(self):
		return reverse('login')


@csrf_exempt
def selectPlayerOffline(request):

	sid = Envariable().sid
	select1status = Envariable().select1status

	if request.method == 'GET':
		if 'username' in request.session:
			lst1, lst2 = getSeries(sid, 'dropdown')
			context = {'post1': lst1, 'post2': lst2}
			return render(request, 'selectPlayerOffline.html', context)
		else:
			messages.info(request, 'Invalid Session')
			return redirect('home')
	else:
		match_id = request.POST['matchid']
		player1 = getplayerid(request.POST['category'])
		player2 = getplayerid(request.POST['category1'])
		player3 = getplayerid(request.POST['category2'])
		player4 = getplayerid(request.POST['category3'])
		player5 = getplayerid(request.POST['category4'])
		username = request.session['username']
		
		if 'dormant' in select1status:
			# if m.status == 'dormant'  or m.status == 'forthcoming':

			if player5 == player1 or player5 == player2:
				messages.info(request, 'Batsman and All-rounder can\'t be same')
				return redirect('selectPlayerOffline')

			elif player1 == player2:
				messages.info(request, 'Both batsmen can\'t be same')
				return redirect('selectPlayerOffline')

			elif player5 == player3 or player5 == player4:
				messages.info(request, 'Bowler and All-rounder can\'t be same')
				return redirect('selectPlayerOffline')

			elif player3 == player4:
				messages.info(request, 'Both Bowlers can\'t be same')
				return redirect('selectPlayerOffline')
				
			select_check = Selected.objects.filter(userName=username).filter(matchId=match_id).filter(seriesId=sid)
			
			if select_check.count() == 0:
				player = Selected(
						userName=username, matchId=match_id, player1=player1, player2=player2,
						player3=player3, player4=player4, player5=player5, seriesId=sid)

				player.save()
				messages.info(request, 'Player Successfully Added')
			else:
				player = Selected.objects.get(userName=username, matchId=match_id, seriesId=sid)
				player.player1 = player1
				player.player2 = player2
				player.player3 = player3
				player.player4 = player4
				player.player5 = player5
				player.save()
				messages.info(request, 'Player Successfully updated')
				
			return redirect('login')
			
		else:
			messages.info(request, 'Match already started')
			return redirect('selectPlayerOffline')


@csrf_exempt
@time_taken
def scorecard(request):

	if request.method == 'POST':
		if 'username' in request.session:
			form = ScoreForm(request.POST)
			if form.is_valid():
				match_id = request.POST['matchid']
				table_data = getMatch(match_id, 'score')
				return render(request, 'scorecard.html', {'data': table_data, 'form': form})
		else:
			messages.info(request, 'Invalid Session')
			return redirect('home')
	
	else:
		if 'username' in request.session:
			form = ScoreForm()
			return render(request, 'scorecard.html', {'form': form})
		else:
			messages.info(request, 'Invalid Session')
			return redirect('home')


@csrf_exempt
def profile(request):

	if 'username' in request.session:
		username = request.session['username']
		profile_data = getProfile(username)
		return render(request, 'myprofile.html', profile_data)
	else:
		return redirect('home')


def selection(request):

	if 'username' in request.session:
		username = request.session['username']
		sid = Envariable().sid

		match_id_list = list()
		match_desc_list = list()

		matches = getSeries(sid, 'all')

		for match in matches:
			match_id_list.append(match[0])
			match_desc_list.append(match[1])

		profile_data = getSelect(username, match_id_list, match_desc_list)
		return render(request, 'selection.html', profile_data)
	else:
		return redirect('home')
		
		
def winners(request):

	if 'username' in request.session:
		sid = Envariable().sid

		match_id_list = list()
		match_desc_list = list()

		matches = getSeries(sid, 'all')

		for match in matches:
			match_id_list.append(match[0])
			match_desc_list.append(match[1])

		profile_data = getWin(match_id_list, match_desc_list)
		return render(request, 'winners.html', profile_data)
	else:
		return redirect('home')


@csrf_exempt
def uploadPhoto(request):
	
	if request.method == 'POST':
		username = request.session['username']
		instance = RplUsers.objects.get(UserName=username)
		form = UploadForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			uploaded_img = form.save(commit=False)
			uploaded_img.image_data = form.cleaned_data['image'].file.read()
			uploaded_img.save()
			messages.info(request, 'Photo successfully uploaded')
		else:
			form = UploadForm()
			messages.info(request, 'Invalid data entered')
		return render(request, 'baseform.html', {'form': form})

	else:
		if 'username' in request.session:
			form = UploadForm()
			return render(request, 'baseform.html', {'form': form})
		else:
			messages.info(request, 'Invalid Session')
			return redirect('home')
			
			
@csrf_exempt 
def updateProfile(request):
	
	if request.method == 'POST':
		username = request.session['username']
		instance = RplUsers.objects.get(UserName=username)
		form = UpdateForm(request.POST, instance=instance)
		if form.is_valid():
			form.save()
			messages.info(request, 'Profile successfully updated')
		else:
			form = UpdateForm()
			messages.info(request, 'Invalid Mobile/Email format')
		return render(request, 'updateprofile.html', {'form': form})

	else:
		if 'username' in request.session:
			form = UpdateForm()
			return render(request, 'updateprofile.html', {'form': form})
		else:
			messages.info(request, 'Invalid Session')
			return redirect('home')
			
			
@csrf_exempt 
def changePassowrd(request):
	
	if request.method == 'POST':
		username = request.session['username']
		instance = RplUsers.objects.get(UserName=username)
		curr_pwd = instance.pwd
		form = PassForm(request.POST, instance=instance)

		if form.is_valid():
			old_pwd = request.POST['pwd']
			if check_password(old_pwd, curr_pwd):
				new_pass = form.cleaned_data['new_password']
				instance.pwd = make_password(new_pass)
				instance.save()
				messages.info(request, 'Password successfully updated')
			else:
				messages.info(request, 'Invalid password')
		else:
			form = PassForm()
			messages.info(request, 'Passwords did not match/ Invalid data')
		return render(request, 'updatepassword.html', {'form': form})

	else:
		if 'username' in request.session:
			form = PassForm()
			return render(request, 'updatepassword.html', {'form': form})
		else:

			messages.info(request, 'Invalid Session')
			return redirect('home')


@csrf_exempt 
def forgotPassword(request):

	otp_pwd = random.randint(111111, 999999)
	
	if request.method == 'POST':
		form = OtpForm(request.POST)
		if form.is_valid():
			otp_recv = request.POST['otp']
			pwd_recv = request.POST['new_password']
			user_recv = request.POST['UserName']
			pwd_conf = request.POST['confirm_password']
			if not otp_recv:

				try:
					user = RplUsers.objects.get(UserName=user_recv)
					print("User name exists")
					otpmail(user.emailId, otp_pwd)

					try:
						Otptabl(UserName=user_recv, Otp=otp_pwd).save()
					except Exception as e:
						print(str(e))
						Otptabl.objects.filter(UserName=user_recv).update(Otp=otp_pwd)

					messages.info(
						request, 'Otp has been sent to your Email. '
						'Please enter received otp with all the other details then click on submit')

				except Exception as e:
					print(str(e))

					try:
						RplUsers.objects.get(emailId=user_recv)
						otpmail(user_recv, otp_pwd)

						try:
							Otptabl(UserName=user_recv, Otp=otp_pwd).save()
						except Exception as e:
							print(str(e))

							Otptabl.objects.filter(UserName=user_recv).update(Otp=otp_pwd)

						messages.info(
								request, 'Otp has been sent to your Email. '
								'Please enter received otp with all the other details then click on submit')

					except Exception as e:
						print(str(e))
						messages.info(request, 'User does not exist')
				return render(request, 'otp.html', {'form': form})

			else:	
				try:
					user = RplUsers.objects.filter(UserName=user_recv) | RplUsers.objects.filter(emailId=user_recv)
					if pwd_recv == pwd_conf:

						enc_pwd = make_password(pwd_recv)
						user.update(pwd=enc_pwd)
						messages.info(request, 'Password changed')
						return redirect('home')
					else:
						messages.info(request, 'Password Mismatch')
						return render(request, 'otp.html', {'form': form})

				except Exception as e:
					print(str(e))
					messages.info(request, 'Incorrect Otp/Username')
					return render(request, 'otp.html', {'form': form})
			
	else:
		form = OtpForm()
		messages.info(request, 'Please first enter your Email Id or User Name and click on Get OTP')
		return render(request, 'otp.html', {'form': form})

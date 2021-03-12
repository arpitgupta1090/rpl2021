from . import views
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
	path('', views.login, name='login'),
	path('home', views.home, name='home'),
	path('register', views.register, name='register'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('selectplayer1', views.selectPlayersLive, name='selectPlayersLive'),
	path('selectplayer2', views.selectPlayerOffline, name='selectPlayerOffline'),
	path('scorecard', views.scorecard, name='scorecard'),
	path('profile', views.profile, name='profile'),
	path('selection', views.selection, name='selection'),
	path('winners', views.winners, name='winners'),
	path('uploadphoto', views.uploadPhoto, name='uploadPhoto'),
	path('updateprofile', views.updateProfile, name='updateProfile'),
	path('changepassowrd', views.changePassowrd, name='changePassowrd'),
	path('forgotpassword', views.forgotPassword, name='forgotPassword'),
	path('reloadteam', views.reloadTeam, name='reloadTeam'),
	path('updateteam', views.updateTeam, name='updateTeam'),
]

if settings.DEBUG: 
	urlpatterns += static(
							settings.MEDIA_URL,
							document_root=settings.MEDIA_ROOT
						)

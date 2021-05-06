from . import views
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
	path('', views.home, name='home'),
	path('home', views.home, name='home'),
	path('logout', views.logout, name='logout'),
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
	path('add', views.SelectPlayer.as_view(), name='add'),
	path('update/<pk>/', views.UpdatePlayer.as_view(), name='update'),
	path('select', views.SelectRedirectView.as_view(), name='select'),
	path('register', views.RegisterView.as_view(), name='register'),
	path('login', views.LoginView.as_view(), name='login'),
]

if settings.DEBUG: 
	urlpatterns += static(
							settings.MEDIA_URL,
							document_root=settings.MEDIA_ROOT
						)

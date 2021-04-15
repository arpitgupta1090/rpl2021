from .models import Selected, RplUsers
from .functions import getPlayerName
from django.db.models import Max, Sum
from natsort import natsorted
from .config import Envariable
from .formatdata import getSeries
from base64 import b64encode
from functools import lru_cache


def getProfile(username):

	sid = Envariable().sid
	no_of_select_dict = Envariable().noofselectdict
	no_of_win_dict = Envariable().noofwindict

	match_id_list = list()
	match_desc_list = list()
	matches = getSeries(sid, 'all')

	for match in matches:
		match_id_list.append(match[0])
		match_desc_list.append(match[1])

	user_dict, lead_dict = getUser(username, sid)
	select_dict = getSelect(username, match_id_list, match_desc_list, no_of_select_dict)
	win_dict = getWin(match_id_list, match_desc_list, no_of_win_dict)

	dict1 = {**user_dict, **lead_dict, **select_dict, **win_dict}
	return dict1
	

def getUser(username, sid):

	base_amount = Envariable().baseamount
	no_of_leaders = Envariable().noofleaders

	dict1 = {}
	dict2 = {}
	name = username

	# series = 'Indian Premier League'
	series = getSeries(sid, 'name')
	user_set = RplUsers.objects.get(UserName=username)
	encoded = b64encode(user_set.image_data).decode('ascii')
	
	results = Selected.objects.filter(userName=username).filter(seriesId=sid).aggregate(Sum('point'), Sum('total'))
	score = results['total__sum']
	point = results['point__sum']
	
	if not score:
		score = 0
	else:
		score = round(results['total__sum'], 4)
		
	if not point:
		point = 0
	else:
		point = round(results['point__sum'], 4)
		
	amount = round((point * base_amount), 2)
	
	all_rec = Selected.objects.filter(seriesId=sid).values('userName').annotate(points=Sum('point')).order_by('-points')
	sort_list = sorted(all_rec, key=lambda i: i['points'], reverse=True)

	photo = ""

	if sort_list:
		winner = sort_list[0].get('userName')
		photo_set = RplUsers.objects.get(UserName=winner)
		photo = b64encode(photo_set.image_data).decode('ascii')
		
	rank = 0
	for user in sort_list:
		rank += 1
		if user.get('userName') == name:
			break

	dict1['name'] = name
	dict1['image'] = encoded
	dict1['series'] = series
	dict1['score'] = score
	dict1['point'] = point
	dict1['amount'] = amount
	dict1['photo'] = photo
	dict1['rank'] = rank
	dict1['userset'] = user_set
	dict2['leaddata'] = sort_list[:no_of_leaders]

	return dict1, dict2
	

def getSelect(username, match_id_list, match_desc_list, counter=None):

	sid = Envariable().sid
	lst = []

	recent = Selected.objects.filter(userName=username).filter(seriesId=sid).order_by('-id')[:counter]

	for rec in recent:
		mdesc = match_desc_list[match_id_list.index(str(rec.matchId))]
		lst.append(
					{'match': mdesc, 'p1': getPlayerName(rec.player1),
						'p2': getPlayerName(rec.player2),
						'p3': getPlayerName(rec.player3),
						'p4': getPlayerName(rec.player4),
						'p5': getPlayerName(rec.player5)}
		)
	
	return {'selectdata': lst}
	
	
def getWin(match_id_list, match_desc_list, counter=None):
	sid = Envariable().sid
	lst = []
	
	all_rec = Selected.objects.filter(seriesId=sid).values('matchId').annotate(points=Max('point')).order_by('-points')

	for rec in all_rec:
		if rec.get('points') > 0:
			all_rec1 = Selected.objects.filter(seriesId=sid).filter(matchId=rec.get('matchId')).filter(point=rec.get('points'))
			username = all_rec1[0].userName
			score = all_rec1[0].total
			match_desc = match_desc_list[match_id_list.index(str(all_rec1[0].matchId))]
			# photo_name = RplUsers.objects.get(UserName=username)
			# photo = b64encode(photo_name.image_data).decode('ascii')
			photo = get_image(username)
			lst.append({'winname': username, 'photoname': photo, 'winmatch': match_desc, 'winscore': score})

	sort_list = natsorted(lst, key=lambda i: i.get('winmatch'), reverse=True)[:counter]

	return {'windata': sort_list}


@lru_cache(maxsize=None)
def get_image(username):
	photo_name = RplUsers.objects.get(UserName=username)
	photo = b64encode(photo_name.image_data).decode('ascii')
	return photo

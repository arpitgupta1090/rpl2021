from django.conf import settings
from django.core.mail import send_mail
import traceback
from .models import PlayerList, Selected
from .config import Envariable


def ranker2(dict1, sbit, mname):
	dict4 = {}
	top1 = []
	top2 = []
	top3 = []

	lst = sorted(set(dict1.values()), reverse=True)[:3]
	for k, v in dict1.items():
		if v == lst[0]:
			top1.append(k)
		elif v == lst[1]:
			top2.append(k)
		elif v == lst[2]:
			top3.append(k)
	
	top1_count = len(top1)
	top2_count = len(top2)
	top3_count = len(top3)

	if top1_count == 0:
		top1_part = 0
		top2_part = 0
		top3_part = 0
		
	elif top2_count == 0:
		top1_part = 1.0 / top1_count
		top2_part = 0
		top3_part = 0
	elif top3_count == 0:
		if top1_count == 1:
			top1_part = 0.6
			top2_part = 0.4 / top2_count
			top3_part = 0
		else:
			top1_part = 6 / ((6 * top1_count) + (4 * top2_count))
			top2_part = 4 / ((6 * top1_count) + (4 * top2_count))
			top3_part = 0
	elif top1_count == 1:
		if top2_count == 1:
			if top3_count == 1:
				top1_part = 0.5
				top2_part = 0.3
				top3_part = 0.2
			else:
				top1_part = 0.5
				top2_part = 0.3
				top3_part = 0.2 / top3_count
		else:
			top1_part = 0.5
			top2_part = (3 * 0.5) / ((3 * top2_count) + (2 * top3_count))
			top3_part = (2 * 0.5) / ((3 * top2_count) + (2 * top3_count))
	else:
		top1_part = 5 / ((5 * top1_count) + (3 * top2_count) + (2 * top3_count))
		top2_part = 3 / ((5 * top1_count) + (3 * top2_count) + (2 * top3_count))
		top3_part = 2 / ((5 * top1_count) + (3 * top2_count) + (2 * top3_count))
		
	top1_part = round(top1_part, 4)
	top2_part = round(top2_part, 4)
	top3_part = round(top3_part, 4)
		
	for k, v in dict1.items():
		if k in top1:
			dict4[k] = specialscore(top1_part, sbit, mname)
		elif k in top2:
			dict4[k] = specialscore(top2_part, sbit, mname)
		elif k in top3:
			dict4[k] = specialscore(top3_part, sbit, mname)
		else:
			dict4[k] = 0

	return dict4
	

def playerscore(plist, batdict, bowldict):

	score1 = score2 = score3 = score4 = 0
	p1 = int(plist[0])
	p2 = int(plist[1])
	p3 = int(plist[2])
	p4 = int(plist[3])
	p5 = int(plist[4])

	if p1 in batdict:
		bat_score = [
			batdict.get(p1).get('runs'), batdict.get(p1).get('sixes'),
			batdict.get(p1).get('fours'), 0, 0, 0, 0]
		score1 = scoring(bat_score, 'bat')

	if p2 in batdict:
		bat_score = [
					batdict.get(p2).get('runs'), batdict.get(p2).get('sixes'),
					batdict.get(p2).get('fours'), 0, 0, 0, 0]
		score2 = scoring(bat_score, 'bat')

	if p3 in bowldict:
		bat_score = [
					0, 0, 0, bowldict.get(p3).get('economyRate'), bowldict.get(p3).get('maidens'),
					bowldict.get(p3).get('wickets'), bowldict.get(p3).get('overs')]
		score3 = scoring(bat_score, 'bowl')
		
	if p4 in bowldict:
		bat_score = [
					0, 0, 0, bowldict.get(p4).get('economyRate'), bowldict.get(p4).get('maidens'),
					bowldict.get(p4).get('wickets'), bowldict.get(p4).get('overs')]
		score4 = scoring(bat_score, 'bowl')
		
	if p5 in bowldict:
		bowl_score = [
			bowldict.get(p5).get('economyRate'), bowldict.get(p5).get('maidens'),
			bowldict.get(p5).get('wickets'), bowldict.get(p5).get('overs')
		]
	else:
		bowl_score = [0, 0, 0, 0]
	
	if p5 in batdict:
		bat_score5 = [batdict.get(p5).get('runs'), batdict.get(p5).get('sixes'), batdict.get(p5).get('fours')]
	else:
		bat_score5 = [0, 0, 0]
		
	player_score = bat_score5 + bowl_score
	score5 = scoring(player_score, 'all',)
	score = [score1, score2, score3, score4, score5]
	return score


def scoring(slist, ptype):

	run = six = four = mdn = wkt = over = eco = 0

	if slist[0]:
		run = int(slist[0])
	if slist[1]:
		six = int(slist[1])
	if slist[2]:
		four = int(slist[2])
	if slist[3]:
		eco = float(slist[3])
	if slist[4]:
		mdn = int(slist[4])
	if slist[5]:
		wkt = int(slist[5])
	if slist[6]:
		over = round(float(slist[6]))

	bat_score = (four * 1) + (six * 2) + (run * 0.2)
	eco_point = lambda eco: (over * 2) if eco <= 7.5 else ((over * 1) if eco <= 10 else 0)
	bowl_score = (mdn * 4) + (wkt * 4) + eco_point(eco)

	if ptype == 'bat':
		return bat_score
	elif ptype == 'bowl':
		return bowl_score
	else:
		return bat_score + bowl_score
		

def setScore(mid, bat_dict, bowl_dict, sid, mname):

	sbit = Envariable().sbit
	try:
		dict1 = {}
		all_rec = Selected.objects.filter(matchId=mid).filter(seriesId=sid)
		for rec in all_rec:
			plist = [rec.player1, rec.player2, rec.player3, rec.player4, rec.player5]
			score = playerscore(plist, bat_dict, bowl_dict)
			print(plist)
			# print(bat1score,bat2score,bowl1score,bowl2score,allscore)
			rec.bat1 = round(score[0], 2)
			rec.bat2 = round(score[1], 2)
			rec.bowl1 = round(score[2], 2)
			rec.bowl2 = round(score[3], 2)
			rec.allround = round(score[4], 2)
			rec.total = round(score[0] + score[1] + score[2] + score[3] + score[4], 2)
			rec.save()
			dict1[rec.userName] = rec.total
		dict2 = ranker2(dict1, sbit, mname)
		# print(dict2)
		for k, v in dict2.items():
			point_rec = Selected.objects.get(matchId=mid, userName=k, seriesId=sid)
			# print(point_rec.userName,k,v)
			point_rec.point = v
			point_rec.save()
		return 'saved'
	except Exception as e:
		print(traceback.format_exc())
		return e


def getPlayerName(pid):
	sid = Envariable().sid
	try:
		prec = PlayerList.objects.get(playerId=pid, teamId=sid)
		return prec.playerName
	except Exception as e:
		return e
	

def getplayerid(pname):

	sid = Envariable().sid

	try:
		pid = PlayerList.objects.get(playerName=pname,teamId=sid).playerId
		return pid

	except Exception as e:
		print(str(e))
		return 00000
		

def otpmail(mailid, otp):
	subject = 'Hey Buddy'
	message = f'Hi, please use {otp} to reset your password'
	email_from = settings.EMAIL_HOST_USER 
	recipient_list = [mailid, ] 
	send_mail(subject, message, email_from, recipient_list)


def update_team(sid, team_fullname_list, team_name_list):

	for fullname, name in zip(team_fullname_list, team_name_list):
		PlayerList.objects.filter(teamId=sid).filter(teamDisName__contains=fullname).update(teamName=name)

	return 'team updated'

	
def specialscore(score, sbit, mname):

	if sbit == 'True':
		s1point = Envariable().s1point
		s2point = Envariable().s2point
		s1desc = Envariable().s1desc
		s2desc = Envariable().s2desc

		s1desclist = s1desc.split('|')
		s2desclist = s2desc.split('|')

		res1 = any(ele in mname for ele in s1desclist)
		res2 = any(ele in mname for ele in s2desclist)

		if res1:
			return score * float(s1point)
		elif res2:
			return score * float(s2point)
		else:
			return score
	else:
		return score

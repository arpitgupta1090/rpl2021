from .cricpunch import Series
from .cricpunch import Match
from .config import Envariable
from .models import PlayerList, Selected
from .functions import setScore, getPlayerName


def getSeries(sid, i_parm=None):

    s = Series(sid)

    if i_parm == 'name':
        return s.name.get("name")
    elif i_parm == 'players':
        return setPlayers(s.players, sid)
    elif i_parm == 'dropdown':
        return getPlayersOffline(s.matches)
    elif i_parm == 'live':
        return getLiveMatch(s.matches)
    elif i_parm == 'past':
        return getAllMatch(s.matches, 'past')
    elif i_parm == 'all':
        return getAllMatch(s.matches, 'all')


def getMatch(mid, i_parm=None):

    m = Match(mid)

    if i_parm == 'name':
        return m.title
    elif i_parm == 'status':
        return m.status
    elif i_parm == 'desc':
        return m.description
    elif i_parm == 'score':
        return getScore(mid, m.score, m.title)


def setPlayers(player_list, sid):
    for team in player_list:

        for player in team:

            team = player.get("player_team")
            player_id = player.get("player_id")
            player_name = player.get("player_name")

            rec = PlayerList(teamDisName=team, playerId=player_id, playerName=player_name, teamId=sid)

            try:
                rec.save()
            except Exception as e:
                print(e)

    return "player loaded in DB"


def getPlayersOffline(matches):

    select2status = Envariable().select2status
    match_list = []
    match_id_list = []
    team_list = []
    team_list1 = []
    lst = []
    dict1 = {}

    for i in matches:
        # if i.get('state') == 'Scheduled' or i.get('state') == 'Result' or i.get('state') == 'Default':
        if i.get('state') in select2status:
            match_list.append(i.get('match_desc'))
            match_id_list.append(i.get('match_id'))
            team_list1.append(str(i.get('team1')) + str(i.get('team2')))
            team_list.append(i.get('team1'))
            team_list.append(i.get('team2'))

    team_list = sorted(set(team_list))

    for match, team, matchid in zip(match_list, team_list1, match_id_list):
        lst.append({'match': match, 'team': team, 'matchid': matchid})

    for team in team_list:
        player_list = get_player_list(team)
        dict1[team] = player_list

    lst2 = sorted(set(team_list1))
    dct = create_team(dict1, lst2)

    return lst, dct


def get_player_list(team_name):

    lst = []
    sid = Envariable().sid
    all_rec = PlayerList.objects.filter(teamName=team_name).filter(teamId=sid).order_by('playerName')

    for rec in all_rec:
        lst.append(rec.playerName)

    return lst


def create_team(dict1, lst):

    print_var = ""

    for k1, v1 in dict1.items():
        for k2, v2 in dict1.items():

            if str(k1 + k2) in lst:
                print_v = str(k1 + k2 + ":" + str(v1) + "," + str(v2) + ",").replace("],[", ",")
                print_var += print_v

    return print_var


def getLiveMatch(match_id_list):

    select1status = Envariable().select1status
    team_list = []

    for mid in match_id_list:
        m = Match(mid['match_id'])
        match_name = m.description
        match_status = m.status

        # if mstatus == 'dormant'  or mstatus == 'forthcoming' or mstatus == 'complete':
        if match_status in select1status:
            # team = m.squads
            team = sorted(m.squads, key=lambda i: i['player_name'])
            for player in team:
                team_list.append((player.get("player_id"), player.get("player_name")))
            break
        else:
            match_name = 'No live match'

    return mid['match_id'], match_name, team_list


def getScore(mid, score, name):

    sid = Envariable().sid
    bat_dict, bowl_dict = score

    if bat_dict:
        setScore(mid, bat_dict, bowl_dict, sid, name)
    lst = []
    sort_list = []

    try:
        all_rec = Selected.objects.filter(matchId=mid).filter(seriesId=sid)

        for rec in all_rec:
            dict1 = {
                'user': rec.userName, 'bat1name': getPlayerName(rec.player1), 'bat1score': rec.bat1,
                'bat2name': getPlayerName(rec.player2), 'bat2score': rec.bat2,
                'bowl1name': getPlayerName(rec.player3), 'bowl1score': rec.bowl1,
                'bowl2name': getPlayerName(rec.player4), 'bowl2score': rec.bowl2,
                'allname': getPlayerName(rec.player5), 'allscore': rec.allround, 'total': rec.total, 'point': rec.point
            }
            lst.append(dict1)
            sort_list = sorted(lst, key=lambda i: i['total'], reverse=True)

        return sort_list

    except Exception as e:
        print(str(e))
        return sort_list


def getAllMatch(matches, i_parm):

    score_status = Envariable().scorestatus
    match_list = list()
    match_id_list = list()
    lst = list()

    if i_parm == 'past':
        for i in matches:
            if i.get('state') in score_status:
                # if i.get('state') == 'Result' or i.get('state') == 'Live' or i.get('state') == 'No result'
                # or i.get('state') == 'Scheduled':
                match_list.append(i.get('match_desc'))
                match_id_list.append(i.get('match_id'))

    if i_parm == 'all':
        for i in matches:
            match_list.append(i.get('match_desc'))
            match_id_list.append(i.get('match_id'))

    for match, match_id in zip(match_list, match_id_list):
        lst.append((match_id, match))
    return lst

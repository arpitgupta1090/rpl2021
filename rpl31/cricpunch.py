import requests
import re
import json
from bs4 import BeautifulSoup


class Series:

    def __init__(self, _series_id=None):
        self._series_url = "https://www.espncricinfo.com/ci/content/match/fixtures_futures.html"
        self._series_id = _series_id

        if not _series_id:
            self.all_series = self._get_series(self._series_url)
        else:
            self._json_url = "http://core.espnuk.org/v2/sports/cricket/leagues/{0}/".format(str(_series_id))
            self._json = self._get_json(self._json_url)

            if self._json:
                self._squad_url = self._squad_url()
                self._squad_url_fix = "https://www.espncricinfo.com/ci/content/squad/index.html?object={0}" \
                    .format(str(self._series_id))
                self.name = {"name": self._json['name']}
                self._url = self._json['links'][0]['href']
                self._fix_url = self._fix_url()
                self.matches = self._get_matches()
                self.players = self._get_players()

            else:
                self.name = "DATA NA"
                self.matches = "DATA NA"
                self.players = "DATA NA"

    @staticmethod
    def _get_json(_url):
        r = requests.get(_url)

        if r.status_code == 404:
            print("URL not found")
        else:
            return r.json()

    @staticmethod
    def _get_series(_url):

        lst = []
        print("Please fetch series-id from below urls")
        r = requests.get(_url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'fixfutures'})

            for row in table.find_all('li'):
                lst.append(row.a['href'])

        else:
            print("Series data NA")
        return lst

    def _get_matches(self):

        r = requests.get(self._fix_url)
        match = []

        if r.status_code == 200:

            soup = BeautifulSoup(r.text, 'html.parser')
            # text = soup.find_all('script')[15].contents[0].split('window.__INITIAL_STATE__ = ',1)[1]
            text2 = str(soup.findAll(text=re.compile('apiUrls'))[0]).split('"apiUrls":{"urls":')[1].split('}', 1)[0]
            url2 = text2.split(',')[0].split('[')[1].replace('"', '')

            req = requests.get(url2)
            soup = BeautifulSoup(req.text, 'lxml')
            text = soup.body.get_text()
            text1 = json.loads(text)['events']
            for event in text1:

                mid = event['competitions'][0]['id']
                match_desc = event['competitions'][0]['description']
                match_status = event['competitions'][0]["status"]["type"]["description"]
                team1 = event['competitions'][0]["competitors"][0]["team"]["shortDisplayName"]
                team2 = event['competitions'][0]["competitors"][1]["team"]["shortDisplayName"]
                match.append({"match_id": mid, "match_desc": match_desc,
                              "state": match_status, "team1": team1, "team2": team2})

        else:
            print("Match data NA at CrinInfo")

        return match

    def _fix_url(self):
        url = ""
        for link in self._json['links']:
            if link["text"] == "Fixtures":
                url = link["href"]
                break
            else:
                url = ""
        return url

    def _squad_url(self):
        url = ""
        for link in self._json['links']:
            if link["text"] == "Squads":
                url = link["href"]
                self._series_id = url.split('=')[1]
                break
            else:
                url = ""
        return url

    def _get_players(self):
        match = []
        lst = []
        r = requests.get(self._squad_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('ul', attrs={'class': 'squads_list'})
        if table is None:
            r = requests.get(self._squad_url_fix)
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find('ul', attrs={'class': 'squads_list'})
        for row in table.findAll('a', href=True):
            link = "https://www.espncricinfo.com" + row['href']
            match.append(link)
        for url2 in match:
            lst.append(self._get_players_from_url(url2))
        return lst

    @staticmethod
    def _get_players_from_url(url2):
        player_list = []

        r = requests.get(url2)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'content main-section'})
        team_table = table.find('div', attrs={'class': 'large-14 medium-20 columns home squads_main main-container'})
        team = team_table.h1.text

        for row in table.findAll('div', attrs={'class': 'large-7 medium-7 small-7 columns'}):
            pid = row.a['href'].split('/')[4].split('.')[0]
            player_name = row.img['title']
            player_dict = dict()
            player_dict['player_name'] = player_name
            player_dict['player_id'] = pid
            player_dict['player_team'] = team
            player_list.append(player_dict)

        for row in table.findAll('div', attrs={'class': 'large-13 medium-13 small-20 columns'}):
            pid = row.a['href'].split('/')[4].split('.')[0]
            player_name = re.sub('\s+', ' ', row.a.text).strip()
            player_dict = dict()
            player_dict['player_name'] = player_name
            player_dict['player_id'] = pid
            player_dict['player_team'] = team
            player_list.append(player_dict)
        return player_list


class Match:

    na_text = "Data not available at the source"

    def __init__(self, match_id):
        self.match_id = match_id
        self._match_url = "https://www.espncricinfo.com/matches/engine/match/{0}.html".format(str(match_id))
        self._json_url = "https://www.espncricinfo.com/matches/engine/match/{0}.json".format(str(match_id))
        self._json = self._get_json()

        if self._json:
            self.status = self._status()
            self.description = self._description()
            self._series = self._series()
            self.series_name = self._series_name()
            self.series_id = self._series_id()
            self.squads = self._squads()
            self.score = self._match_score()
            self.title = self._match_title()
            self.espn = self._espn()
            if not self.score[0]:
                self.score = self._espn()

        else:
            self.status = self.na_text
            self.description = self.na_text
            self.series = self.na_text
            self.series_name = self.na_text
            self.series_id = self.na_text
            self.squads = self.na_text
            self.score = self.na_text
            self.title = self.na_text

    def __str__(self):
        return self.match_id

    def _get_json(self):
        r = requests.get(self._json_url)
        if r.status_code == 404:
            print("MatchNotFoundError")
        elif 'Scorecard not yet available' in r.text:
            print("NoScorecardError")
        else:
            return r.json()

    def _match_json(self):
        return self._json['match']

    def _match_title(self):
        return self._match_json()['cms_match_title']

    def _status(self):
        return self._match_json()['match_status']

    def _description(self):
        return self._json['description']

    def _series(self):
        return self._json['series']

    def _series_name(self):
        try:
            return self._json['series'][-1]['series_name']
        except Exception as e:
            print(str(e))
            return "Series name NA"

    def _series_id(self):
        return self._json['series'][-1]['core_recreation_id']

    def _squads(self):
        lst = []
        lst2 = []
        url1 = self._match_url
        r = requests.get(url1)
        soup = BeautifulSoup(r.text, 'html.parser')
        tag_data = soup.find('script', text=re.compile('props'))
        text = tag_data.contents[0]
        data1 = json.loads(text)
        url2 = data1["props"]["pageProps"]["seo"]["canonical"].replace('/game/', '/scorecard/')
        req = requests.get(url2)
        soup2 = BeautifulSoup(req.text, 'html.parser')
        tag_data2 = soup2.find('script', text=re.compile('props'))
        data2 = None
        if tag_data2:
            text2 = tag_data2.contents[0]
            if text2:
                data2 = json.loads(text2)["props"]["pageProps"]["data"]["pageData"]["content"]["matchPlayers"]

        if data2:
            data3 = data2.get("teamPlayers")
            if data3:
                for team in data3:
                    b1 = team.get("players")
                    lst += b1

                for players in lst:
                    player = players.get("player")
                    lst2.append({"player_id": player.get("objectId"), "player_name": player.get("longName")})

            else:
                lst2 = []
                print("player list NA at CricInfo")
        else:
            lst2 = []
            print("player list NA at CricInfo")

        return lst2

    def _espn(self):
        url1 = "https://www.espn.in/cricket/series/{0}/game/{1}/".format(self.series_id, self.match_id)
        r = requests.get(url1)
        soup = BeautifulSoup(r.text, 'html.parser')
        tag_data = soup.find('script', text=re.compile('__INITIAL_STATE__'))
        if tag_data:
            text = tag_data.contents[0].splitlines()[2].split("=", 1)[1][:-1]
            if text:
                text1 = json.loads(text)["gamePackage"]["scorecard"]["innings"]

                if text1.get("1"):
                    innings_1_batsmen = text1.get("1").get("batsmen")
                    innings_1_bowlers = text1.get("1").get("bowlers")
                else:
                    innings_1_batsmen = []
                    innings_1_bowlers = []

                if text1.get("2"):
                    innings_2_batsmen = text1.get("2").get("batsmen")
                    innings_2_bowlers = text1.get("2").get("bowlers")
                else:
                    innings_2_batsmen = []
                    innings_2_bowlers = []

                batsmen = innings_1_batsmen + innings_2_batsmen
                bowlers = innings_1_bowlers + innings_2_bowlers

                bat_dict = dict()
                for batsman in batsmen:
                    player_id = int(batsman.get("href").split(".")[-2].split("/")[-1])
                    stats = batsman.get("stats")

                    dict2 = dict()
                    for data in stats:
                        if data.get("name") == "runs":
                            dict2["runs"] = int(data.get("value"))
                        if data.get("name") == "fours":
                            dict2["fours"] = int(data.get("value"))
                        if data.get("name") == "sixes":
                            dict2["sixes"] = int(data.get("value"))
                    bat_dict[player_id] = dict2

                bowl_dict = dict()
                for bowler in bowlers:
                    player_id = int(bowler.get("href").split(".")[-2].split("/")[-1])
                    stats = bowler.get("stats")

                    dict2 = dict()
                    for data in stats:
                        if data.get("name") == "economyRate":
                            dict2["economyRate"] = float(data.get("value"))
                        if data.get("name") == "maidens":
                            dict2["maidens"] = int(data.get("value"))
                        if data.get("name") == "wickets":
                            dict2["wickets"] = int(data.get("value"))
                        if data.get("name") == "overs":
                            dict2["overs"] = float(data.get("value"))
                    bowl_dict[player_id] = dict2

            else:
                bat_dict = []
                bowl_dict = []

        else:
            bat_dict = []
            bowl_dict = []

        return bat_dict, bowl_dict

    def _match_score(self):
        bat_list = []
        bowl_list = []
        bat_dict = {}
        bowl_dict = {}
        url1 = self._match_url
        r = requests.get(url1)
        soup = BeautifulSoup(r.text, 'html.parser')
        tag_data = soup.find('script', text=re.compile('props'))
        text = tag_data.contents[0]
        data1 = json.loads(text)
        url2 = data1["props"]["pageProps"]["seo"]["canonical"]

        req = requests.get(url2)
        soup2 = BeautifulSoup(req.text, 'html.parser')
        tag_data2 = soup2.find('script', text=re.compile('props'))
        data2 = None
        if tag_data2:
            text2 = tag_data2.contents[0]

            # with open("temp1.json", "w") as w_file:
            #     temptext = json.dumps(json.loads(text2), indent=4)
            #     w_file.write(temptext)

            if text2:
                data2 = json.loads(text2)["props"]["pageProps"]["data"]["pageData"]["content"].get("scorecard")

        if data2:
            data3 = data2.get("innings")
            if data3:
                for inning in data3:
                    b1 = inning.get("inningBatsmen")
                    b2 = inning.get("inningBowlers")
                    bat_list += b1
                    bowl_list += b2

                for bat in bat_list:
                    batsman_id = bat["player"]["objectId"]
                    bat_dict[batsman_id] = {
                        'runs': bat.get('runs'), 'fours': bat.get('fours'),
                        'sixes': bat.get('sixes')}

                for bowl in bowl_list:
                    bowler_id = bowl["player"]["objectId"]
                    bowl_dict[bowler_id] = {'economyRate': bowl.get('economy'), 'maidens': bowl.get('maidens'),
                                            'wickets': bowl.get('wickets'), 'overs': bowl.get('overs')}

            else:

                bat_dict = []
                bowl_dict = []
                print("ScoreCard NA at source")

        else:
            bat_dict = []
            bowl_dict = []
            print("ScoreCard NA at source")

        return bat_dict, bowl_dict


def main():

    se = Series()
    print(se.all_series)

    s = Series(1249214)
    print(s.name)
    print(s.matches)
    print(s.players)

    m = Match(1254060)
    print(m.description)
    print(m.status)
    print(m.series_id)
    print(m.match_id)
    print(m.series_name)
    print(m.title)
    print(m.squads)
    print(m.score)
    #print(m.espn)


if __name__ == "__main__":
    main()

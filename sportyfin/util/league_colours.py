NBA = "nba"
NHL = "nhl"
NFL = "nfl"
EF = "English Football"


class LeagueColours:
    def __init__(self, lg: str):
        self.league = lg
        self.colours = {
            NBA: {
                "Atlanta Hawks": [(225, 68, 52), (196, 214, 0), (38, 40, 42)],
                "Boston Celtics": [(0, 122, 51), (139, 111, 78), (150, 56, 33), (255, 255, 255), (0, 0, 0)],
                "Brooklyn Nets": [(0, 0, 0), (255, 255, 255)],
                "Charlotte Hornets": [(29, 17, 96), (0, 120, 140), (161, 161, 164)],
                "Chicago Bulls": [(206, 17, 65), (6, 25, 34)],
                "Cleveland Cavaliers": [(134, 0, 56), (4, 30, 66), (253, 187, 48), (0, 0, 0)],
                "Dallas Mavericks": [(0, 83, 188), (0, 43, 92), (187, 196, 202), (6, 25, 34)],
                "Denver Nuggets": [(13, 34, 64), (255, 198, 39), (139, 35, 50), (29, 66, 138)],
                "Detroit Pistons": [(200, 16, 46), (29, 66, 138), (181, 179, 179), (0, 45, 98)],
                "Golden State Warriors": [(29, 66, 138), (255, 199, 44)],
                "Houston Rockets": [(206, 17, 65), (6, 25, 34), (196, 206, 211)],
                "Indiana Pacers": [(0, 45, 98), (253, 187, 48), (190, 192, 194)],
                "Los Angeles Clippers": [(200, 16, 46), (29, 66, 148), (190, 192, 194), (0, 0, 0)],
                "Los Angeles Lakers": [(85, 37, 130), (253, 185, 39), (6, 25, 34)],
                "Memphis Grizzlies": [(93, 118, 169), (18, 23, 63), (255, 187, 34), (112, 114, 113)],
                "Miami Heat": [(152, 0, 46), (249, 160, 27), (6, 25, 34)],
                "Milwaukee Bucks": [(0, 71, 27), (240, 235, 210), (0, 125, 197), (6, 25, 34)],
                "Minnesota Timberwolves": [(12, 35, 64), (35, 97, 146), (158, 162, 162), (120, 190, 32)],
                "New Orleans Pelicans": [(0, 22, 65), (225, 58, 62), (180, 151, 90)],
                "New York Knicks": [(0, 107, 182), (245, 132, 38), (190, 192, 194), (35, 31, 32)],
                "Oklahoma City Thunder": [(0, 125, 195), (239, 59, 36), (0, 45, 98), (253, 187, 48)],
                "Orlando Magic": [(0, 125, 197), (196, 206, 211), (6, 25, 34)],
                "Philadelphia 76ers": [(0, 107, 182), (237, 23, 76), (0, 43, 92), (196, 206, 211)],
                "Phoenix Suns": [(29, 17, 96), (229, 95, 32), (6, 25, 34), (99, 113, 122), (249, 160, 27)],
                "Portland Trail Blazers": [(224, 58, 62), (6, 25, 34)],
                "Sacramento Kings": [(91, 43, 130), (99, 113, 122), (6, 25, 34)],
                "SanAntonio Spurs": [(196, 206, 211), (6, 25, 34)],
                "Toronto Raptors": [(206, 17, 65), (6, 25, 34), (161, 161, 164), (180, 151, 90)],
                "Utah Jazz": [(0, 43, 92), (0, 71, 27), (249, 160, 27)],
                "Washington Wizards Navy": [(0, 43, 92), (227, 24, 55), (196, 206, 212)]
            },
            NFL: {
                "Baltimore Ravens": [(26, 25, 95), (0, 0, 0), (158, 124, 12), (198, 12, 14)],
                "Cincinnati Bengals": [(251, 79, 20), (0, 0, 0)],
                "Cleveland Browns": [(49, 29, 0), (255, 60, 0)],
                "Pittsburgh Steelers": [(255, 182, 18), (16, 24, 32), (0, 48, 135), (198, 12, 48),(165, 172, 175)],
                "Buffalo Bills": [(0, 51, 141), (198, 12, 48)],
                "Miami Dolphins": [(0, 142, 151), (252, 76, 2), (0, 87, 120)],
                "New England Patriots": [(0, 34, 68), (198, 12, 48), (176, 183, 188)],
                "New York Jets": [(18, 87, 64), (0, 0, 0), (255, 255, 255)],
                "Houston Texans": [(3, 32, 47), (167, 25, 48)],
                "Indianapolis Colts": [(0, 44, 95), (162, 170, 173)],
                "Jacksonville Jaguars": [(16, 24, 32), (215, 162, 42), (159, 121, 44), (0, 103, 120)],
                "Tennessee Titans": [(12, 35, 64), (75, 146, 219), (200, 16, 46), (138, 141, 143)],
                "Denver Broncos": [(251, 79, 20), (0, 34, 68)],
                "Kansas City Chiefs": [(227, 24, 55), (255, 184, 28)],
                "Las Vegas Raiders": [(0, 0, 0), (165, 172, 175)],
                "Los Angeles Chargers": [(0, 128, 198), (255, 194, 14), (255, 255, 255)],
                "Chicago Bears": [(11, 22, 42), (200, 56, 3)],
                "Detroit Lions": [(0, 118, 182) , (176, 183, 188), (0, 0, 0), (255, 255, 255)],
                "Green Bay Packers": [(24, 48, 40), (255, 184, 28)],
                "Minnesota Vikings": [(79, 38, 131), (255, 198, 47)],
                "Dallas Cowboys": [(0, 53, 148), (0, 34, 68), (134, 147, 151), (127, 150, 149), (255, 255, 255)],
                "New York Giants": [(1, 35, 82), (163, 13, 45), (155, 161, 162)],
                "Philadelphia Eagles": [(0, 76, 84), (165, 172, 175), (186, 202, 211), (0, 0, 0), (95, 96, 98)],
                "Washington Football Team": [(63, 16, 16), (255, 182, 18)],
                "Atlanta Falcons": [(167, 25, 48), (0, 0, 0), (165, 172, 175)],
                "Carolina Panthers": [(0, 133, 202), (16, 24, 32), (191, 192, 191)],
                "New Orleans Saints": [(211, 188, 141), (16, 24, 31)],
                "Tampa Bay Buccaneers": [(213, 10, 10), (255, 121, 0), (10, 10, 8), (177, 186, 191), (52, 48, 43)],
                "Arizona Cardinals": [(151, 35, 63), (0, 0, 0), (255, 182, 18)],
                "Los Angeles Rams": [(0, 53, 148), (255, 163, 0), (255, 130, 0), (255, 209, 0), (255, 255, 255)],
                "San Francisco 49ers": [(170, 0, 0), (173, 153, 93)],
                "Seattle Seahawks": [(0, 34, 68), (105, 190, 40), (165, 172, 175)]
                },
            NHL: {
                "Anaheim Ducks": [(252, 76, 2), (185, 151, 91), (193, 198, 200)],
                "Arizona Coyotes": [(140, 38, 51), (226, 214, 181)],
                "Boston Bruins": [(252, 181, 20), (17, 17, 17)],
                "Buffalo Sabres": [(0, 38, 84), (252, 181, 20)],
                "Calgary Flames": [(200, 16, 46), (241, 190, 72)],
                "Carolina Hurricanes": [(226, 24, 54), (35, 31, 32)],
                "Chicago Blackhawks": [(207, 10, 44), (255, 103, 27)],
                "Colorado Avalanche": [(111, 38, 61), (35, 97, 146)],
                "Columbus Blue Jackets": [(0, 38, 84), (206, 17, 38)],
                "Dallas Stars": [(0, 104, 71), (143, 143, 140)],
                "Detroit Red Wings": [(206, 17, 38), (255, 255, 255)],
                "Edmonton Oilers": [(4, 30, 66), (252, 76, 0)],
                "Florida Panthers": [(4, 30, 66), (200, 16, 46)],
                "Los Angeles Kings": [(17, 17, 17), (162, 170, 173)],
                "Minnesota Wild": [(175, 35, 36), (2, 73, 48)],
                "Montreal Canadiens": [(175, 30, 45), (25, 33, 104)],
                "Nashville Predators": [(255, 184, 28), (4, 30, 66)],
                "New Jersey Devils": [(206, 17, 38), (0, 0, 0)],
                "New York Islanders": [(0, 83, 155), (244, 125, 48)],
                "New York Rangers": [(0, 56, 168), (206, 17, 38)],
                "Ottawa Senators": [(197, 32, 50), (194, 145, 44)],
                "Philadelphia Flyers": [(247, 73, 2), (0, 0, 0)],
                "Pittsburgh Penguins": [(0, 0, 0), (207, 196, 147)],
                "St. Louis Blues": [(0, 47, 135), (252, 181, 20)],
                "San Jose Sharks": [(0, 109, 117), (234, 114, 0)],
                "Seattle Kraken": [(0, 22, 40), (153, 217, 217)],
                "Tampa Bay Lightning": [(0, 40, 104), (255, 255, 255)],
                "Toronto Maple Leafs": [(0, 32, 91), (255, 255, 255)],
                "Vancouver Canucks": [(0, 32, 91), (10, 134, 61)],
                "Vegas Golden Knights": [(185, 151, 91), (51, 63, 72)],
                "Washington Capitals": [(4, 30, 66), (200, 16, 46)],
                "Winnipeg Jets": [(4, 30, 66), (0, 76, 151)]
            },
            EF: {
                "Arsenal": [(239, 1, 7), (219, 0, 7)],
                "Aston Villa FC": [(149, 191, 229), (103, 14, 54)],
                "AFC Bournemouth": [(218, 41, 28), (181, 14, 18)],
                "Brighton & Hove Albion": [(0, 87, 184), (255, 205, 0)],
                "Burnley Football Club": [(108, 29, 69), (153, 214, 234)],
                "Chelsea FC": [(3, 70, 148), (238, 36, 44)],
                "Crystal Palace FC": [(27, 69, 143), (167, 165, 166)],
                "Everton FC": [(39, 68, 136), (255, 255, 255)],
                "Leicester City Football Club": [(0, 83, 160), (253, 190, 17)],
                "Liverpool FC": [(200, 16, 46), (0, 178, 169)],
                "Manchester City FC": [(108, 171, 221), (28, 44, 91)],
                "Manchester United": [(218, 41, 28), (251, 225, 34)],
                "Newcastle United FC": [(45, 41, 38), (255, 255, 255)],
                "Norwich City": [(255, 242, 0), (0, 166, 80)],
                "Sheffield United": [(238, 39, 55), (13, 23, 26)],
                "Southampton FC": [(215, 25, 32), (19, 12, 14)],
                "Tottenham Hotspur": [(19, 34, 87)],
                "Watford FC": [(251, 238, 35), (237, 33, 39)],
                "West Ham United": [(122, 38, 58), (27, 177, 231)],
                "Wolverhampton Wanderers": [(253, 185, 19), (35, 31, 32)],
                "Cardiff City": [(0, 112, 181), (209, 21, 36)],
                "Fulham FC": [(204, 0, 0), (0, 0, 0)],
                "Huddersfield Town": [(14, 99, 173), (255, 255, 255)],
                "Leeds United Football Club": [(255, 205, 0), (29, 66, 138)],
                "Stoke City FC": [(224, 58, 62), (27, 68, 156)],
                "Swansea City AFC": [(18, 18, 18)],
                "West Bromwich Albion": [(18, 47, 103), (255, 255, 255)],
            }

        }

    def get_helper(self, tn: str, pos: int):
        t = self.colours.get(self.league, None).get(tn, None)
        if t:
            for i in range(pos):
                try:
                    return t[pos - i - 1]
                except:
                    pass
        return None

    def get_second(self, n: str):
        t = self.get_helper(n, 2)
        if not t:
            n_s = n.split()
            for n_p in reversed(n_s):
                for team_name in self.colours[self.league].keys():
                    if n_p in team_name:
                        t = self.get_helper(n, 2)
            if not t:
                t = (0, 0, 0)
        return t

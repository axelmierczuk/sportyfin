NBA = "nba"
NHL = "nhl"
NFL = "nfl"

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
                "Washington WizardsNavy": [(0, 43, 92), (227, 24, 55), (196, 206, 212)]
            },
            NFL: {},
            NHL: {}
        }

    def get_helper(self, tn: str, pos: int) -> tuple[int, int, int]:
        t = self.colours.get(self.league, None).get(tn, None)
        if t:
            for i in range(pos):
                try:
                    return t[pos - i - 1]
                except:
                    pass
        return None

    def get_second(self, n: str) -> tuple[int, int, int]:
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

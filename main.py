import logging
import sys
import requests as r
import regex as re
from game_info import get_game_info


try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


NBA = "nba"
NHL = "nhl"
NFL = "nfl"


# Helper Functions
def find_urls(s: str) -> list[str]:
    soup = BeautifulSoup(s, 'html.parser')
    pretty = soup.prettify()
    for line in pretty.splitlines():
        if "m3u8" in line:
            print(line)


def check_m3u8_url(s: str) -> str:
    if '.m3u8' in s:
        print(s)
        index = s.find('"')
        if index != -1:
            print(s[:index])
            return s[:index]
        return s
    return None


def bypass_bitly(link: str) -> str:
    parsed_html = BeautifulSoup(r.request("GET", link).text, features="lxml")
    try:
        return parsed_html.body.find('a', attrs={'id': 'skip-btn'}).get('href')
    except Exception:
        return ""


def get_m3u8(link: str) -> str:
    if not link:
        return None
    try:
        res = r.request("GET", link)
        if res.status_code == 200:
            urls = find_urls(res.content)
            for u in urls:
                print(u)
                if 'm3u8' in str(u):
                    print(u)
                return check_m3u8_url(u)
    except Exception:
        return None
    return None


def pull_bitly_link(link) -> str:
    parsed_html_next = BeautifulSoup(r.request("GET", link).text, features="lxml")
    try:
        for tag in parsed_html_next.body.find_all('tr'):
            return tag.get('data-stream-link')
    except Exception:
        print(f"[-] Error getting bitly link from {link}.")


def find_streams(lg: str):
    res = []
    if lg == NBA:
        print("Collecting NBA streaming links.")
        games = []
        parsed_html = BeautifulSoup(r.request("GET", "https://reddit.rnbastreams.com/").text, features="lxml")
        for tag in parsed_html.body.find_all('a', attrs={'href': re.compile('/game/.*')}):
            if len(tag.find_all('span', string="Full time ")) == 0 and len(tag.find_all('i', attrs={"class": "icon-clock"})) == 0:
                match = get_game_info(tag)
                print(match)
                games.append(f"https://sportscentral.io/streams-table/{tag.get('href')[-6:]}/basketball?new-ui=1&origin=reddit.rnbastreams.com")
        for link in games:
            stream_link = pull_bitly_link(link)
            if not (not stream_link or stream_link in res):
                res.append(stream_link)
        print(res)
        return res
    elif lg == NHL:
        return []
    elif lg == NFL:
        return []


# Main class
class StreamCollector:
    def __init__(self):
        self.streaming_sites = {
            NBA: find_streams(NBA),
            NHL: find_streams(NHL),
            NFL: find_streams(NFL)
        }
        self.leagues: list[str] = leagues

    def collect(self) -> list[str]:
        lm3u: list[str] = []
        for lg in self.leagues:
            print(f"Collecting {lg.upper()} m3u8 links.")
            lm3u.extend(self.get_streams(lg))
        return lm3u

    def get_streams(self, lg: str) -> list[str]:
        res: list[str] = []
        for link in self.streaming_sites[lg]:
            m3u_link = get_m3u8(bypass_bitly(link))
            if m3u_link:
                res.append(m3u_link)
        return res


def main() -> list[str]:
    collector = StreamCollector()
    collector.collect()


if __name__ == "__main__":
    leagues = []
    verbosity = False
    for i in sys.argv:
        if str(i) == "-v":
            verbosity = True
        if str(i).startswith("-n"):
            i = str(i)[2:]
            for c in i:
                if c == "b" and NBA not in leagues:
                    leagues.append(NBA)
                if c == "h" and NHL not in leagues:
                    leagues.append(NHL)
                if c == "f" and NFL not in leagues:
                    leagues.append(NFL)
    try:
        main()
    except Exception as e:
        logging.error("Unexpected error.")
        if verbosity:
            print(e.with_traceback())
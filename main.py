import logging
import numpy as np
import PIL
import sys
import requests as r
import regex as re
import os
import urllib.request
from PIL import Image

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# Enums
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

def generate_img(m, sport: str) -> str:
    ht = m['home_team']
    at = m['away_team']
    location = str(hash(ht['name']+at['name']))
    if not os.path.isfile(f"output/{sport}/{location}.jpg"):
        if not os.path.isdir(f"output/{sport}"):
            os.makedirs(f"output/{sport}")

        list_im = []

        # Download HT icon
        ht_loc = f"output/{location}/{str(hash(ht['name']))}.jpg"
        if not os.path.isfile(ht_loc):
            res = urllib.request.urlretrieve(ht['icon_url'], ht_loc)
            if res:
                list_im.append(ht_loc)
        else:
            list_im.append(ht_loc)

        # Download AT icon
        at_loc = f"output/{location}/{str(hash(at['name']))}.jpg"
        if not os.path.isfile(at_loc):
            res = urllib.request.urlretrieve(at['icon_url'], at_loc)
            if res:
                list_im.append(at_loc)
        else:
            list_im.append(at_loc)

        if len(list_im > 1):
            imgs = [PIL.Image.open(i) for i in list_im]
            min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
            imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
            imgs_comb = PIL.Image.fromarray(imgs_comb)
            imgs_comb.save(f"output/{sport}/{location}.jpg")
        else:
            # Move file and return hashed filename
            if len(list_im) == 0:
                return ""
            else:
                return list_im[0]
    return f"output/{sport}/{location}.jpg"

def get_game_info(tag):
    home_team_tags = tag.find('span', attrs={'class': "logo home-team competition-cell-table-cell"}).find_all('img')
    away_team_tags = tag.find('span', attrs={'class': "competition-cell-table-cell competition-cell-side2"}).find_all(
        'img')
    for h in home_team_tags:
        if len(h.get("alt")) > 0:
            h_img = h
            break
    for a in away_team_tags:
        if len(a.get("alt")) > 0:
            a_img = a
            break
    match = {
        "home_team": {
            "name": str(h_img.get('alt')),
            "icon_url": str(h_img.get('src') if str(h_img.get('src')).find('?') == -1 else str(h_img.get('src'))[
                                                                                           :str(h_img.get('src')).find(
                                                                                               '?')])
        },
        "away_team": {
            "name": str(a_img.get('alt')),
            "icon_url": str(a_img.get('src') if str(a_img.get('src')).find('?') == -1 else str(a_img.get('src'))[
                                                                                           :str(a_img.get('src')).find(
                                                                                               '?')])
        },
        "match": {
        }
    }
    match['match']['name'] = f"{match['away_team']['name']} at {match['home_team']['name']}"
    match['match']['img_location'] = generate_img(match, NBA)
    return match

def find_streams(lg: str):
    res = []
    if lg == NBA:
        print("Collecting NBA streaming links.")
        games = []
        parsed_html = BeautifulSoup(r.request("GET", "https://reddit.rnbastreams.com/").text, features="lxml")
        for tag in parsed_html.body.find_all('a', attrs={'href': re.compile('/game/.*')}):
            if len(tag.find_all('span', string="Full time ")) == 0 and len(tag.find_all('i', attrs={"class": "icon-clock"})) == 0:
                # GET INFO
                try:
                    match = get_game_info(tag)
                except Exception as e:
                    print("[-] Error getting team information.")
                    print(e)
                games.append(f"https://sportscentral.io/streams-table/{tag.get('href')[-6:]}/basketball?new-ui=1&origin=reddit.rnbastreams.com")
        for link in games:
            parsed_html_next = BeautifulSoup(r.request("GET", link).text, features="lxml")
            try:
                for tag in parsed_html_next.body.find_all('tr'):
                    stream_link = tag.get('data-stream-link')
                    if not (not stream_link or stream_link in res):
                        res.append(stream_link)
            except Exception:
                pass
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
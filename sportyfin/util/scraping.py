import time
import requests as r
import regex as re
import datetime
import json
import sys
from . import game_info
from .pretty_print import *
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv
import os

load_dotenv()

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

NBA = "nba"
NHL = "nhl"
NFL = "nfl"
EF = "English Football"


def flatten_json(y: dict) -> dict:
    """
    Function capable of flattening an object.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            ix = 0
            for a in x:
                flatten(a, name + str(ix) + '_')
                ix += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out


# Helper Functions
def selenium_find(link: str) -> list:
    """
    Looks for possible m3u8 links in network traffic from a streaming site.
    """
    pind(f"Trying to find m3u8 in network traffic - {link}", colours.OKCYAN, otype.DEBUG)
    res = []
    try:
        try:

            caps = DesiredCapabilities.CHROME
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
        except Exception as e:
            print(e.with_traceback())
        driver.get(link)
        time.sleep(1)  # wait for all the data to arrive.
        perf = driver.get_log('performance')
        for j in perf:
            try:
                if "m3u8" in json.dumps(j):
                    obj = flatten_json(json.loads(j["message"]))
                    list_of_dict_values = list(obj.values())
                    for value in list_of_dict_values:
                        if str(value).find("m3u8") > -1 and str(value) not in res:
                            if int(r.get(value, allow_redirects=True).status_code) == 200:
                                pind2(f"Found a stream - {str(value)}", colours.OKGREEN, otype.REGULAR)
                            res.append(value)
            except KeyboardInterrupt:
                sys.exit()
                pass
            except Exception as e:
                p("Something went wrong pulling a m3u8 link", colours.FAIL, otype.ERROR, e)
                continue
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        print(e.with_traceback())
        p("Something went wrong with Selenium", colours.FAIL, otype.ERROR, e)
    return list(dict.fromkeys(res))


def html_find(link: str) -> list:
    """
    Looks for possible m3u8 links in html traffic from a streaming site.
    """
    pind(f"Trying to find m3u8 in page content - {link}", colours.OKCYAN, otype.DEBUG)
    res = []
    try:
        content = r.get(link).text
        for match in re.findall(r"([\'][^\'\"]+(\.m3u8)[^\'\"]*[\'])|([\"][^\'\"]+(\.m3u8)[^\'\"]*[\"])", content):
            for i in match:
                if (i.count("\'") == 2 and i.count("\"") == 0) or (i.count("\"") == 2 and i.count("\'") == 0) and ".m3u8" in i and i[1:-1] not in res:
                    if int(r.get(i[1:-1], allow_redirects=True).status_code) == 200:
                        res.append(i[1:-1])
                        pind2(f"Found a stream - {str(i[1:-1])}", colours.OKGREEN, otype.REGULAR)
    except Exception as e:
        pass
    return res


def find_urls(ll: list) -> list:
    """
    Helper function used to scrape html and network traffic from a provided link.
    """
    res = []
    if len(ll) == 0:
        return res
    try:
        for link in ll:
            if os.environ.get('selenium') == "0":
                res.extend(x for x in selenium_find(link) if x not in res)
            res.extend(x for x in html_find(link) if x not in res)
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        return list(dict.fromkeys(res))
    if len(res) == 0:
        p(f"Did not find streams", colours.FAIL, otype.DEBUG)
    return list(dict.fromkeys(res))


def bypass_bitly(ll: list) -> list:
    """
    Ability to bypass bitly pages to get streaming site url.
    """
    res = []
    for link in ll:
        parsed_html = BeautifulSoup(r.request("GET", link).text, features="lxml")
        try:
            url = parsed_html.body.find('a', attrs={'id': 'skip-btn'}).get('href')
            if url:
                res.append(url)
        except KeyboardInterrupt:
            sys.exit()
            pass
        except Exception as e:
            p(f"Error occurred bypassing bitly - {link}", colours.FAIL, otype.ERROR)
            pass
    return list(dict.fromkeys(res))


def pull_bitly_link(link) -> list:
    """
    Pull bitly link from main streaming site.
    """
    parsed_html_next = BeautifulSoup(r.request("GET", link).text, features="lxml")
    res = []
    try:
        for tag in parsed_html_next.body.find_all('tr'):
            if tag.get('data-stream-link'):
                res.append(tag.get('data-stream-link'))
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        p(f"Error getting stream link from {link}", colours.FAIL, otype.DEBUG)
        return res
    return res


def make_match(api_res, hosts, lg) -> list:
    games = []
    for g in api_res:
        ht = g['homeTeam']
        at = g['awayTeam']
        if lg == EF:
            host_id = str(g['eventLink'].split('/')[-1]).split("?")[0]
        else:
            host_id = str(g['eventLink']).split('/')[-1]
        match = {
            "home_team": {
                "name": ht['name'],
                "icon_url": ht['logo']
            },
            "away_team": {
                "name": at['name'],
                "icon_url": at['logo']
            },
            "match": {
                "name": g.get('name', ''),
                "img_location": "",
                "url": f"{hosts[0]}{host_id}{hosts[1]}"
            }
        }
        if match['match']['name'] == '':
            match['match']['name'] = f"{match['away_team']['name']} vs {match['home_team']['name']}"
        match['match']['img_location'] = game_info.generate_img(match, lg)
        p(f"Found - {match['match']['name']}", colours.OKGREEN, otype.REGULAR)
        pind2(f"URL - {match['match']['url']}", colours.OKCYAN, otype.DEBUG)
        pind2(f"ICON - {match['match']['img_location']}", colours.OKCYAN, otype.DEBUG)
        games.append(match)
    return games


def find_streams(lg: str) -> list:
    """
    Finds current games that are active for a given league.
    """
    STREAM_LINK = os.environ.get('stream_link')
    p(f"COLLECTING {lg.upper()} STREAMING LINKS", colours.HEADER, otype.REGULAR)
    res = []
    games = []
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    hosts = [f"{STREAM_LINK}/streams-table/"]
    path = None
    if lg == NHL:
        path = "nhl-tournaments"
        hosts.append("/ice-hockey?new-ui=1&origin=live.redditnhlstreams.com")
    elif lg == NFL:
        path = "nfl-tournaments-week"
        hosts.append("/american-football?new-ui=1&origin=official.nflstreams.to")
    elif lg == NBA:
        path = "nba-tournaments"
        hosts.append("/basketball?new-ui=1&origin=reddit.rnbastreams.com")
    elif lg == EF:
        hosts.append("/soccer?new-ui=1&origin=redi1.soccerstreams.net")
        api_res = json.loads(r.get(f"{STREAM_LINK}/new-api/matches?timeZone=300&date={date}").content)
        for i in api_res:
            if i['country']['name'] == "England":
                games.extend(make_match(i['events'], hosts, lg))

    if path:
        main_link = f"{STREAM_LINK}/api/{path}?date={date}"
        api_res = json.loads(r.request("GET", main_link).content)[0]['events']
        games = make_match(api_res, hosts, lg)

    for match in games:
        match['match']['url'] = pull_bitly_link(match['match']['url'])
        if not (len(match['match']['url']) == 0 or match in res):
            res.append(match)
    if len(res) == 0:
        p(f"COULD NOT FIND {lg.upper()} GAMES", colours.FAIL, otype.ERROR)
    return res


def get_streams(s: list) -> list:
    return find_urls(bypass_bitly(s))

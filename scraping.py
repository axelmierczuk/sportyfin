import time
import requests as r
import regex as re
import datetime
import chromedriver_binary
import json
import sys
from pretty_print import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from game_info import get_game_info

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

selenium_enabled = False
NBA = "nba"
NHL = "nhl"
NFL = "nfl"


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
def selenium_find(link: str) -> list[str]:
    """
    Looks for possible m3u8 links in network traffic from a streaming site.
    """
    pind(f"Trying to find m3u8 in network traffic - {link}", colours.OKCYAN, otype.DEBUG)
    res = []
    try:
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        prefs = {"download.default_directory": "/tmp/chrome_downloads/",
                 'profile.default_content_setting_values.automatic_downloads': 1}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
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
                            pind2(f"Found a stream - {str(value)}", colours.OKGREEN, otype.REGULAR)
                            res.append(value)
            except KeyboardInterrupt:
                sys.exit()
                pass
            except Exception as e:
                if verbosity:
                    p(e, colours.FAIL, otype.ERROR)
                    print(e.with_traceback())
                continue
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        if verbosity:
            p(e, colours.FAIL, otype.ERROR)
            print(e.with_traceback())
    return list(dict.fromkeys(res))


def html_find(link: str) -> list[str]:
    """
    Looks for possible m3u8 links in html traffic from a streaming site.
    """
    return []


def find_urls(ll: list[str]) -> list[str]:
    """
    Helper function used to scrape html and network traffic from a provided link.
    """
    res = []
    if len(ll) == 0:
        return res
    try:
        for link in ll:
            if selenium_enabled:
                res = selenium_find(link)
            res.extend(x for x in html_find(link) if x not in res)
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        return list(dict.fromkeys(res))
    if len(res) == 0:
        p(f"Did not find streams", colours.FAIL, otype.DEBUG)
    return list(dict.fromkeys(res))


def bypass_bitly(ll: list[str]) -> list[str]:
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
            print(e.with_traceback())
    return list(dict.fromkeys(res))


def pull_bitly_link(link) -> list[str]:
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


def find_streams(lg: str) -> list[dict]:
    """
    Finds current games that are active for a given league.
    """
    res = []
    p(f"COLLECTING {lg.upper()} STREAMING LINKS", colours.HEADER, otype.REGULAR)
    if lg == NBA:
        games = []
        parsed_html = BeautifulSoup(r.request("GET", "https://reddit.rnbastreams.com/").text, features="lxml")
        parsed_html = parsed_html.find('ul', attrs={'class': 'competitions'})
        for tag in parsed_html.find_all('a', attrs={'href': re.compile('/game/.*')}):
            try:
                game_hour = int(tag.find('span', attrs={"class": "competition-cell-status"}).text[:-3]) - datetime.datetime.now().hour < 2
            except:
                game_hour = False
            if (len(tag.find_all('span', string="Full time ")) == 0 and len(tag.find_all('i', attrs={"class": "icon-clock"})) == 0) or game_hour:
                match = get_game_info(tag, lg)
                match['match']['url'] = f"https://sportscentral.io/streams-table/{tag.get('href')[-6:]}/basketball?new-ui=1&origin=reddit.rnbastreams.com"
                p(f"Found - {match['match']['name']}", colours.OKGREEN, otype.REGULAR)
                pind2(f"URL - {match['match']['url']}", colours.OKCYAN, otype.DEBUG)
                pind2(f"ICON - {match['match']['img_location']}", colours.OKCYAN, otype.DEBUG)
                games.append(match)
        for match in games:
            match['match']['url'] = pull_bitly_link(match['match']['url'])
            if not (len(match['match']['url']) == 0 or match in res):
                res.append(match)
    elif lg == NHL:
        pass
    elif lg == NFL:
        pass
    if len(res) == 0:
        p(f"COULD NOT FIND {lg.upper()} GAMES", colours.FAIL, otype.REGULAR)
    return res


def get_streams(s: list[str]) -> list[str]:
    return find_urls(bypass_bitly(s))
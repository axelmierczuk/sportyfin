import sys
import time
import xml.etree.cElementTree as ET
from .util.pretty_print import *
from .util import scraping
from dotenv import load_dotenv

load_dotenv()

NBA = "nba"
NHL = "nhl"
NFL = "nfl"
EF = "English Football"
leagues = []
OUTPUT = os.path.join(os.getcwd(), "output")
os.environ['output'] = OUTPUT


def header():
    print()
    print()
    print(f"{colours.OKCYAN + colours.BOLD} ________  ________  ________  ________  _________    ___    ___ ________ ___  ________    ")
    print(f"{colours.OKCYAN + colours.BOLD}|\   ____\|\   __  \|\   __  \|\   __  \|\___   ___\ |\  \  /  /|\  _____\\  \|\   ___  \    ")
    print(f"{colours.OKCYAN + colours.BOLD}\ \  \___|\ \  \|\  \ \  \|\  \ \  \|\  \|___ \  \_| \ \  \/  / | \  \__/\ \  \ \  \\ \  \   ")
    print(f"{colours.OKCYAN + colours.BOLD} \ \_____  \ \   ____\ \  \\\  \ \   _  _\   \ \  \   \ \    / / \ \   __\\ \  \ \  \\ \  \  ")
    print(f"{colours.OKCYAN + colours.BOLD}  \|____|\  \ \  \___|\ \  \\\  \ \  \\  \|   \ \  \   \/  /  /   \ \  \_| \ \  \ \  \\ \  \ ")
    print(f"{colours.OKCYAN + colours.BOLD}    ____\_\  \ \__\    \ \_______\ \__\\ _\    \ \__\__/  / /      \ \__\   \ \__\ \__\\ \__\ ")
    print(f"{colours.OKCYAN + colours.BOLD}   |\_________\|__|     \|_______|\|__|\|__|    \|__|\___/ /        \|__|    \|__|\|__| \|__|")
    print(f"{colours.OKCYAN + colours.BOLD}   \|_________|                                     \|___|/                                  ")
    print()
    print(f"{colours.OKGREEN}    Summary: Stream sports events straight from your Jellyfin server. Sportyfin allows users to scrape for ")
    print(f"{colours.OKGREEN}             live streamed events and watch straight from Jellyfin. Sportyfin also generates meta-data that ")
    print(f"{colours.OKGREEN}             is used in Jellyfin to provide a great viewing experience.")
    print()
    print(f"{colours.OKGREEN}    Author: Axel Mierczuk")
    print(f"{colours.OKGREEN}    Version: 1.0.0")
    print(f"{colours.OKGREEN}    Github: https://github.com/axelmierczuk/sportyfin")
    print()
    print()


# Main class
class StreamCollector:
    def __init__(self):
        self.streaming_sites = {
            NBA: scraping.find_streams(NBA) if NBA in leagues else [],
            NHL: scraping.find_streams(NHL) if NHL in leagues else [],
            NFL: scraping.find_streams(NFL) if NFL in leagues else [],
            EF: scraping.find_streams(EF) if EF in leagues else [],
        }
        self.leagues: list = leagues

    def collect(self) -> None:

        for lg in self.leagues:
            p(f"COLLECTING {lg.upper()} .M3U8 LINKS", colours.HEADER, otype.REGULAR)
            res = 0
            for match in self.streaming_sites[lg]:
                p(f"Looking for {match['match']['name']} streams:", colours.WARNING, otype.REGULAR)
                match['match']['m3u8_urls'] = scraping.get_streams(match['match']['url'])
                res += len(match['match']['m3u8_urls'])
            if res == 0:
                p(f"COULD NOT FIND {lg.upper()} M3U8 LINKS", colours.FAIL, otype.REGULAR)

    def generate_xmltv(self, lg: str):
        root = ET.Element("tv")
        for match in self.streaming_sites[lg]:
            for url in match['match']['m3u8_urls']:
                doc = ET.SubElement(root, "channel", id=str(url))
                ET.SubElement(doc, "display-name").text = match['match']['name']
                ET.SubElement(doc, "icon").text = f"{OUTPUT}/{lg}/{match['match']['img_location'].split('/')[-1]}"
        tree = ET.ElementTree(root)
        outp = os.path.join(OUTPUT, f"docs")
        if not os.path.isdir(f"{OUTPUT}"):
            os.makedirs(f"{OUTPUT}")
            os.makedirs(f"{outp}")
        elif not os.path.isdir(f"{outp}"):
            os.makedirs(f"{outp}")
        output_path = os.path.join(outp, f"{lg}.xml")
        tree.write(output_path)

    def generate_m3u(self, lg: str):
        with open(os.path.join(*[OUTPUT, "docs", f"{lg}.m3u"]), 'w') as file:
            file.write(f"""#EXTM3U x-tvg-url="{os.path.join(*[OUTPUT, "docs", f"{lg}.xml"])}"\n""")
            for match in self.streaming_sites[lg]:
                for url in match['match']['m3u8_urls']:
                    file.write(f"""#EXTINF:-1 tvg-id="{url}" tvg-country="USA" tvg-language="English" tvg-logo="{os.path.join(*[OUTPUT, lg, match['match']['img_location'].split('/')[-1]])}" group-title="{lg}",{match['match']['name']}\n""")
                    file.write(f"""{url}\n""")

    def generate_docs(self):
        for lg in self.leagues:
            p(f"Generating XML channel data for {lg.upper()}", colours.HEADER, otype.REGULAR)
            self.generate_xmltv(lg)
            p(f"Generating m3u playlist data for {lg.upper()}", colours.HEADER, otype.REGULAR)
            self.generate_m3u(lg)


def run(argv: list):
    global OUTPUT
    minutes = 30
    try:
        os.environ['stream_link'] = "https://sportscentral.io"
        if "-v" in argv:
            os.environ["verbosity"] = "0"
        else:
            os.environ["verbosity"] = "1"
        if "-vv" in argv:
            os.environ["no_verbosity"] = "0"
        else:
            os.environ["no_verbosity"] = "1"
        if "-s" in argv:
            os.environ["selenium"] = "0"
        else:
            os.environ["selenium"] = "1"
        if "-nba" in argv:
            leagues.append(NBA)
        if "-nhl" in argv:
            leagues.append(NHL)
        if "-nfl" in argv:
            leagues.append(NFL)
        if "-ef" in argv:
            leagues.append(EF)
        if "-a" in argv and len(leagues) == 0:
            leagues.append(NBA)
            leagues.append(NHL)
            leagues.append(NFL)
            leagues.append(EF)
        elif "-a" in argv and len(leagues) != 0:
            p("Cannot pass -a with -nba/-nfl/-nhl/-ef", colours.FAIL, otype.ERROR)
            sys.exit()
        if "-t" in argv:
            try:
                if argv.index("-t") + 1 >= len(argv):
                    raise Exception("Missing time input (in minutes)")
                minutes = argv[argv.index("-t") + 1]
                if minutes.startswith("-"):
                    raise Exception("Missing time input (in minutes)")
            except Exception as e:
                p(e, colours.FAIL, otype.ERROR)
        if "-o" in argv:
            try:
                if argv.index("-o") + 1 >= len(argv):
                    raise Exception("Missing output location")
                dp = str(argv[argv.index("-o") + 1])
                OUTPUT = os.path.join(*[dp, "output"])
                if dp.startswith('~') and os.name == 'nt':
                    OUTPUT = os.path.join(os.path.expandvars("%userprofile%"), dp[2:])
                elif not dp.startswith('/') and not dp.startswith('~'):
                    if dp.startswith('.'):
                        OUTPUT = os.path.join(*[os.getcwd(), dp[2:], "output"])
                    else:
                        OUTPUT = os.path.join(*[os.getcwd(), dp, "output"])
                if OUTPUT.startswith("-"):
                    raise Exception("Missing output location")
                os.environ['output'] = OUTPUT
            except Exception as e:
                p(e, colours.FAIL, otype.ERROR)
                sys.exit()
        if len(leagues) == 0:
            sys.exit()
        header()
        if "-d" in argv:
            collector = StreamCollector()
            collector.collect()
            collector.generate_docs()
        else:
            while True:
                collector = StreamCollector()
                collector.collect()
                collector.generate_docs()
                p(f"Waiting {minutes} minutes until next update", colours.WARNING, otype.REGULAR)
                time.sleep(int(int(minutes) * 60))
    except Exception as e:
        p(e, colours.FAIL, otype.ERROR, e)

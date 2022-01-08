import logging
import sys
import pretty_print
import scraping
from pretty_print import *


NBA = "nba"
NHL = "nhl"
NFL = "nfl"


# Main class
class StreamCollector:
    def __init__(self):
        self.streaming_sites = {
            NBA: scraping.find_streams(NBA),
            NHL: scraping.find_streams(NHL),
            NFL: scraping.find_streams(NFL)
        }
        self.leagues: list[str] = leagues

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

    def generate_xmltv(self):
        pass

    def generate_m3u(self):
        self.generate_xmltv()
        pass

def main() -> list[str]:
    collector = StreamCollector()
    collector.collect()
    collector.generate_m3u()


if __name__ == "__main__":
    leagues = []
    for i in sys.argv:
        if str(i) == "-v":
            pretty_print.verbosity = True
        if str(i) == "-vv":
            pretty_print.no_verbosity = True
        if str(i) == "-s":
            scraping.selenium_enabled = True
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
        if pretty_print.verbosity:
            print(e.with_traceback())

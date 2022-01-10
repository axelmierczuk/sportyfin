import os
import sys
from PIL import Image, ImageDraw
import subprocess
import hashlib
from . import league_colours, pretty_print
from dotenv import load_dotenv
import requests
load_dotenv()

NBA = "nba"
NHL = "nhl"
NFL = "nfl"
EF = "English Football"


def download_jpg(lp: list) -> list:
    res = []
    for lpi in lp:
        if not os.path.isfile(lpi[0]):
            try:
                pretty_print.pind(f"Downloading {lpi[1]} to {lpi[0]}", pretty_print.colours.OKCYAN, pretty_print.otype.DEBUG)
                r = requests.get(lpi[1], allow_redirects=True)
                open(lpi[0], 'wb').write(r.content)
                res.append(lpi[0])
            except KeyboardInterrupt:
                sys.exit()
                pass
            except Exception as e:
                pretty_print.p(f"Error occurred attempting to download - {lpi[1]}", pretty_print.colours.FAIL, pretty_print.otype.ERROR, e)
        else:
            res.append(lpi[0])
    return res


def concat_images(image_path_list: list, output: str, ht_name: str, at_name: str, league: str):
    lc = league_colours.LeagueColours(league)
    images = [Image.open(x).convert("RGBA") for x in image_path_list]
    widths, heights = zip(*(i.size for i in images))
    total_width = int(sum(widths) * 1.5)
    max_height = int(max(heights) * 1.5)

    if total_width > max_height:
        max_height = total_width
    else:
        total_width = max_height
    y_offset = int(max_height * 0.15)
    x_offset = int(max_height * 0.1)
    new_im = Image.new(mode='RGB', size=(total_width, max_height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(new_im)
    points = {
        "first": [
            (int(total_width * 0.65), 0),
            (int(total_width * 0.35), max_height),
            (0, max_height),
            (0, 0)
        ],
        "second": [
            (total_width, 0),
            (total_width, max_height),
            (int(total_width * 0.35), max_height),
            (int(total_width * 0.65), 0)
        ]
    }
    draw.polygon(points['first'], lc.get_second(ht_name))
    draw.polygon(points['second'], lc.get_second(at_name), lc.get_second(at_name))
    for c, im in enumerate(images):
        if c != 0:
            y_offset = int(max_height - y_offset - im.height)
            x_offset = int(total_width - im.width - x_offset)
        new_im.paste(im, (x_offset, y_offset), im)
    new_im.save(output, quality=100, subsampling=0)


def generate_img(m, sport: str) -> str:
    ht = m['home_team']
    at = m['away_team']
    output = os.environ.get("output")
    location = str(hashlib.sha1((ht['name']+at['name']).encode()).hexdigest())
    op = os.path.join(*[output, sport, f"{location}.jpg"])
    op_sport = os.path.join(*[output, sport])
    if not os.path.isfile(f"op"):
        if not os.path.isdir(f"{output}"):
            os.makedirs(f"{output}")
            os.makedirs(f"{op_sport}")
        elif not os.path.isdir(f"{op_sport}"):
            os.makedirs(f"{op_sport}")

        ht_p = (os.path.join(*[op_sport, f"{str(hashlib.sha1(ht['name'].encode()).hexdigest())}.png"]), ht['icon_url'])
        at_p = (os.path.join(*[op_sport, f"{str(hashlib.sha1(at['name'].encode()).hexdigest())}.png"]), at['icon_url'])
        list_im = download_jpg([ht_p, at_p])
        if len(list_im) > 1:
            try:
                concat_images(list_im, op, ht['name'], at['name'], sport)
            except KeyboardInterrupt:
                sys.exit()
                pass
            except Exception as e:
                pretty_print.p(f"Error building game icon", pretty_print.colours.FAIL, pretty_print.otype.ERROR, e)
        elif len(list_im) == 1:
            return list_im[0]
        else:
            return ""
    return op

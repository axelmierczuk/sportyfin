import numpy as np
import os
import sys
from PIL import Image
import subprocess
import hashlib

NBA = "nba"
NHL = "nhl"
NFL = "nfl"


def download_jpg(lp: list[(str, str)]) -> list[str]:
    res = []
    for lpi in lp:
        if not os.path.isfile(lpi[0]):
            try:
                print(f"[*] Downloading {lpi[1]} to {lpi[0]}")
                subprocess.run(["wget", lpi[1], "-O", lpi[0]], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                res.append(lpi[0])
            except Exception as e:
                print(f"Could not download {lpi[1]}: {e}")
        else:
            res.append(lpi[0])
    return res


def concat_images(image_path_list, output):
    images = [Image.open(x).convert("RGBA") for x in image_path_list]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    y_offset = 0
    x_offset = 0
    if total_width > max_height:
        y_offset = int((total_width - max_height) / 2)
        max_height = total_width
    else:
        x_offset = int((max_height - total_width) / 2)
        total_width = max_height
    new_im = Image.new(mode='RGB', size=(total_width, max_height), color=(255, 255, 255, 0))
    for im in images:
        new_im.paste(im, (x_offset, y_offset), im)
        x_offset += im.size[0]
    new_im.save(output)


def generate_img(m, sport: str) -> str:
    ht = m['home_team']
    at = m['away_team']
    location = str(hashlib.sha1((ht['name']+at['name']).encode()).hexdigest())
    if not os.path.isfile(f"output/{sport}/{location}.jpg"):
        if not os.path.isdir(f"output"):
            os.makedirs(f"output")
            os.makedirs(f"output/{sport}")
        elif not os.path.isdir(f"output/{sport}"):
            os.makedirs(f"output/{sport}")
        ht_p = (f"output/{sport}/{str(hashlib.sha1(ht['name'].encode()).hexdigest())}.png", ht['icon_url'])
        at_p = (f"output/{sport}/{str(hashlib.sha1(at['name'].encode()).hexdigest())}.png", at['icon_url'])
        list_im = download_jpg([ht_p, at_p])

        print(list_im)
        if len(list_im) > 1:
            concat_images(list_im, f"output/{sport}/{location}.jpg")
        elif len(list_im) == 1:
            return list_im[0]
        else:
            return ""
    return f"output/{sport}/{location}.jpg"


def generate_team_info(img_tag) -> dict:
    return {
        "name": str(img_tag.get('alt')),
        "icon_url": str(img_tag.get('src') if str(img_tag.get('src')).find('?') == -1 else str(img_tag.get('src'))[
                                                                                       :str(img_tag.get('src')).find(
                                                                                           '?')])
    }


def get_img_from_tag(tag):
    for h in tag:
        if len(h.get("alt")) > 0:
            return h
    return None


def get_game_info(tag):
    try:
        home_team_tags = tag.find('span', attrs={'class': "logo home-team competition-cell-table-cell"}).find_all('img')
        away_team_tags = tag.find('span', attrs={'class': "competition-cell-table-cell competition-cell-side2"}).find_all(
            'img')
        h_img = get_img_from_tag(home_team_tags)
        a_img = get_img_from_tag(away_team_tags)

        match = {
            "home_team": generate_team_info(h_img),
            "away_team": generate_team_info(a_img),
            "match": {
            }
        }
        match['match']['name'] = f"{match['away_team']['name']} at {match['home_team']['name']}"
        match['match']['img_location'] = generate_img(match, NBA)
        return match
    except Exception as e:
        print("[-] Error getting team information.")
        print(e)

import numpy as np
import PIL
import os
import urllib.request
from PIL import Image


def download_jpg(lp: list[(str, str)]) -> list[str]:
    res = []
    for lpi in lp:
        if not os.path.isfile(lpi[0]):
            dr = urllib.request.urlretrieve(lpi[1], lpi[0])
            if dr:
                res.append(lpi[0])
        else:
            res.append(lpi[0])
    return res


def generate_img(m, sport: str) -> str:
    ht = m['home_team']
    at = m['away_team']
    location = str(hash(ht['name']+at['name']))
    if not os.path.isfile(f"output/{sport}/{location}.jpg"):
        if not os.path.isdir(f"output"):
            os.makedirs(f"output")
            os.makedirs(f"output/{sport}")
        elif not os.path.isdir(f"output/{sport}"):
            os.makedirs(f"output/{sport}")
        ht_p = (f"output/{location}/{str(hash(ht['name']))}.jpg", ht['icon_url'])
        at_p = (f"output/{location}/{str(hash(at['name']))}.jpg", at['icon_url'])
        list_im = download_jpg([ht_p, at_p])

        if len(list_im > 1):
            imgs = [PIL.Image.open(i) for i in list_im]
            min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
            imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
            imgs_comb = PIL.Image.fromarray(imgs_comb)
            imgs_comb.save(f"output/{sport}/{location}.jpg")
        elif len(list_im == 1):
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

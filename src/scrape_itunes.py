import re
import requests


class Scrape(object):
    """docstring for ."""

    def __init__(self):
        pass

    def get_img_url(self, text):
        '''
            uses regular expressions to parse the url from json text and enhance resolution to 1000x1000
        '''
        m = re.search('http(.+)170x170bb-85\.jpg', text)
        if m:
            image_url = re.sub('170x170', '1000x1000', m.group())
            return image_url
        else:
            return 'No image found'

    def get_json_results(self, search_url, genre):
        'Print executing search for', genre
        album_requests = requests.get(search_url)
        if 'entry' in album_requests.json()['feed']: #some of these searches produce incomplete json docs. Check to see that we have a good one
            albums = album_requests.json()['feed']['entry']
            #albums = albums[hit_number]
            return albums
        else:
            return

    def get_album_details(self, album, main_genre_name):
        album_name = album['im:name']['label']
        print 'Retrieving album details for', album_name
        album_id = album['id']['attributes']['im:id']
        genre = album['category']['attributes']['label']
        genre_id = album['category']['attributes']['im:id']
        artist = album['im:artist']['label']
        full_url = album['im:image'][2]['label']
        release_date = album['im:releaseDate']['attributes']['label']
        release_year = release_date.split()[2]
        album_details = {
            'album_id': album_id,
            'genre': genre,
            'main genre': main_genre_name,
            'genre_id': genre_id,
            'artist': artist,
            'album': album_name,
            'release year': release_year,
            'img_url': self.get_img_url(full_url)
        }

        return album_details

def get_genre_names(filename):
    genre_names = {}
    with open(filename) as fhandle:
        lines = fhandle.readlines()
        for line in lines:
            info = line.split()
            genre_id, name = int(info[0]), info[1]
            if not line.startswith('\t'):
                main_genre_id = genre_id
                subgenres = {}
                genre_names[main_genre_id] = subgenres
            subgenres[genre_id] = name
    return genre_names

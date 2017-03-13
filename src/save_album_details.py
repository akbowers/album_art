import urllib
import requests
import re
import os.path

def write_to_file_and_save_to_server(filename, popular_genre_names):
    album_ids = []
    print 'Opening file'
    server_path = '/home/amanda/galvanize/project/itunes_photos/'
    with open(filename, 'w') as target:
        for genreId in popular_genre_names:
            genre = popular_genre_names[genreId]
            target.write('----------------------------')
            target.write('\n')
            target.write('\n')
            target.write(genre.upper())
            target.write('\n')
            target.write('\n')
            target.write('----------------------------')
            target.write('\n')
            target.write('\n')
            search_url = 'https://itunes.apple.com/us/rss/topalbums/genre={}/limit=200/json'.format(genreId)
            albums = get_json_results(search_url, genre)
            for hit_number in range(len(albums)):
                album = albums[hit_number]
                album_details = get_album_details(album)
                    #save_album_id(album_details, album_ids)
                target.write(str(album_details))
                target.write('\n')
                target.write('\n')
                image_url = album_details['img_url']
                img_count = hit_number + 1
                img_num = '%03d'%img_count #make it a 3-digit number with leading zeros
                print 'saving', image_url, 'on server'
                album_id = album_details['album_id']
                path = server_path + genre + album_id + '.jpg'
                if not check_duplicate(path): #Does itunes classify some albums as multiple genres?
                #In particular, do subgenres create duplicates??
                    urllib.urlretrieve(image_url, path) #download images onto server

    print 'Closing file'

def get_img_url(text):
    '''
        uses regular expressions to parse the url from json text and enhance resolution to 1000x1000
    '''
    m = re.search('http(.+)170x170bb-85\.jpg', text)
    if m:
        image_url = re.sub('170x170', '1000x1000', m.group())
        return image_url
    else:
        return 'No image found'

def check_duplicate(path):
    return os.path.exists(path)

def get_album_details(album):
    album_name = album['im:name']['label']
    print 'Retrieving album details for', album_name
    album_id = album['id']['attributes']['im:id']
    genre = album['category']['attributes']['label']
    genre_id = album['category']['attributes']['im:id']
    artist = album['im:artist']['label']
    full_url = album['im:image'][2]['label']
    album_details = {
        'album_id': album_id,
        'genre': genre,
        'genre_id': genre_id,
        'artist': artist,
        'album': album_name,
        'img_url': get_img_url(full_url)
    }

    return album_details

def get_json_results(search_url, genre):
    'Print executing search for', genre
    album_requests = requests.get(search_url)
    albums = album_requests.json()['feed']['entry']
    #albums = albums[hit_number]
    return albums

if __name__ == '__main__':
    popular_genre_names = {2: "Blues", 3: "Comedy", 4: "Children's_Music", 5: "Classical", 6: "Country", 7: "Electronic", 10:"Singer_Songwriter",\
                      11: "Jazz", 12: "Latino", 14: "Pop", 15: "R&B_Soul", 16: "Soundtrack", 17: "Dance", 18: "Hip-Hop_Rap", 19: "World", 20: "Alternative", 21: "Rock",\
                      22: "Christian & Gospel", 24: "Reggae", 50: "Fitness & Workout", \
                      51: "K-Pop", 1153: "Metal"}

    genre_names = {2: "Blues", 3: "Comedy", 4: "Children's Music", 5: "Classical", 6: "Country", 7: "Electronic", 8: "Holiday", 9: "Opera", 10:"Singer_Songwriter",\
                  11: "Jazz", 12: "Latino", 13: "New Age", 14: "Pop", 15: "R&B_Soul", 16: "Soundtrack", 17: "Dance", 18: "Hip-Hop_Rap", 19: "World", 20: "Alternative", 21: "Rock",\
                  22: "Christian_&_Gospel", 23: "Vocal", 24: "Reggae", 25: "Easy Listening", 27: "J-Pop", 28: "Enka", 29: "Anime", 30: "Kayokyoku", 50: "Fitness & Workout", \
                  51: "K-Pop", 52: "Karaoke", 53: "Instrumental", 1122: "Brazilian", 1153: "Metal"}

    country = {6: "Country"} #use this baby dictionary  for preliminary testing
    filename = 'album_artwork_details.txt'
    write_to_file_and_save_to_server(filename, genre_names)

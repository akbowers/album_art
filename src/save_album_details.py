from scrape_itunes import Scrape, get_genre_names
import boto3
import requests
from pymongo import MongoClient

def search_albums(albums):
    for hit_number in range(len(albums)):
        album = albums[hit_number]
        album_details = s.get_album_details(album, main_genre_name)
        album_id = album_details['album_id']
        #path = server_path + album_id + '.jpg'
        if not check_duplicate(album_details, col): #Does itunes classify some albums as multiple genres?
            print 'Inserting', album, 'into MongoDB'
            col.insert_one(album_details)
            image_url = album_details['img_url']
            album_id = album_details['album_id']

            print 'saving', image_url, 'on S3'
            r = requests.get(image_url)
            body = r.content
            b_key = image_url.split('/')[-2]
            write_to_s3(b_key, body)


def search_subgenres(main_genre_name, subgenres):
    '''
        Loops through all genreIds in the subgenres dictionary and retrieves the Json results
    '''
    for genreId in subgenres:
        genre = subgenres[genreId]
        search_url = 'https://itunes.apple.com/us/rss/topalbums/genre={}/limit=200/json'.format(genreId)
        albums = s.get_json_results(search_url, genre)
        if not albums: #checks that JSON file isn't incomplete
            continue
        search_albums(albums)

def write_to_s3(bucket_key, body):
       s3 = boto3.resource('s3')
       b = s3.Bucket('humanslovepenguins')
       b.put_object(Key=bucket_key, Body=body)


def create_collection():

    client = MongoClient()
    db = client.album_details
    col = db.get_collection('album_details')
    return col

def check_duplicate(entry, col):
    '''
        Checks to see if entry already exists in MongoDB
        INPUT: entry in MongoDB, collection object from pymongo
        OUTPUT: BOOL
    '''
    return col.find(entry).count() > 0

if __name__ == '__main__':

    genre_names = get_genre_names('genre_names_and_ids.tsv')
    col = create_collection()

    s = Scrape()

    for mainID in genre_names:
         subgenres = genre_names[mainID]
         main_genre_name = subgenres[mainID]
         search_subgenres(main_genre_name, subgenres)

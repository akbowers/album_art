from scrape_itunes import Scrape, get_genre_names
import boto3
import requests
from pymongo import MongoClient

def search_albums(albums):
    #for hit_number in range(len(albums)):
    hit_number = 0
    #print type(albums)
    while hit_number < len(albums):
        try:
            album = albums[hit_number]
        except KeyError:
            album = albums
        album_details = s.get_album_details(album, main_genre_name)
        album_id = album_details['album_id']
        image_url = album_details['img_url']
        album_id = album_details['album_id']
        #main_genre_name = s.album_details['main_genre']
        #path = server_path + album_id + '.jpg'
        s3 = boto3.resource('s3')
        b = s3.Bucket('humanslovepenguins')
        try:
            b_key = '{}/{}.jpg'.format(main_genre_name, album_id)
        except UnicodeDecodeError:
            print 'the following main_genre_name is fucked: '.format(main_genre_name)
        if not check_duplicate(album_details, col): #Does itunes classify some albums as multiple genres?
            print 'Inserting', album, 'into MongoDB'
            col.insert_one(album_details)
        if not check_saved_on_s3(b, b_key):
            try:
                r = requests.get(image_url)
            except requests.ConnectionError:
                print 'Connection timed out'
                time.sleep(2) #wait 10 seconds when the internet craps out
                continue
            body = r.content
            try:
                print 'saving', image_url, 'on S3'
                write_to_s3(b, b_key, body)
            except UnicodeDecodeError:
                print 'The following filename is invalid: {}'.format(b_key)

        hit_number += 1

def search_subgenres(main_genre_name, subgenres):
    '''
        Loops through all genreIds in the subgenres dictionary and retrieves the Json results
    '''
    for genreId in subgenres:
        genre = subgenres[genreId]
        #genre = s.find_unicode_error_char(genre)
        # print '-------------------\n'
        # print '\n'
        # print 'Genre NAME:'
        # print '\n'
        # print genre
        # print '\n'
        # print '--------------------\n'
        search_url = 'https://itunes.apple.com/us/rss/topalbums/genre={}/limit=200/json'.format(genreId)
        albums = s.get_json_results(search_url, genre)
        if not albums: #checks that JSON file isn't incomplete
            continue
        search_albums(albums)

def write_to_s3(bucket, bucket_key, body):
       bucket.put_object(Key=bucket_key, Body=body)


def create_collection():

    client = MongoClient()
    db = client.albums
    col = db.get_collection('album_details')
    return col

def check_duplicate(entry, col):
    '''
        Checks to see if entry already exists in MongoDB
        INPUT: entry in MongoDB, collection object from pymongo
        OUTPUT: BOOL
    '''
    return col.find(entry).count() > 0

def check_saved_on_s3(bucket, bucket_key):
    files_on_bucket = [obj.key for obj in bucket.objects.all()]
    return bucket_key in files_on_bucket

if __name__ == '__main__':

    genre_names = get_genre_names('genre_names_and_ids.tsv')
    col = create_collection()

    already_collected = ['Blues', 'Classical', 'Comedy', 'Country', 'Dance',
                        'Electronic', 'Holiday', 'Opera', 'Pop', 'Singer_Songwriter', 'Soundtrack']

    s = Scrape()

    for mainID in genre_names:
         subgenres = genre_names[mainID]
         main_genre_name = subgenres[mainID]
         main_genre_name = s.find_unicode_error_char(main_genre_name)
         if main_genre_name not in already_collected:
             search_subgenres(main_genre_name, subgenres)

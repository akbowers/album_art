# Copyright 2017 Albo-rithm: An Image Classifier by Amanda Bowers
#
# This code Finds preselected image files (*.jpg) saved in directories labeled
# by respective genre, extracts the album_id, which is used to search for the
# album details in the mongodb.
# Those album details are written along with html code to produce a 3xn tile
# layout that each contain a link to a jquery magnic pop-up
#
# This code is intended to be ran only after scraping itunes has commenced.
# =============================================================================

import os
from pymongo import MongoClient

def create_collection(col_name):

    client = MongoClient()
    db = client.album_details
    col = db.get_collection(col_name)
    return col

def get_album_ids(genre):
    '''
    returns a list of album_ids corresponding to images saved in the directory
    corresponding to the specified genre
    '''

    album_ids = []
    lookup_path = os.path.join('static/img/portfolio/fullsize', genre)
    files = os.listdir(lookup_path)
    for filename in files:
         album_id = filename.split('.')[0]
         album_ids.append(album_id)
    return album_ids

#
# def is_thumnail(album_id):
#     image_is_thumnail = False
#     lookup_path = 'static/img/portfolio/thumbnails'
#     thumnails = os.listdir(lookup_path)
#     if (album_id + '.jpg') in thumnails:
#         image_is_thumnail = True
#     return image_is_thumnail


def find_thumbnail(album_ids):
    lookup_path = 'static/img/portfolio/thumbnails'
    thumnails = os.listdir(lookup_path)
    for album_id in album_ids:
        if (album_id + '.jpg') in thumnails:
            return album_id

def get_album_details(image_is_thumnail, album_id, genre, data_group, col):
    '''
    Retrieves album details from mongo col and returns them in an href string
    INPUTS: image_is_thumnail: bool that user sets to true if he wants that album
                                cover to also appear as tile thumbnail
            filepath: str giving location of image in local directory when running web_app
            album_id: str of unique identifier of album in MongoDB
            genre: str
            data_group: int used to separate images in genre from one another when creating pop-up
            col: mongo collection object used to lookup title info for fig captions
    '''
    entry ={}
    entry["album_id"] = album_id
    #entry = '{}"album_id": "{}"{}'.format('{', album_id, '}')
    #print entry

    if col.find(entry).count() > 0:
        for result in col.find(entry):
            artist = result["artist"]
            album = result["album"]
            year = result["release year"]
    else: #We have one image whose details were not stored in db
        artist = 'Kenny Chesney'
        album = "Hemmingway's Whiskey"
        year = "2010"
        print album_id

    filepath = os.path.join('static/img/portfolio/fullsize', genre, album_id)
    try:
        if not image_is_thumnail:
            atag = '\t\t\t\t\t<a href="{}.jpg" data-group="{}" class="galleryItem portfolio-box" title="{}: {} ({})"> </a>\n'.format(filepath, str(data_group), artist, album, year)
            print atag
        else:
            atag = '\t\t\t\t\t<a href="{}.jpg" data-group="{}" class="galleryItem portfolio-box" title="{}: {} ({})">\n'.format(filepath, str(data_group), artist, album, year)
            atag += '''\t\t\t\t\t\t<img src="static/img/portfolio/thumbnails/{}.jpg" height= "150" width= "750" class="img-responsive" alt="">
\t\t\t\t\t\t\t<div class="portfolio-box-caption">
\t\t\t\t\t\t\t\t<div class="portfolio-box-caption-content">
\t\t\t\t\t\t\t\t\t<div class="project-name">
\t\t\t\t\t\t\t\t\t{}
\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t<div class="project-category text-faded">
\t\t\t\t\t\t\t\t\t{}: {}
\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</a>\n'''.format(album_id, genre, artist, album)
            print atag
    except UnicodeEncodeError:
        artist = artist.encode('utf8')
        album = album.encode('utf8')
        if not image_is_thumnail:
            atag = '\t\t\t\t\t<a href="{}.jpg" data-group="{}" class="galleryItem portfolio-box" title="{}: {} ({})"> </a>\n'.format(filepath, str(data_group), artist, album, year)
            print atag
        else:
            atag = '\t\t\t\t\t<a href="{}.jpg" data-group="{}" class="galleryItem portfolio-box" title="{}: {} ({})">\n'.format(filepath, str(data_group), artist, album, year)
            atag += '''\t\t\t\t\t\t<img src="static/img/portfolio/thumbnails/{}.jpg" height= "150" width= "750" class="img-responsive" alt="">
\t\t\t\t\t\t\t<div class="portfolio-box-caption">
\t\t\t\t\t\t\t\t<div class="portfolio-box-caption-content">
\t\t\t\t\t\t\t\t\t<div class="project-name">
\t\t\t\t\t\t\t\t\t{}
\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t<div class="project-category text-faded">
\t\t\t\t\t\t\t\t\t{}: {}
\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</a>\n'''.format(album_id, genre, artist, album)
            print atag
#     except UnicodeEncodeError:
#         if not image_is_thumnail:
#             atag = '\t\t\t\t\t\t\t\t\t<a href="{}.jpg" data-group="{}" class="galleryItem portfolio-box" title="'.format(filepath, str(data_group))
#             atag = atag + artist + ' ' + album + ' ' +  '(' + year + ')"> </a>\n'
#         else:
#             atag = '\t\t\t\t\t<a href="{}.jpg" data-group="{}" class="galleryItem portfolio-box" title="'.format(filepath, str(data_group))
#             atag = atag + artist + ' ' + album + ' ' +  '(' + year + ')"> </a>\n'
#             atag = atag + '''\t\t\t\t\t\t<img src="static/img/portfolio/thumbnails/{}.jpg" height= "150" width= "750" class="img-responsive" alt="">
# \t\t\t\t\t\t\t<div class="portfolio-box-caption">
# \t\t\t\t\t\t\t\t<div class="portfolio-box-caption-content">
# \t\t\t\t\t\t\t\t\t<div class="project-name">
# \t\t\t\t\t\t\t\t\t{}
# \t\t\t\t\t\t\t\t\t</div>
# \t\t\t\t\t\t\t\t\t<div class="project-category text-faded">
# \t\t\t\t\t\t\t\t\t{}: {}
# \t\t\t\t\t\t\t\t\t</div>
# \t\t\t\t\t\t\t\t</div>
# \t\t\t\t\t\t\t</div>
# \t\t\t\t\t\t</a>\n'''.format(album_id, genre, artist, album)
    return atag

def write_html_to_index(oldfile, newfile, new_content):
    '''
        opens 2 files. Scans oldfile to look for location to insert new html
        writes old code to newfile before location is found
        writes new code to new file after location is found
        writes remaining old code to newfile after insertion is complete
    '''
    with open(oldfile, 'r') as f_old, open(newfile, 'w') as f_new:
        insertFlag = False
        print 'looping through old index'
        for line in f_old:
            if '<!-- Begin album_tile insertion -->' in line:
                insertFlag = True
            elif '<!-- End album_tile insertion -->' in line:
                insertFlag = False
            if not insertFlag:
                f_new.write (line)
            else:
                f_new.write(line)
                f_new.write(new_content)

if __name__ == '__main__':
    # display_genres = ['Alternative', 'Anime', 'Brazilian', "Children's_Music",
    #                     'Comedy', 'Christian_&_Gospel', 'Easy_Listening', 'Enka',
    #                     'Fitness_&_Workout', 'French_Pop', 'German_Pop',
    #                     'Holiday_Music', 'Instrumental', 'J-Pop', 'Karaoke',
    #                     'K-Pop', 'Latino', 'New_Age', 'Opera', 'Singer_Songwriter',
    #                     'Soundtrack', 'Spoken_Word', 'Vocal', 'World'] # Can be whatever
    #                     #the user wants to display on website,
    #                     # but len should be divisible by  3 because 3 columns is
    #                     # specified in jquery
    display_genres = ['Blues', 'Classical', 'Country', "Children's_Music",
                        'Comedy', 'Christian_&_Gospel', 'Easy_Listening', 'Enka',
                        'Fitness_&_Workout', 'French_Pop', 'German_Pop',
                        'Holiday_Music', 'Instrumental', 'J-Pop', 'Karaoke',
                        'K-Pop', 'Latino', 'New_Age', 'Opera', 'Singer_Songwriter',
                        'Soundtrack', 'Spoken_Word', 'Vocal', 'World'] # Can be whatever
                        #the user wants to display on website,
                        # but len should be divisible by  3 because 3 columns is
                        # specified in jquery

    col = create_collection('album_details_full')

    group = 0
    write_content = ''
    for genre in display_genres:
        write_content = write_content + '\t\t\t\t<div class="col-lg-4 col-sm-6">\n'
        group += 1
        album_ids = get_album_ids(genre)
        thumbnail_id = find_thumbnail(album_ids)
        write_content = write_content + get_album_details(True, thumbnail_id, genre, group, col)
        for album_id in album_ids:
            if not album_id == thumbnail_id:
                write_content = write_content + get_album_details(False, album_id, genre, group, col)
        write_content = write_content + '\t\t\t\t</div>\n'
    # print write_content
    write_html_to_index('templates/incomplete_more-artwork.html',
                        'templates/more-artwork.html',
                        write_content)

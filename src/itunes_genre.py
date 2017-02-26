import urllib
#import json
import re
from collections import OrderedDict

def get_img_url(text):
    m = re.search('artworkUrl100(.+)\.jpg', text)
    if m:
        #print m.group()
        m2 = re.search('http.+', m.group())
        if m2:
            image_url = re.sub('100x100', '1000x1000', m2.group())
            return image_url
        else:
            return 'ArtworkUrl broken'
    else:
        return 'No image found'

def store_album_name(text):
    '''
        OUTPUT: bool


    '''
    pass


def is_repeat(albumn_name, albumns_stored):
    '''
        OUTPUT: bool

        Checks whether or not this albums artwork has been saved
    '''
    if albumn_name in albumns_stored:
        return True
    else:
        return False

def get_json_url(search_term):
    '''
        INPUT: a dictionary that maps genre name to top40 albumns sold in itunes_url
        OUTPUT: None

        This function loops through all albumn_names in said genre and scapes iTunes search API to retrieve JSON text
    '''


    #print type(search_term)
    itunes_url = 'https://itunes.apple.com/search?term=' + search_term
    response = urllib.urlopen(itunes_url) #response spits out JSON text
    print 'extracting Apple search API json files'
    lines = response.readlines()
    JSON_doc = ' '.join(lines)
    img_url = get_img_url(JSON_doc)
    return img_url

def save_to_server(img_url, genre, img_num):
    '''
        INPUT: img_url, genre
        OUTUT: None
        Downloads images from url and stores them on garage server
    '''
    #server_path = '/run/user/1000/gvfs/smb-share:server=10.227.195.203,share=storage/music_image_project/'
    print 'saving', img_url, 'on server'
    server_path = '/home/amanda/galvanize/project/itunes_photos/'
    if len(img_num) == 1:
        path = server_path + genre + '00' + img_num + '.jpg'
    elif len(img_num) == 2:
        path = server_path + genre + '0' + img_num + '.jpg'
    else:
        path = server_path + genre + img_num + '.jpg'

    urllib.urlretrieve(img_url, path) #download images onto server
    return

def write_to_file(filename):
    genre_images = get_json_url(hip_hop)
    target = open(filename, 'w')
    print 'Opening file'
    print type(genre_images)
    print genre_images
    for genre, urls in genre_images:
        print 'Writing', genre, 'to file'
        target.write(genre)
        target.write('\n')
        target.write(urls)
    print 'Closing file'
    target.close()

def unique_searches(popular_genres_by_country):
    '''
        INPUT: dictionary that separates albums by genre and country code (may have duplicates)
        OUTPUT: dictionary that only separates albums by country code
        looks for duplicates in each country's top40 list across a particular genre and eliminates said duplicates
    '''

    tot_genres = 0
    tot_unique_genres = 0
    popular_genres = {}
    prev_genre = popular_genres_by_country.keys()[0].split()[0]
    for genre in popular_genres_by_country:
        print 'genre', genre
        current_genre = genre.split()[0]
        print 'current:', current_genre
        #if current_genre == prev_genre:
        albums = popular_genres_by_country[genre]
        tot_genres += len(albums)
        for search_term in albums:
            if search_term not in popular_genres.get(current_genre, []):
                popular_genres[current_genre] = popular_genres.get(current_genre, []) + [search_term]
                tot_unique_genres += 1
        prev_genre = genre.split()[0]

    return popular_genres, tot_genres, tot_unique_genres

if __name__ == '__main__':
    genre_names = {2: "Blues", 3: "Comedy", 4: "Children's Music", 5: "Classical", 6: "Country", 7: "Electronic", 8: "Holiday", 9: "Opera", 10:"Singer/Songwriter",\
                  11: "Jazz", 12: "Latino", 13: "New Age", 14: "Pop", 15: "R&B/Soul", 16: "Soundtrack", 17: "Dance", 18: "Hip-Hop/Rap", 19: "World", 20: "Alternative", 21: "Rock",\
                  22: "Christian & Gospel", 23: "Vocal", 24: "Reggae", 25: "Easy Listening", 27: "J-Pop", 28: "Enka", 29: "Anime", 30: "Kayokyoku", 50: "Fitness & Workout", \
                  51: "K-Pop", 52: "Karaoke", 53: "Instrumental", 1122: "Brazilian"}
    hip_hop = {18: "Hip-Hop/Rap"} #use this baby dictionary  dfoe preliminary testing

    #album names come from www.itunescharts.net/uk/albums/Alternative
    popular_genres_by_country = {"Alternative UK": ["Rag'n'Bone Man - Human", "The 1975 - I like it when you sleep, for you are so beautiful yet so unaware of it", "Blossoms - Blossoms", \
                                                    "Elbow - Little Fictions", "The 1975 - The 1975", "twenty one pilots - Blurryface", "Kings of Leon - WALLS", "Coldplay - A Head Full of Dreams",\
                                                    "Christine and the Queens - Chaleur Humaine", "Catfish and the Bottlemen - The Ride", "Rag'n'Bone Man - Wolves", "Bastille - Wild World",\
                                                    "The xx - I see You", "Lana Del Rey - Ultraviolence", "Biffy Clyro - Ellipsis", "Lana Del Rey - Born to Die", "Panic! At the Disco - Death of A Bachelor",\
                                                    "Oh Wonder - Oh Wonder", "twenty one pilots - Vessel", "Oasis - Time Flies... 1994-2009", "Red Hot Chili Peppers - Greatest Hits", "Bastille - Bad Blood", \
                                                    "Arctic Monkeys - Whatever People Say I Am, That's What I'm Not", "Fall Out Boy - American Beauty/ American Psycho", "Kaleo - A/B", "Green Day - American Idiot"\
                                                    "Arctic Monkeys - AM", "Kings of Leon - Only by the Night", "Catfish and the Bottlemen - The Balcony", "Lana Del Rey - Born to Die - The Paradise Edition" \
                                                    "London Grammar - If You Wait", "LINKIN PARK - Hybrid Theory", "Oasis - (What's the Story) Morning Glory?", "Melanie Martinez - Cry Baby", "Snow Patrol - Up to Now",\
                                                    "Lana Del Rey - Honeymoon", "Two Door Cinema Club - Gameshow", "Maggie Rogers - Now that the Light is Fading - EP"],
                                "Alternative US": ["City Heads - Dessert - EP", "Hippo Campus Landmark", "Acceptance - Colliding By Design", "Panic At the Disco - Death Of A Bachelor", "Dirty Projectors - Dirty Projectors",\
                                                   "Los Campesinos! - Sick Scenes", "King Gizzard & The Lizard Wizard - Flying Microtonal Banana", "Maggie Rogers - Now That the Light Is Fading - EP", "The Lumineers - Cleopatra",\
                                                   "Halsey - BADLANDS", "twenty one pilots - Blurryface", "NEWNEWNEW"],
                                      "Blues US": ["Etta James - At Last!"]}

    ordered_genres = OrderedDict()
    ordered_genres["Alternative UK"] = popular_genres_by_country["Alternative UK"]
    ordered_genres["Alternative US"] = popular_genres_by_country["Alternative US"]
    ordered_genres["Blues US"] = popular_genres_by_country["Blues US"]
    #print get_json_url(genre_names)
    #print len(genre_names)
    #print get_json_url({18: "Hip-Hop/Rap"})

    popular_genres, tot1, tot2  = unique_searches(ordered_genres)
    #print popular_genres
    #print '\n'
    #print 'Total genres: {} \n Unique genres: {}'.format(tot1, tot2)

    ##########################################################################################

    #                       GOOD CODE

    #####################################################################################

    img_count = 0 #count all images in genre
    prev_genre = popular_genres.keys()[0]
    for genre in popular_genres:
        albums = popular_genres[genre]
        for search_term in albums:
            img_url = get_json_url(search_term)

            if not genre == prev_genre:
                img_count = 0 #initialize img_count back to zero if we're on a new genre (disregarding country code!!!)
            img_count += 1
            if not img_url == 'No image found':
                save_to_server (img_url, genre, str(img_count))
        prev_genre = genre
    #write_to_file('album_artwork_urls.txt')

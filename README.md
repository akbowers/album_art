# album_art

This repository was created for my cumulative project at Galvanize. The goal is to train a convolutional neural network on iTunes album covers for 11 different genres.

25 Feb 2016 UPDATE

- Repo created
- Using the iTunes search API to download album cover images in jpeg format
  - https://itunes.apple.com/search?term=Adele
  - url leads to JSON doc with track info for all tracks matching specified query
  - intunes_genre.py searches for artworkUrl100 to find url with highest resolution image. (Can hack url to increase resolution)
- Code is available to automate Downloads. Save images to remote server. I have shortcut path on my machine (~/galvanize/project/itunes_photos)
- Need to scrape www.itunescharts.net to generate dictionary of all search terms per genre. Currently using manually created dictionary, which only performs 44 searches. 

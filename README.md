### Project began on 25 Feb 2017

This repository was created for my cumulative project at Galvanize. The goal is to train a convolutional neural network on iTunes album covers for different genres. This project is currently under construction

### 13 March 2017 UPDATE

# Predicting Genre from Album Art

## Business Understanding
Much progress has been made in recent years to classify images and train algorithms using neural networks. In some cases, computers have performed better at image recognition than humans (e.g. in medical diagnostics using MRIs)[reference]. However, very little progress has been made to understand the features that classify different types of music. Streaming services such as Pandora, Apple Music, and Spotify rely largely on ratings and recommendations of “friends” in order to recommend new music to users. While this project itself is not a recommender system, future research into the correlation between album art and music “genre” can help improve those existing recommender systems deployed by music streaming services.
The goal of the project is to somehow tie the advanced machine learning knowledge of image classification to the not well-understood latent features of audio clips.
Traditionally, recommendations are made based on historical usage data. Tracks are recommended based on preferences . However, new models are on the market that attempt to use the latent features in the audio clip to make predictions. Since my project only looks for correlations between genre and album art, I think it remains an original idea whose results could prove highly valuable in the performance of music recommender systems. For more on state of the art algorithms used at Spotify:

http://benanne.github.io/2014/08/05/spotify-cnns.html

The results of this project may also prove useful to marketing teams at major record labels. When trying to decide on various details of an album cover, such as the lighting of a photograph or the color-scheme of a digitally rendered image, marketing teams are trying to determine which art is most appealing to their listeners. Producing an album cover that appeals to a different sector of the market than the music itself could potentially disway listeners from purchasing the album. Currently, these decisions regarding the final touches of an album cover lie in the hands of humans, but running the image through a machine-learning genre classifier prior to releasing the album, could help confirm that that artwork would appeal to the desired audience or might suggest that the team reconsider a few details of the cover.

## Data Understanding
The iTunes search API is surprisingly easy to scrape. The genre of music can be specified via the following url:

    search_url = 'https://itunes.apple.com/us/rss/topalbums/genre={}/limit=200/json'.format(genreId)

where the genreID is an integer that maps to a particular genre. The file ‘genre_names_and_ids.tsv’ contains a list of all the genreIDs and names, where subgenres are indented under their respective umbrella genre. By looping through the genreIDs, we can retrieve the json documentation provided by Apple for up to 200 album hits. The image url can easily be parsed from this documentation and the images can be saved on an Amazon S3 bucket.

## Data Preparation
The Python libraries urllib and requests are use to parse the JSON documents returned by the search API. For each search result, three image URLs are provided all linking to the same album art. The image results differ by resolution. However, the highest resolution image provided is only 170 x 170. Although the model may actually be trained on low-resolution images, higher resolution (1000 x 1000) images were initially stored. Regular expressions were used to hack the URL.

## Modeling
Convolutional neural networks will be trained on image data to make predictions about music genre. We are researching the posibility of using Deep Convolutional Activation Feature (DECAF) transfer learning to train the images faster and enhance performance.  

## Evaluation
Performance evaluation will be done through cross-validation. I will also do a simple 80/20 train/test split on the images scraped.

## Deployment
Not only will I create a powerpoint presentation summarizing my work (hopefully with an ROC curve), but ideally I can deploy my algorithm on a website where users can upload an image and ask the classifier to determine which genre of music it would belong to if used for album art. This would require some basic javascript skills and pretty good confidence in the performance of my CNNs.

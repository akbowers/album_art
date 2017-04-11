# Albo-rithm: Predicting Genre From Album Art

This repository was created for my cumulative project at Galvanize. The goal is to train a convolutional neural network on iTunes album covers for different genres. This project is currently under construction

## Business Understanding

Albums are not simply a collection of music, but rather a body of art. The album cover is the piece of visual art an artist can use to most effectively grab a potential listener's attention. While the attention-grabbing effectiveness of a cover photo was absolutely crucial during the age of record stores, modern listeners are presented with more possible pathways to arrive at the purchase of a new album, such as a recommendation from iTunes, Pandora, or Spotify. These recommender systems, however, are flawed in that they make recommendations based soley on what other listeners with similar purchase histories like. The current recommender systems make no attempt to find the latent features in the audio clips of songs to generate music profiles of their listeners (although this is a current area of active research). Therefore, the album cover remains critical when marketing music to a target audience.

Genre has long been the fundamental classification system for categorizing different types of music. While album covers within a particular genre all tend to share some of the same stylistic features, it would be useful to know if proposed album artwork for a new album could be easily classified into its intended music genre simply be looking at the cover. If a machine learning algorithm could do this with a high degree of accuracy, record labels could rely on the predicted genre of the algorithm to help guide their business decisions.

Moreover, if machine learning image classifiers were to become good at detecting stylistic features in images, the applications would span far beyond the scope of this project. Machine learning could be used to detect fraudulent paintings, recognize similarities between photos of two similar travel destinations, or help home-buyers find the most aesthetically pleasing homes.

## Data Understanding

Image classifiers are known to have high performance when the size of each class is on the order of 5000 images. In order to obtain a large enough image dataset, the iTunes search API was scraped by genre Id. Because the maximum number of hits that can be returned for any given search is only 200, umbrella genres were grouped together with their subgenres (as classified by iTunes) to increase the total number of images per class.

The following URL returns a JSON document with album information for the 200 most popular albums in the specified genre:

  search_url = 'https://itunes.apple.com/us/rss/topalbums/genre={}/limit=200/json'.format(genreId)

The Python libraries urllib and requests can be used to parse this JSON.

iTunes classifies genres in the following way:

### Genres and Subgenres by Genre ID

**2 Blues**
	* 1007 Chicago Blues
	* 1009 Classic Blues
	* 1010 Contemporary Blues
	* 1011 Country Blues
	* 1012 Delta Blues
	* 1013 Electric Blues
	* 1210 Acoustic Blues
**3 Comedy**
	* 1167 Novelty
	* 1171 Standup Comedy
**4 Children’s Music**
	* 1014 Lullabies
	* 1015 Sing-Along
	* 1016 Stories
**5 Classical**
	* 1017 Avant-Garde
	* 1018 Baroque
	* 1019 Chamber Music
	* 1020 Chant
	* 1021 Choral
	* 1022 Classical Crossover
	* 1023 Early Music
	* 1024 Impressionist
	* 1025 Medieval
	* 1026 Minimalism
	* 1027 Modern Composition
	* 1028 Opera
	* 1029 Orchestral
	* 1030 Renaissance
	* 1031 Romantic
	* 1032 Wedding Music
	* 1211 High Classical
**6 Country**
	* 1033 Alternative Country
	* 1034 Americana
	* 1035 Bluegrass
	* 1036 Contemporary Bluegrass
	* 1037 Contemporary Country
	* 1038 Country Gospel
	* 1039 Honky Tonk
	* 1040 Outlaw Country
	* 1041 Traditional Bluegrass
	* 1042 Traditional Country
	* 1043 Urban Cowboy
**7 Electronic**
	* 1056 Ambient
	* 1057 Downtempo
	* 1058 Electronica
	* 1060 IDM/Experimental
	* 1061 Industrial
**8 Holiday**
	* 1079 Chanukah
	* 1080 Christmas
	* 1081 Christmas: Children’s
	* 1082 Christmas: Classic
	* 1083 Christmas: Classical
	* 1084 Christmas: Jazz
	* 1085 Christmas: Modern
	* 1086 Christmas: Pop
	* 1087 Christmas: R&B
	* 1088 Christmas: Religious
	* 1089 Christmas: Rock
	* 1090 Easter
	* 1091 Halloween
	* 1092 Holiday: Other
	* 1093 Thanksgiving
<br> **9 Opera** </br>
<br> **10 Singer/Songwriter** </br>
	* 1062 Alternative Folk
	* 1063 Contemporary Folk
	* 1064 Contemporary Singer/Songwriter
	* 1065 Folk-Rock
	* 1066 New Acoustic
	* 1067 Traditional Folk
**11 Jazz**
	* 1052 Big Band
	* 1106 Avant-Garde Jazz
	* 1107 Contemporary Jazz
	* 1108 Crossover Jazz
	* 1109 Dixieland
	* 1110 Fusion
	* 1111 Latin Jazz
	* 1112 Mainstream Jazz
	* 1113 Ragtime
	* 1114 Smooth Jazz
	* 1207 Hard Bop
	* 1208 Trad Jazz-1
	* 1209 Cool
**12 Latino**
	* 1115 Latin Jazz
	* 1116 Contemporary Latin
	* 1117 Pop Latino
	* 1118 Raíces
	* 1119 Reggaeton y Hip-Hop
	* 1120 Baladas y Boleros
	* 1121 Alternativo & Rock Latino
	* 1123 Regional Mexicano
	* 1124 Salsa y Tropical
**13 New Age**
	* 1125 Environmental
	* 1126 Healing
	* 1127 Meditation
	* 1128 Nature
	* 1129 Relaxation
	* 1130 Travel
**14 Pop**
	* 1131 Adult Contemporary
	* 1132 Britpop
	* 1133 Pop/Rock
	* 1134 Soft Rock
	* 1135 Teen Pop
**15 R&B/Soul**
	* 1136 Contemporary R&B
	* 1137 Disco
	* 1138 Doo Wop
	* 1139 Funk
	* 1140 Motown
	* 1141 Neo-Soul
	* 1142 Quiet Storm
	* 1143 Soul
**16 Soundtrack**
	* 1165 Foreign Cinema
	* 1166 Musicals
	* 1168 Original Score
	* 1169 Soundtrack
	* 1172 TV Soundtrack
**17 Dance**
	* 1044 Breakbeat
	* 1045 Exercise
	* 1046 Garage
	* 1047 Hardcore
	* 1048 House
	* 1049 Jungle/Drum’n’bass
	* 1050 Techno
	* 1051 Trance
**18 Hip-Hop/Rap**
	* 1068 Alternative Rap
	* 1069 Dirty South
	* 1070 East Coast Rap
	* 1071 Gangsta Rap
	* 1072 Hardcore Rap
	* 1073 Hip-Hop
	* 1074 Latin Rap
	* 1075 Old School Rap
	* 1076 Rap
	* 1077 Underground Rap
	* 1078 West Coast Rap
**19 World**
	* 1177 Afro-Beat
	* 1178 Afro-Pop
	* 1179 Cajun
	* 1180 Celtic
	* 1181 Celtic Folk
	* 1182 Contemporary Celtic
	* 1184 Drinking Songs
	* 1185 Indian Pop
	* 1186 Japanese Pop
	* 1187 Klezmer
	* 1188 Polka
	* 1189 Traditional Celtic
	* 1190 Worldbeat
	* 1191 Zydeco
	* 1195 Caribbean
	* 1196 South America
	* 1197 Middle East
	* 1198 North America
	* 1199 Hawaii
	* 1200 Australia
	* 1201 Japan
	* 1202 France
	* 1203 Africa
	* 1204 Asia
	* 1205 Europe
	* 1206 South Africa
**20 Alternative**
	* 1001 College Rock
	* 1002 Goth Rock
	* 1003 Grunge
	* 1004 Indie Rock
	* 1005 New Wave
	* 1006 Punk
**21 Rock**
	* 1144 Adult Alternative
	* 1145 American Trad Rock
	* 1146 Arena Rock
	* 1147 Blues-Rock
	* 1148 British Invasion
	* 1149 Death Metal/Black Metal
	* 1150 Glam Rock
	* 1151 Hair Metal
	* 1152 Hard Rock
	* 1153 Metal
	* 1154 Jam Bands
	* 1155 Prog-Rock/Art Rock
	* 1156 Psychedelic
	* 1157 Rock & Roll
	* 1158 Rockabilly
	* 1159 Roots Rock
	* 1160 Singer/Songwriter
	* 1161 Southern Rock
	* 1162 Surf
	* 1163 Tex-Mex
**22 Christian & Gospel**
	* 1094 CCM
	* 1095 Christian Metal
	* 1096 Christian Pop
	* 1097 Christian Rap
	* 1098 Christian Rock
	* 1099 Classic Christian
	* 1100 Contemporary Gospel
	* 1101 Gospel
	* 1103 Praise & Worship
	* 1104 Southern Gospel
	* 1105 Traditional Gospel
**23 Vocal**
	* 1173 Standards
	* 1174 Traditional Pop
	* 1175 Vocal Jazz
	* 1176 Vocal Pop
**24 Reggae**
	* 1183 Dancehall
	* 1192 Roots Reggae
	* 1193 Dub
	* 1194 Ska
**25 Easy Listening**
	* 1053 Bop
	* 1054 Lounge
	* 1055 Swing
<br> **27 J-Pop** </br>
<br> **28 Enka** </br>
<br> **29 Anime** </br>
<br> **30 Kayokyoku** </br>
<br> **50 Fitness & Workout** </br>
<br> **51 K-Pop** </br>
<br> **52 Karaoke** </br>
<br> **53 Instrumental** </br>
<br> **1122 Brazilian** </br>
	* 1220 Axé
	* 1221 Bossa Nova
	* 1222 Choro
	* 1223 Forró
	* 1224 Frevo
	* 1225 MPB
	* 1226 Pagode
	* 1227 Samba
	* 1228 Sertanejo
	* 1229 Baile Funk
<br> **50000061 Spoken Word** </br>
<br> **50000063 Disney** </br>
<br> **50000064 French Pop** </br>
<br> **50000066 German Pop** </br>

*Note:* The aforementioned grouping results in the creation of fairly heterogenous classes, which poses potential problems. For example, a death metal / black metal album and a blues-rock album would both be labeled as 'Rock.'

## Data Preparation

For each search result, three image URLs are provided all linking to the same album art. The image results differ by resolution. However, the highest resolution image provided is only 170 x 170. Although the model may actually be trained on low-resolution images, higher resolution (1000 x 1000) images were initially stored. Regular expressions were used to hack the URL. Other details of the album, such as the album id, album name, artist, genre name, main genre, genre id, and release year were stored together using MongoDB.

In total, 34,484 were stored ranging across 36 different genres. These images were stored on an AWS S3 bucket and all computations were performed using an EC2 instance in the cloud.

## Modeling

Transfer Learning

![alt text](https://4.bp.blogspot.com/-TMOLlkJBxms/Vt3HQXpE2cI/AAAAAAAAA8E/7X7XRFOY6Xo/s1600/image03.png "Inception V3 with Tensorflow")
<br>A convolutional Neural Net (CNN) illustrating Google's Inception V3 architecture.</br>


![alt text](figs/forward_propagation.png "Goodfellow, I., Bengio, Y., & Courville, A. (2017). Deep learning. Cambridge, MA: MIT Press.")
<br>Forward propagation with dropout: Randomly Selected Input Layer μ (binary inputs sampled independently)</br>

![alt text](figs/pooling.png "Goodfellow, I., Bengio, Y., & Courville, A. (2017). Deep learning. Cambridge, MA: MIT Press.")
<p>Max pooling reduces variance:</p>
<p>*(Top)* Maximum of three inputs taken to obtain outputs</p>
<p>*(Bottom)* Same inputs shifted to the right by one pixel. Outputs remain relatively unchanged.</p>

![alt text](figs/rotational_invariance.png "Goodfellow, I., Bengio, Y., & Courville, A. (2017). Deep learning. Cambridge, MA: MIT Press.")
<br>An example of rotational invariance due to pooling</br>

## Evaluation

## Deployment

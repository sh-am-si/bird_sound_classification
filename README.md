# Legal notice of using *xeno-canto*

Users are free to download and distribute these recordings as long as they attribute the recordist, but they are not free to use them commercially or alter them in any way. As an example of a valid use under this license, a user is free download a recording from xeno-canto and offer it for download from her own website provided that the recordist is properly credited.

## source
[xeno-canto.org](https://xeno-canto.org/)

##  creating local database
use birdDB
db.createCollection("birdSoundDB")

## restore mongo

https://stackoverflow.com/questions/13312358/mongo-couldnt-connect-to-server-127-0-0-127017

sudo service mongodb stop 

sudo rm /var/lib/mongodb/mongod.lock 

sudo mongod --repair --dbpath /var/lib/mongodb 

sudo mongod --fork --logpath /var/lib/mongodb/mongodb.log --dbpath /var/lib/mongodb 

sudo service mongodb start

## ffmpeg

```bash
sudo apt update
sudo apt install ffmpeg
```




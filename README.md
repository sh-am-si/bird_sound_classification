##  creating local database
use birdDB
db.createCollection("birdSoundDB")

## ffmpeg

```bash
sudo apt update
sudo apt install ffmpeg
```

## restore mongo

https://stackoverflow.com/questions/13312358/mongo-couldnt-connect-to-server-127-0-0-127017

sudo service mongodb stop 

sudo rm /var/lib/mongodb/mongod.lock 

sudo mongod --repair --dbpath /var/lib/mongodb 

sudo mongod --fork --logpath /var/lib/mongodb/mongodb.log --dbpath /var/lib/mongodb 

sudo service mongodb start

## source
[xeno-canto.org](https://xeno-canto.org/)
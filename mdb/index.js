const { MongoClient } = require("mongodb");

const uri =
  "mongodb+srv://volodya:seniseviyorum@cluster0.qyssq.mongodb.net/birdDB?retryWrites=true&writeConcern=majority"; 

const client = new MongoClient(uri);

async function run() {
  try {
    await client.connect();
    const database = client.db('birdDB');
    const records = database.collection('mbirdSoundDB');

    // const query = { name: 'Common Chiffchaff' };
    const query = {};
    const rec = await records.find(query);
    console.log(rec);
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
run().catch(console.dir);

const sqlite3 = require("sqlite3").verbose()
export default async function handler(req, res){
    const db = new sqlite3.Database("test.db")

    

    db.run("CREATE TABLE IF NOT EXISTS all_docs_ (doc_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, creator_id INTEGER NOT NULL, title TEXT NOT NULL)")
    db.run("CREATE TABLE IF NOT EXISTS slides (doc_id INTEGER NOT NULL, slide_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL)")
    db.run("CREATE TABLE IF NOT EXISTS editors (user_id TEXT NOT NULL, doc_id INTEGER NOT NULL, title TEXT NOT NULL)")
    if(req.method == "PUT"){
        let user_id = req.body.user_id
        console.log(user_id)

        let title = req.body.title
        console.log(title)
        let doc_id = null
        db.run("INSERT INTO all_docs_ (creator_id, title) VALUES(?, ?)", [user_id, title], function(err){
            doc_id = this.lastID
            db.run("INSERT INTO editors (user_id, doc_id, title) VALUES(?, ?, ?)", [user_id, doc_id, title], function(err){
                return res.status(200).json({doc_id : doc_id})
            })



        })


    }


    if(req.method == "POST"){

        let docs = []


        let user_id = req.body.user_id


        db.all("SELECT * FROM editors WHERE user_id = ?", [String(user_id)], function(err, rows){
            return res.status(200).json(rows)



        })



    }



}
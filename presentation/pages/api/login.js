const sqlite3 = require("sqlite3").verbose()
export default function handler(req, res){
    const db = new sqlite3.Database("test.db")
    db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)")

    if(req.method == "POST"){
        let username = req.body.username
        let password = req.body.password
        db.all("SELECT * FROM users WHERE username = ? AND password = ?", [username, password], function(err, rows){
            if(!rows.length == 0){
                return res.status(200).json({"success" : "h", "user_id" : rows[0].id})



            }
            else{
                return res.status(200).json({"err" : "h"})
            }
        })




    }


}

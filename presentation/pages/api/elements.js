const sqlite3 = require("sqlite3").verbose()

export default function hanlder(req, res){
    const db = new sqlite3.Database("test.db")
    db.run("CREATE TABLE IF NOT EXISTS elements (slide_id INTEGER NOT NULL, element_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL, top TEXT NOT NULL DEFAULT 'no', left TEXT NOT NULL DEFAULT 'no', textContent TEXT NOT NULL DEFAULT '')")
    if(req.method == "POST"){
        let type = req.body.type
        let slide_id = req.body.slide_id
        db.run("INSERT INTO elements (type, slide_id) VALUES(?, ?)", [type, slide_id], function(err){
            let e_id = this.lastID
            db.get("SELECT * FROM elements WHERE element_id = ?", [e_id], function(err, row){
                return res.status(200).json(row)
            })
        })

    }
    if(req.method == "PUT"){
        let slide_id = req.body.slide_id
        db.all("SELECT * FROM elements WHERE slide_id = ?", [slide_id], function(err, rows){
            return res.status(200).json(rows)
        })
    }
}
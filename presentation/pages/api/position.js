const sqlite3 = require("sqlite3").verbose()
export default function handler(req, res){
    const db = new sqlite3.Database("test.db")
    if(req.method == "POST"){
        let left = req.body.left
        let top = req.body.top
        let element_id = req.body.element_id
        console.log(left)
        console.log(top)
        console.log(element_id)
        db.run("UPDATE elements SET top = ?, left = ? WHERE element_id = ?", [top, left, element_id], function(err){
            return res.status(200).json({"h" : "h"})
        })

    }
}
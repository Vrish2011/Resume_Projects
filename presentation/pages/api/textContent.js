const sqlite3 = require("sqlite3").verbose()
export default function handler(req, res){
    const db = new sqlite3.Database("test.db")
    if(req.method == "POST"){
        let element_id = req.body.element_id
        let textContent = req.body.textContent
        console.log(element_id)
        console.log(textContent)
        db.run("UPDATE elements SET textContent = ? WHERE element_id = ?", [textContent, element_id], function(err, row){
            return res.status(200).json({"h" : "h"})
        })

    }
}

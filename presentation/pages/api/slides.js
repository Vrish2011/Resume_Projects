const sqlite3 = require("sqlite3").verbose()

export default function Handler(req, res){
    const db = new sqlite3.Database("test.db")
    if(req.method == "POST"){
        let doc_id = req.body.doc_id
        console.log(parseInt(doc_id[0]))

        db.all("SELECT * FROM slides WHERE doc_id = ?", [parseInt(doc_id[0])], function(err, rows){
            let slides = []
            let completed = 0
            for(let i = 0; i < rows.length; i++){
                console.log(rows.length)
                db.all("SELECT * FROM elements WHERE slide_id = ?", [rows[i].slide_id], function(err, rows_){

                    let json = {slide_id : rows[i].slide_id, doc_id : rows[i].doc_id, content : rows[i].content, elements: []}
                    console.log(JSON.stringify(json))
                    for(let j = 0; j < rows_.length; j++){
                        console.log(JSON.stringify(rows_[j]))
                        json.elements.push({element_id : rows_[j].element_id, slide_id : rows_[j].slide_id, type: rows_[j].type, top: rows_[j].top, left: rows_[j].left, textContent : rows_[j].textContent})

                    }
                    slides.push(json)
                    completed++
                    if(completed == rows.length){
                        
                        return res.status(200).json(slides)
                    }

                })

            }
            console.log(JSON.stringify(slides))

        })
    }
    if(req.method == "PUT"){
        let doc_id = parseInt(req.body.doc_id, 10)
        console.log(req.body.doc_id[0])

        db.run("INSERT INTO slides (doc_id, content) VALUES(?,?)", [doc_id, ""], function(err, rows){
            return res.status(200).json(this)
        })
    }
}
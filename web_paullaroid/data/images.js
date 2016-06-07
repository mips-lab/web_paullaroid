{
   "_id": "_design/images",
   "language": "javascript",
   "views": {
       "all": {
           "map": "function(doc) {\n  if (doc.type_doc == 'image')\n\t{\n  \t  emit([doc.event_id, doc._id], doc);\n}\n}"
       }
   }
}

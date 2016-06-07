{
   "_id": "_design/event",
   "language": "javascript",
   "views": {
       "all": {
           "map": "function(doc) {\n  if (doc.type_doc == 'event')\n\t{\n  \t  emit(doc._id, doc);\n      }\n}"
       }
   }
}

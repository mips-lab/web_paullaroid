{
   "_id": "_design/images",
   "language": "javascript",
   "views": {
       "all": {
           "map": "function(doc) {\n  if (doc.type_doc == 'image')\n\t{\n\t  var tmp = doc._id.split('_');\n  \t  emit([doc.event_id, tmp[0]], doc);\n}\n}",
           "reduce": "function(keys, values, rereduce)\n{\n   var result = {nb: 0};\n   if (rereduce){\n\tfor(var i=0; i < values.length; i++) {\n\t  result.nb += values[i].nb;\n\t }\n\treturn result;\n     }\n   result.nb = values.length;\n   return result;\n}"
       }
   }
}

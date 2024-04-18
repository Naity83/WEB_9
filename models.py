
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

connect(db="hw_9", host="mongodb+srv://web8:150209@cluster0.tn5gmti.mongodb.net/")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField(min_length=10)
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)    
    quote = StringField()
    meta = {"collection": "quotes"}



    
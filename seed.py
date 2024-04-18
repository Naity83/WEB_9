import json
from models import Author, Quote


def read_data(file):
    with open(file, 'r', encoding='utf-8') as fd:
        data = json.load(fd)
    return data


def fill_data_authors(data):
    Author.drop_collection()
    for el in data:
        author = Author()
        author.fullname = el['fullname']
        author.born_date = el['born_date']
        author.born_location = el['born_location']
        author.description = el['description']
        author.save()


def fill_data_quotes(data):
    Quote.drop_collection()
    for el in data:
        quote = Quote()
        quote.tags = el['tags']
        quote.author = Author.objects(fullname=el['author'])[0].id
        quote.quote = el['quote']
        quote.save()


if __name__ == '__main__':
    data_authors = read_data('authors.json')
    data_for_quotes = read_data('quotes.json')
    fill_data_authors(data=data_authors)
    fill_data_quotes(data_for_quotes)





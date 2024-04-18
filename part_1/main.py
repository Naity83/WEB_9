import requests
from bs4 import BeautifulSoup
import json

url = 'https://quotes.toscrape.com/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

QUOTES_INFO = []
AUTHORS_INFO = []

def quotes():
    quotes_list = [quote.text for quote in soup.find_all('span', class_="text")]
    authors_list = [author.text for author in soup.find_all('small', class_="author")]
    tags_list = [tag.text.replace('Tags:', '').strip().split('\n') for tag in soup.find_all('div', class_="tags")]
    for quote, author, tags in zip(quotes_list, authors_list, tags_list):
        QUOTES_INFO.append({
            'tags': tags,
            'author': author,
            'quote': quote,
            })
    return QUOTES_INFO

def authors():
    link_about_author = soup.find_all('a', string='(about)')
    for link in link_about_author:
        new_url = url + link['href']
        response = requests.get(new_url)
        soup_author = BeautifulSoup(response.text, 'html.parser')  # Новая переменная soup_author
        fullname = soup_author.find('h3', class_="author-title").text  # Исправлено на h2
        born_date = soup_author.find('span', class_="author-born-date").text  # Исправлено на author-born-date
        born_location = soup_author.find('span', class_="author-born-location").text
        description = soup_author.find('div', class_="author-description").text.strip()
        authors_dict = {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description,
            }
        AUTHORS_INFO.append(authors_dict)
    return AUTHORS_INFO

def write_json(filename, info):
    with open(filename, 'w', encoding='utf-8') as fd:
        json.dump(info, fd, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # quotes()
    # write_json('quotes.json', QUOTES_INFO)
    authors()
    write_json('authors.json', AUTHORS_INFO)


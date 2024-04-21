import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://quotes.toscrape.com/'

quotes_info = []  # Изменила название переменной
authors_info = []  # Изменила название переменной


def quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_list = [quote.text for quote in soup.find_all('span', class_="text")]
    authors_list = [author.text for author in soup.find_all('small', class_="author")]
    tags_list = [tag.text.replace('Tags:', '').strip().split('\n') for tag in soup.find_all('div', class_="tags")]
    for quote, author, tags in zip(quotes_list, authors_list, tags_list):
        quotes_info.append({
            'tags': tags,
            'author': author,
            'quote': quote,
            })
    
    # Проверяем наличие следующей страницы с цитатами
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_link = next_page.find('a')['href']
        next_page_url = BASE_URL + next_page_link
        quotes(next_page_url)  # Рекурсивно вызываем функцию для следующей страницы


def authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_about_author = soup.find_all('a', string='(about)')
    for link in link_about_author:
        new_url = BASE_URL + link['href']
        response = requests.get(new_url)
        soup_author = BeautifulSoup(response.text, 'html.parser')
        fullname = soup_author.find('h3', class_="author-title").text
        born_date = soup_author.find('span', class_="author-born-date").text
        born_location = soup_author.find('span', class_="author-born-location").text
        description = soup_author.find('div', class_="author-description").text.strip()
        authors_dict = {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description,
            }
        authors_info.append(authors_dict)
    
    # Проверяем наличие следующей страницы с информацией об авторах
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_link = next_page.find('a')['href']
        next_page_url = BASE_URL + next_page_link
        authors(next_page_url)  # Рекурсивно вызываем функцию для следующей страницы


def write_json(filename, info):
    with open(filename, 'w', encoding='utf-8') as fd:
        json.dump(info, fd, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    quotes(BASE_URL)  # Стартуем с первой страницы цитат
    write_json('quotes.json', quotes_info)  # Сохраняем цитаты в JSON
    authors(BASE_URL)  # Стартуем с первой страницы информации об авторах
    write_json('authors.json', authors_info)  # Сохраняем информацию об авторах в JSON

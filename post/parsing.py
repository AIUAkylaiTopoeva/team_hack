from bs4 import BeautifulSoup
import requests
from post.models import Post


# import os
# import django

# os.environ.setdefault('DJANGO_SETTIeNGS_MODULE', 'main.settings')
# django.setup()

'''Parsing'''
URl = 'https://music.kg/index.php?route=product/category&path=60_138'


def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('div', class_="pagination_wrap row").find('ul', class_='pagination').find_all('li')
    # print(page_list)
    last_page = page_list[-3].text
    # print(last_page)
    return int(last_page)

# print(get_total_pages(get_html(URl)))


def get_guitar_descriptions(html):
    soup = BeautifulSoup(html, 'lxml')
    guitars = soup.find_all('div', class_="product-thumb transition")
    for guitar in guitars:
        body = guitar.find('div', class_='caption').find('p', class_='description').text.strip()
        Post.objects.create(body=body)


def main():
    url = URl
    pages = '&page='
    html = get_html(url)
    total_pages = get_total_pages(html)
    get_guitar_descriptions(html)
    i = 2
    while i <= total_pages:
        url = f'{URl}{pages}{i}'
        html = get_html(url)
        get_guitar_descriptions(html)
        i+=1

if __name__ == '__name__':
    # os.environ.setdefault('DJANGO_SETTIeNGS_MODULE', 'main.settings')
    # django.setup()
    main()


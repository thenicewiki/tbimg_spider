import requests
import re
from bs4 import BeautifulSoup


def get_html(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    filename = url[-10:]
    soup_html = soup.prettify()
    with open(filename + '.html', 'w') as file:
        file.write(soup_html)
    return soup_html


def get_img(html):
    img_link_lst = re.findall('BDE_Image.+?=\"(http.+?jpg)\"', html)
    print(img_link_lst)
    return img_link_lst


def demo(url):
    img_lst = []
    for i in url:
        html = get_html(i)
        img_lst.extend(get_img(html))

    for j in img_lst:
        print('Spider consoles: ' + j)
    return img_lst



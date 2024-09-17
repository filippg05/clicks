import requests
import os
from urllib.parse import urlparse

API_KEY = os.getenv('VK_API_KEY')
url = input('Введите ссылку: ')


def is_shorten_link(url):
    parsed = urlparse(url)
    if 'vk.cc' in parsed.netloc:
        return True


def shorten_link(API_KEY, url):
    method = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": API_KEY,
        "v": "5.131",
        "url": url,
    }

    response = requests.get(method, params=params)
    response.raise_for_status()
    data = response.json()
    return data
    
   
def count_clicks(API_KEY, url):
    method = "https://api.vk.ru/method/utils.getLinkStats"
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith('/'):
        path = path[1:]
    params = {
        "access_token": API_KEY,
        "v": "5.199",
        "key": path,
        "interval": 'forever',
        "extended": 0,
    }
    response = requests.get(method, params=params)
    response.raise_for_status()
    data = response.json()
    return data


def main():
    if is_shorten_link(url):
        try:
            if 'views' not in count_clicks(API_KEY,url)['response']['stats']:
                print ('По вашей ссылке нет кликов')
            else:
                print('Всего кликов по вашей ссылке: ', count_clicks(API_KEY,url)['response']['stats'][0]['views'] )
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка при получении статистики кликов: {e}')
    else:
        try:
            print('Ваша сокращенная ссылка: ', shorten_link(API_KEY,url)['response']['short_url'])
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка при сокращении ссылки: {e}')




if __name__ == "__main__":
    main()

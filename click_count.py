import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def is_shorten_link(url):
    parsed = urlparse(url)
    return 'vk.cc' in parsed.netloc


def shorten_link(api_key, url):
    method = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": api_key,
        "v": "5.131",
        "url": url,
    }

    response = requests.get(method, params=params)
    response.raise_for_status()
    short_link = response.json()
    return short_link


def count_clicks(api_key, url):
    method = "https://api.vk.ru/method/utils.getLinkStats"
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith('/'):
        path = path[1:]
    params = {
        "access_token": api_key,
        "v": "5.199",
        "key": path,
        "interval": 'forever',
        "extended": 0,
    }
    response = requests.get(method, params=params)
    response.raise_for_status()
    clicks = response.json()
    return clicks


def main():
    load_dotenv()
    api_key = os.environ["VK_API_KEY"]
    parser = argparse.ArgumentParser(
        description='Получите сокращенную ссылку или количество кликов по ней.'
        )
    parser.add_argument("-link",  help="Введите ссылку",)
    args = parser.parse_args()
    url = args.link
    if is_shorten_link(url):
        try:
            if 'views' not in count_clicks(api_key, url)['response']['stats']:
                print('По вашей ссылке нет кликов')
            else:
                print('Всего кликов по вашей ссылке: ', count_clicks(api_key, url)['response']['stats'][0]['views'])
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка при получении статистики кликов: {e}')
    else:
        try:
            print('Ваша сокращенная ссылка: ', shorten_link(api_key, url)['response']['short_url'])
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка при сокращении ссылки: {e}')


if __name__ == "__main__":
    main()

import random
from collections import namedtuple
from xml.etree import ElementTree

import requests

Episode = namedtuple('Episode', 'title link pubdate show_id')
episode_data = {}


def main():
    show_header()
    download_data()
    latest_show_id = get_latest_show_id()
    print("Working with total of {} episodes".format(latest_show_id))
    display_results()


def display_results():
    start = random.randint(90, 110)
    latest_id = get_latest_show_id()
    end = random.randint(130, latest_id + 1)
    for show_id in range(start, end):
        info = get_episode(show_id)
        print("{}. {}".format(info.show_id, info.title))


def get_episode(show_id):
    return episode_data.get(show_id)


def get_latest_show_id():
    return max(episode_data.keys())


def download_data():
    url = 'https://talkpython.fm/episodes/rss'
    resp = requests.get(url)
    resp.raise_for_status()
    dom = ElementTree.fromstring(resp.text)
    items = dom.findall('channel/item')
    episode_count = len(items)
    for idx, item in enumerate(items):
        episode = Episode(
            item.find('title').text,
            item.find('link').text,
            item.find('pubDate').text,
            episode_count - idx - 1
        )
        episode_data[episode.show_id] = episode


def show_header():
    print("Welcome to the talk python info downloader.")
    print()


if __name__ == '__main__':
    main()

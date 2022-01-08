import requests
import bs4
from typing import Union
from .Casts import casts


class PeopleSearchResult:
    def __init__(self, urls: dict):
        self.names = tuple(urls.keys())
        self.urls = urls

    def __getitem__(self, item):
        if type(item) == str:
            return self.urls[item]
        elif type(item) == int:
            return self.names[item]
        else:
            raise TypeError

    def __len__(self):
        return len(self.names)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.names):
            index = self.__index
            self.__index += 1
            return self.names[index]
        else:
            raise StopIteration

    def __str__(self):
        return str(self.names)

    def get(self, x: Union[int, str]):
        if type(x) == int:
            return casts(self.urls[self.names[x]])
        elif type(x) == str:
            return casts(self.urls[x])

    def get_all(self, limit: int = 20):
        lst = []
        try:
            if limit > 20:
                limit = 20
        except TypeError:
            limit = 20
        for item in list(self.urls.keys())[:limit]:
            print('Getting:', item)
            lst.append(casts(self.urls[item]))
        return lst


def search_people(name: str, page: int = 1, max_results: int = 20, nationality: str = None) -> Union[PeopleSearchResult, None]:
    urls = {}
    if max_results > 20:
        print("Cannot have more than 20 Results!")
        max_results = 20
    url = f"https://mydramalist.com/search?q={name.replace(' ', '+')}&page={page}"
    soup = bs4.BeautifulSoup(requests.get(url).text, 'lxml')
    content = soup.find('div', class_='m-t nav-active-border b-primary').find_all('div', class_='box')
    for item in content:
        if not item.find('span', class_='pull-right jbtn-like'):
            continue
        # print(nationality.lower(), item.find('div', class_='text-muted').text.strip('\n').lower())
        if nationality and (nationality.lower() != item.find('div', class_='text-muted').text.strip('\n').lower()):
            continue
        artist = item.find('h6').text.strip('\n')
        if artist in urls.keys():
            artist += '/' + item.find('h6').a['href'].lstrip('/people/').split('-')[0]
        urls[artist] = item.find('h6').a['href']
        if len(urls) >= max_results:
            break
    if len(urls) > 0:
        return PeopleSearchResult(urls)
    else:
        return None

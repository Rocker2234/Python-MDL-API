import bs4
import requests
from typing import Union, List
from .Infopage import info, InfoPage


class SearchResult:
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

    def get(self, x: Union[int, str]) -> InfoPage:
        if type(x) == int:
            return info(self.urls[self.names[x]])
        elif type(x) == str:
            return info(self.urls[x])

    def get_all(self, limit: int = 20) -> List[InfoPage]:
        lst = []
        try:
            if limit > 20:
                limit = 20
        except TypeError:
            limit = 20
        for item in list(self.urls.keys())[:limit]:
            print('Getting:', item)
            lst.append(info(self.urls[item]))
        return lst


def search(name: str, page: int = 1, style: str = None, year=None, eps: int = None, score: str = None,
           match_all: bool = True, max_results: int = 20) -> Union[SearchResult, None]:
    urls = {}
    if max_results > 20:
        print("Cannot have more than 20 Results!")
        max_results = 20
    filters_given = any([style, year, eps, score])
    url = f"https://mydramalist.com/search?q={name.replace(' ', '+')}&page={page}"
    base = requests.get(url)
    soup = bs4.BeautifulSoup(base.text, 'lxml')
    results_box = soup.find('div', class_='col-lg-8 col-md-8').find_all('div', class_='box')
    for item in results_box:
        # Get Title
        try:
            curr_title = item.find("h6").find('a').text
        except AttributeError:
            return None

        # Get Category
        curr_cateory = item.find('span', class_='text-muted')

        # Check if Ctegory Exists
        if curr_cateory:
            curr_cateory = curr_cateory.text
        else:
            continue

        # Get URL
        curr_url = item.find("h6").find('a')['href']

        # Apply filters
        if filters_given:
            if match_all:
                filter_check = 15  # Has to match all filters given
            else:
                filter_check = 0  # Has to match atleast one of the filters given
            # In Binary from MSB [0] is style, [1] is year, [2] is eps, [3] is score

            # Check for Score
            curr_score = item.find('span', class_='score').text
            if score:
                if curr_score:
                    if score.endswith('+'):
                        if not float(curr_score) >= float(score.rstrip('+')):
                            filter_check &= 0b1110
                        else:
                            filter_check |= 0b0001
                    elif score.endswith('-'):
                        if not float(curr_score) <= float(score.rstrip('-')):
                            filter_check &= 0b1110
                        else:
                            filter_check |= 0b0001
                    else:
                        if not curr_score == score:
                            filter_check &= 0b1110
                        else:
                            filter_check |= 0b0001
                else:
                    filter_check &= 0b1110

            # Check for Episodes Filter
            if eps:
                if not ((curr_cateory.split(',')[-1]).startswith(f" {eps} episode")):
                    filter_check &= 0b1101
                else:
                    filter_check |= 0b0010

            # Check for Year Filter
            if year:
                if not curr_cateory.split(',')[0].split('-')[-1].strip() == str(year):
                    filter_check &= 0b1011
                else:
                    filter_check |= 0b0100

            # Check for Style Filter
            if style:
                if curr_cateory.find(style) == -1:
                    filter_check &= 0b0111
                else:
                    filter_check |= 0b1000

            # Add it to list if checks pass
            if match_all and filter_check == 15:
                urls[curr_title] = curr_url
            elif (not match_all) and filter_check != 0:
                urls[curr_title] = curr_url

        else:   # Directly add if no filters are given
            urls[curr_title] = curr_url
        if len(urls) >= max_results:
            break
    if len(urls) > 0:
        return SearchResult(urls)
    else:
        return None

import bs4
import requests
import warnings
from typing import Union, List
from .Infopage import info, InfoPage
from datetime import datetime
from .enums import *


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
            print('Getting:', item)  # noqa: 201
            lst.append(info(self.urls[item]))
        return lst


def search(name: str, page: int = 1, style: str = None, year=None, eps: int = None, score: str = None,
           match_all: bool = True, max_results: int = 20) -> Union[SearchResult, None]:
    urls = {}
    if max_results > 20:
        warnings.warn("Cannot have more than 20 Results! Setting it to 20 and continuing...")
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
            elif match_all and filter_check == 15:
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


def adv_search(name: str = None, page: int = 1,
               search_type: SearchType = SearchType.TITLE,
               release_date_initial: int = 1890,
               release_date_final: int = datetime.now().strftime('%Y'),
               title_types: List[TitleType] = None,
               title_status: TitleStatus = None,
               title_sorted_by: TitleSortedByType = TitleSortedByType.MOST_POPULAR,
               style: str = None,
               year=None,
               eps: int = None,
               score: str = None,
               match_all: bool = True,
               max_results: int = 20) -> Union[SearchResult, None]:

    urls = {}
    if max_results > 20:
        warnings.warn("Cannot have more than 20 Results! Setting it to 20 and continuing...")
        max_results = 20

    title_type_encoded = ""
    if title_types is not None:
        title_type_encoded = f"&ty={','.join(map(lambda t: str(t), title_types))}"

    title_status_encoded = ""
    if title_status is not None:
        title_status_encoded = f'&st={title_status}'

    release_date_encoded = ""
    if release_date_initial != 1890 or release_date_final != datetime.now().strftime('%Y'):
        release_date_encoded = f"&re={release_date_initial},{release_date_final}"

    sorted_encoded = f"&so={title_sorted_by}"

    filters_given = any([style, year, eps, score])
    url = f"https://mydramalist.com/search?adv={search_type}{title_type_encoded}{title_status_encoded}{release_date_encoded}{sorted_encoded}&page={page}"
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
            elif match_all and filter_check == 15:
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

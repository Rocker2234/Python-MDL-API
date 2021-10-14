import bs4
import requests


class SearchResult:
    def __init__(self, values):
        self.names = list(values.keys())
        self.urls = values

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


def search(name: str, page: int = 1, style: str = None, year: int = None, eps: int = None, score: str = None,
           match_all: bool = True, max_results=20):
    urls = {}
    if max_results > 20:
        print("Cannot have more than 20 Results!")
        max_results = 20
    url = f"https://mydramalist.com/search?q={name.replace(' ', '+')}&page={page}"
    base = requests.get(url)
    # noinspection PyUnboundLocalVariable
    soup = bs4.BeautifulSoup(base.text, 'lxml')
    results_box = soup.find('div', class_='col-lg-8 col-md-8').find_all('div', class_='box')
    for item in results_box[:max_results]:
        # Get Title
        curr_title = item.find("h6").find('a').text

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
        if match_all:
            filter_check = [True, True, True, True]  # Has to match all filters given
        else:
            filter_check = [False, False, False, False]  # Has to match atleast one of the filters given
        # [0] is style, [1] is year, [2] is eps, [3] is score

        # Check for Score
        curr_score = item.find('span', class_='score').text
        if score:
            if curr_score:
                if score.endswith('+'):
                    if not float(curr_score) >= float(score.rstrip('+')):
                        filter_check[3] = False
                    else:
                        filter_check[3] = True
                elif score.endswith('-'):
                    if not float(curr_score) <= float(score.rstrip('-')):
                        filter_check[3] = False
                    else:
                        filter_check[3] = True
                else:
                    if not curr_score == score:
                        filter_check[3] = False
                    else:
                        filter_check[3] = True
            else:
                filter_check[3] = False

        # Check for Episodes Filter
        if eps:
            if not ((curr_cateory.split(',')[-1]).startswith(f" {eps} episode")):
                filter_check[2] = False
            else:
                filter_check[2] = True

        # Check for Year Filter
        if year:
            if not curr_cateory.split(',')[0].split('-')[-1].strip() == str(year):
                filter_check[1] = False
            else:
                filter_check[1] = True

        # Check for Style Filter
        if style:
            if curr_cateory.find(style) == -1:
                filter_check[0] = False
            else:
                filter_check[0] = True

        # Add it to list if checks pass
        if match_all and filter_check == [True, True, True, True]:
            urls[curr_title] = curr_url
        elif (not match_all) and filter_check != [False, False, False, False]:
            urls[curr_title] = curr_url
    return SearchResult(urls)


if __name__ == "__main__":
    res = search('Yellow', 2, score='7.1-', year=2013, match_all=True)
    for i in res:
        print(i)

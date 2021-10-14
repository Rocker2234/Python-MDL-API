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
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.names):
            index = self.index
            self.index += 1
            return self.names[index]
        else:
            raise StopIteration

    def __str__(self):
        return str(self.names)


def search(name: str, style: str = None, year: int = None, eps: int = None, max_results=20):
    names = []
    urls = {}
    if max_results > 20:
        print("Cannot have more than 20 Results!")
        max_results = 20
    url = f"https://mydramalist.com/search?q={name.replace(' ', '+')}"
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
        filter_check = [True, True, True]  # This is to check for filters, [0] is style, [1] is year, [2] is eps

        # Check for Episodes Filter
        if eps:
            if not ((curr_cateory.split(',')[-1]).startswith(f" {eps} episode")):
                filter_check[2] = False

        # Check for Year Filter
        if year:
            if not curr_cateory.split(',')[0].split('-')[-1].strip() == str(year):
                filter_check[1] = False

        # Check for Style Filter
        if style:
            if curr_cateory.find(style) == -1:
                filter_check[0] = False

        # Add it to list if checks pass
        if filter_check == [True, True, True]:
            urls[curr_title] = curr_url
            names.append(curr_title)
        # Score
        # results[curr_title].append(item.find('span', class_='score').text)
        # Description
        # results[curr_title].append(item.find_all('p')[1].text)
    return SearchResult(urls)


if __name__ == "__main__":
    res = search('Flower of evil', year=2021)
    # print("Items:", ser.items)
    # print(ser.names)
    # print(ser.urls)
    print("Results:", len(res))
    for i in res:
        print(i)

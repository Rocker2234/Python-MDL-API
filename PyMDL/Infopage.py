import bs4
import requests


class InfoPage:
    def __init__(self, details):
        self.info = details.copy()
        self.info.pop('reco')
        self.info.pop('reviews')
        self.info.pop('synopsis')

        self.details = details

        allkeys = self.details.keys()

        if 'title' in allkeys:
            self.title = self.details['title']
        if 'thumbnail' in allkeys:
            self.thumbnail = self.details['thumbnail']
        if 'type' in allkeys:
            self.type = self.details['type']
        if 'synopsis' in allkeys:
            self.synopsis = self.details['synopsis']
        if 'casts' in allkeys:
            self.casts = self.details['casts']
        if 'native title' in allkeys:
            self.native = self.details['native title'].strip()
        if 'genres' in allkeys:
            self.genre = self.details['genres'].strip()
        if 'duration' in allkeys:
            self.duration = self.details['duration'].strip()
        if 'country' in allkeys:
            self.country = self.details['country'].strip()
        if 'also known as' in allkeys:
            self.aka = self.details['also known as'].split(",")
        if 'director' in self.details.keys():
            self.director = self.details['director']
            del self.details['director']
        if 'screenwriter' in self.details.keys():
            self.screenwriter = self.details['screenwriter']
            del self.details['screenwriter']
        if 'screenwriter & director' in self.details.keys():
            self.director = self.screenwriter = self.details['screenwriter & director']
            del self.details['screenwriter & director']
        del self.details['native title'], self.details['genres'], self.details['duration'], \
            self.details['country'], self.details['also known as']

        self.releasedate = self.__release()

        if details['reco']:
            self.rec = self.details['reco']
        if details['reviews']:
            self.reviews = self.details['reviews']

    def __str__(self):
        return str(self.info)

    def __release(self):
        date = "Not Recorded Yet"
        if self.type == "Movie":
            if 'release date' in self.details.keys():
                date = self.details['release date'].strip()
                del self.details['release date']
            return date
        else:
            if 'aired' in self.details.keys():
                date = self.details['aired'].strip()
                del self.details['aired']
            return date


def info(link: str):
    if not type(link) == str:
        raise UserWarning
    else:
        details = {}
        if link.startswith("https"):
            url = link
        else:
            url = f"https://mydramalist.com{link}"
        base = requests.get(url)
        # noinspection PyUnboundLocalVariable
        soup = bs4.BeautifulSoup(base.text, 'lxml')
        # Finding General Details
        mainbox = soup.find("div", class_="box")
        details['title'] = mainbox.find("h1", class_="film-title").text
        details['thumbnail'] = mainbox.find("img", class_="img-responsive")['src']
        details['ratings'] = mainbox.find("div", class_="row no-gutter").find("div", class_="hfs").text
        details['synopsis'] = mainbox.find("p").text.replace('\n', ' ')
        minibox = mainbox.find("div", class_="show-detailsxss").find("ul").find_all("li")
        for item in minibox[:5]:
            try:
                if item.text.split(":")[0].lower() == 'tags':
                    continue
                details[item.text.split(":")[0].lower()] = item.text.split(":")[1]
            except IndexError:
                continue
        castbox = soup.find("div", class_="box clear").find("div", class_="p-a-sm").find_all("b")
        casts = []
        for item in castbox:
            casts.append(item.text)
        details['casts'] = casts
        sidebox = soup.find("div", class_="box-body light-b").find_all("li")
        for item in sidebox[1:]:
            details[item.text.split(":")[0].lower()] = item.text.split(":")[1]
        if 'Duration' not in details.keys():
            details['duration'] = "Not Recorded Yet"
        # Checking if it is a Movie or Drama
        if 'Episodes' in details.keys():
            details['type'] = "Drama"
        else:
            details['type'] = "Movie"
        # Finding recommendations
        reclink = url + "/recs"
        recsoup = bs4.BeautifulSoup(requests.get(reclink).text, 'lxml')
        recbox = recsoup.find("div", class_="col-lg-8").find_all("div", class_="box-body")
        details['reco'] = []
        for item in recbox:
            if item.find('a', class_='btn primary'):
                continue
            details['reco'].append(item.find("a").text)
        # Finding Reviews
        revlink = url + "/reviews"
        revsoup = bs4.BeautifulSoup(requests.get(revlink).text, 'lxml')
        allreview = revsoup.find_all("div", class_="review")
        details['reviews'] = []
        for item in allreview:
            tofilter = item.find("div", class_="review-body")
            tags = str(tofilter).find("</p>") + 4
            details['reviews'].append(str(tofilter)[tags:str(tofilter).find("<p", tags)].replace("<br/>", "").strip())
        # Work on Review Filter
        return InfoPage(details)


if __name__ == "__main__":
    var = info("/40257-round-six")
    print(var)

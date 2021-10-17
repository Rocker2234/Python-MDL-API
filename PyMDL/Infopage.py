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
            self.title = self.details.pop('title')
        if 'thumbnail' in allkeys:
            self.thumbnail = self.details.pop('thumbnail')
        if 'type' in allkeys:
            self.type = self.details.pop('type')
        if 'synopsis' in allkeys:
            self.synopsis = self.details.pop('synopsis')
        if 'casts' in allkeys:
            self.casts = self.details.pop('casts')
        if 'native title' in allkeys:
            self.native = self.details.pop('native title').strip()
        if 'genres' in allkeys:
            self.genre = self.details.pop('genres').strip()
        if 'duration' in allkeys:
            self.duration = self.details.pop('duration').strip()
        if 'country' in allkeys:
            self.country = self.details.pop('country').strip()
        if 'also known as' in allkeys:
            self.aka = self.details.pop('also known as').split(",")
        if 'director' in self.details.keys():
            self.director = self.details.pop('director')
        if 'screenwriter' in self.details.keys():
            self.screenwriter = self.details.pop('screenwriter')
        if 'screenwriter & director' in self.details.keys():
            self.director = self.screenwriter = self.details.pop('screenwriter & director')

        self.releasedate = self.__release()

        if 'reco' in self.details.keys():
            self.rec = self.details.pop('reco')
        if 'reviews' in self.details.keys():
            self.rec = self.details.pop('reviews')

    def __str__(self):
        return str(self.info)

    def __release(self):
        date = "Not Recorded Yet"
        if self.type == "Movie":
            if 'release date' in self.details.keys():
                date = self.details.pop('release date').strip()
            return date
        else:
            if 'aired' in self.details.keys():
                date = self.details.pop('aired').strip()
            return date


def info(link: str):
    if not type(link) == str:
        raise TypeError
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
        revsoup = bs4.BeautifulSoup(requests.get(url + "/reviews").text, 'lxml')
        rlist = revsoup.find_all('div', class_="review")
        scrs = []
        for item in rlist:
            erviw = item.find_all("div", class_="row")
            for items in erviw:
                sbox = items.find_all("div", class_="box pull-right text-sm m-a-sm")
                for things in sbox:
                    scrs.append(str(things.text))  # Getting Side Scores
        frev = []
        for item in rlist:
            erviw = item.find_all("div", class_="row")
            for items in erviw:
                reviews = items.find_all("div", class_="review-body")
                for things in reviews:
                    frev.append(str(things.text))   # Getting Reviews
        remove1 = "Was this review helpful to you? Yes No Cancel"
        remove2 = "Read More"
        final = []
        if len(frev) == len(scrs):
            for item in range(len(frev)):
                final.append(((frev[item].replace(scrs[item], "").replace(remove1, "")).replace(remove2, "").strip()).replace("  ", ":- "))     # Final Review
        details['reviews'] = final
        return InfoPage(details)


# Testing
# if __name__ == "__main__":
#     var = info("/26136-parasite-war")
#     print(var.reviews)

import json
import bs4
import requests


class InfoPage:
    def __init__(self, details: dict):
        self.details = details
        self.reco = []
        self.reviews = []
        allkeys = self.details.keys()
        self.url = self.details.pop('url')

        if 'title' in allkeys:
            self.title = self.details.pop('title')
        else:
            self.title = None
        if 'thumbnail' in allkeys:
            self.thumbnail = self.details.pop('thumbnail')
        else:
            self.thumbnail = None
        if 'type' in allkeys:
            self.type = self.details.pop('type')
        else:
            self.type = None
        if 'ratings' in allkeys:
            self.ratings = self.details.pop('ratings')
        else:
            self.ratings = None
        if 'synopsis' in allkeys:
            self.synopsis = self.details.pop('synopsis')
        else:
            self.synopsis = None
        if 'casts' in allkeys:
            self.casts = self.details.pop('casts')
        else:
            self.casts = None
        if 'native title' in allkeys:
            self.native = self.details.pop('native title').strip()
        else:
            self.native = None
        if 'genres' in allkeys:
            self.genre = self.details.pop('genres').strip()
        else:
            self.genre = None
        if 'duration' in allkeys:
            self.duration = self.details.pop('duration').strip()
        else:
            self.duration = None
        if 'country' in allkeys:
            self.country = self.details.pop('country').strip()
        else:
            self.country = None
        if 'also known as' in allkeys:
            self.aka = self.details.pop('also known as').split(",")
        else:
            self.aka = None
        if 'director' in allkeys:
            self.director = self.details.pop('director')
        else:
            self.director = None
        if 'screenwriter' in allkeys:
            self.screenwriter = self.details.pop('screenwriter')
        else:
            self.screenwriter = None
        if 'screenwriter & director' in allkeys:
            self.director = self.screenwriter = self.details.pop('screenwriter & director')
        self.date = "N/A"
        if self.type == "Movie":
            if 'release date' in allkeys:
                self.date = self.details.pop('release date').strip()
        else:
            if 'aired' in allkeys:
                self.date = self.details.pop('aired').strip()

    # Finding recommendations
    def get_recomendations(self):
        reclink = self.url + "/recs"
        recsoup = bs4.BeautifulSoup(requests.get(reclink).text, 'lxml')
        recbox = recsoup.find("div", class_="col-lg-8").find_all("div", class_="box-body")
        for item in recbox:
            if item.find('a', class_='btn primary'):
                continue
            self.reco.append(item.find("a").text)

    # Finding Reviews
    def get_reviews(self):
        revsoup = bs4.BeautifulSoup(requests.get(self.url + "/reviews").text, 'lxml')
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
                    frev.append(str(things.text))  # Getting Reviews
        remove1 = "Was this review helpful to you? Yes No Cancel"
        remove2 = "Read More"
        final = []
        if len(frev) == len(scrs):
            for item in range(len(frev)):
                final.append(
                    ((frev[item].replace(scrs[item], "").replace(remove1, "")).replace(remove2, "").strip()).replace(
                        "  ", ":- "))  # Final Review
        self.reviews = final

    def dumps(self) -> dict:
        ret = {
            self.title:
                {
                    'date': self.date,
                    'thumbnail': self.thumbnail,
                    'type': self.type,
                    'ratings': self.ratings,
                    'synopsis': self.synopsis,
                    'casts': self.casts,
                    'native title': self.native,
                    'genere': self.genre,
                    'duration': self.duration,
                    'country': self.country,
                    'aka': self.aka,
                    'director': self.director,
                    'screenwriter': self.screenwriter
                }
        }
        if len(self.reco):
            ret['recommendations'] = self.reco
        if len(self.reviews):
            ret['reviews'] = self.reviews
        return ret

    def to_json(self):
        return json.dumps(self.dumps())

    def save(self, file: str):
        try:
            with open(file) as f:
                try:
                    loaded = json.load(f)
                except json.decoder.JSONDecodeError:
                    loaded = False
            with open(file, 'w') as f:
                if loaded:
                    json.dump({**loaded, **self.dumps()}, f, indent=4)
                else:
                    json.dump(self.dumps(), f, indent=4)
            return True
        except FileNotFoundError:
            with open(file, 'w') as f:
                json.dump(self.dumps(), f, indent=4)
                return True
        except Exception as e:
            print("Got Exception\n", e)
            return False

    def __str__(self):
        return str(self.dumps())


def info(link: str):
    if not type(link) == str:
        raise TypeError
    else:
        details = {}
        if link.startswith("https"):
            url = link
        else:
            url = f"https://mydramalist.com{link}"
        details['url'] = url
        base = requests.get(url)
        # noinspection PyUnboundLocalVariable
        soup = bs4.BeautifulSoup(base.text, 'lxml')

        # Finding General Details
        details['title'] = soup.find("div", class_="col-lg-8 col-md-8 col-rightx").find('h1', class_='film-title').text
        mainbox = soup.find("div", class_="col-lg-8 col-md-8 col-rightx").find('div', class_='box-body')
        details['thumbnail'] = mainbox.find("img", class_="img-responsive")['src']
        details['synopsis'] = mainbox.find("div", class_='show-synopsis').find('span').text.replace('\n', ' ')

        # Finding Ratings
        details['ratings'] = mainbox.find("div", class_="hfs", itempropx="aggregateRating")
        if details['ratings']:
            # noinspection PyUnresolvedReferences
            details['ratings'] = details['ratings'].find("b").text

        detailed_info = mainbox.find("div", class_="show-detailsxss").find("ul").find_all("li")
        req_info = ['native title', 'also known as', 'director', 'screenwriter', 'screenwriter & director', 'genres']
        for item in detailed_info:
            try:
                # if item.text.split(":")[0].lower() == 'tags':
                #     continue
                field = item.find('b').text.lower().rstrip(':')
                if field in req_info:
                    curr_info = ""
                    for i in item.find_all('a'):
                        curr_info += i.text + ", "
                    curr_info = curr_info.rstrip(', ').strip()
                    if curr_info != '':
                        details[field] = curr_info
            except IndexError:
                continue
        cast_names = soup.find('div', class_='col-lg-8 col-md-8 col-rightx').\
            find("div", class_="box clear").find("div", class_="p-a-sm").find_all("b")
        casts = []
        for item in cast_names:
            casts.append(item.text)
        details['casts'] = casts
        details_box = soup.find("div", class_="box-body light-b").ul.find_all("li")
        for item in details_box[1:]:
            details[item.text.split(":")[0].lower()] = item.text.split(":")[1].strip()
        if 'duration' not in details.keys():
            details['duration'] = "N/A"

        # Checking if it is a Movie or Drama
        if 'episodes' in details.keys():
            details['type'] = "Drama"
        else:
            details['type'] = "Movie"
        return InfoPage(details)

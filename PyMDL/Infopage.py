import bs4
import requests


class InfoPage:
    def __init__(self, details):
        self.info = details
        self.title = details['title']
        self.thumbnail = details['thumbnail']
        self.type = details['type']
        self.casts = details['casts']
        self.details = {**details['details'], **details['sdetails']}
        self.releasedate = self.__release()
        self.native, self.genre, self.duration, self.country, self.aka, self.director = self.__break()

    def __str__(self):
        return str(self.info)

    def __release(self):
        if self.type == "Drama":
            date = self.details['Release Date'].strip()
            del self.details['Release Date']
            return date
        else:
            date = self.details['Aired'].strip()
            del self.details['Aired']
            return date

    def __break(self):
        broken = [self.details['Native Title'].strip(),
                  self.details['Genres'].strip(),
                  self.details['Duration'].strip(),
                  self.details['Country'].strip(),
                  self.details['Also Known As'].split(","),
                  self.details['Screenwriter & Director'].strip()]
        del self.details['Native Title'], self.details['Genres'], self.details['Duration'], \
            self.details['Country'], self.details['Also Known As'], self.details['Screenwriter & Director']
        return broken


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
        mainbox = soup.find("div", class_="box")
        details['title'] = mainbox.find("h1", class_="film-title").text
        details['thumbnail'] = mainbox.find("img", class_="img-responsive")['src']
        details['ratings'] = mainbox.find("div", class_="row no-gutter").find("div", class_="hfs").text
        details['description'] = mainbox.find("p").text.replace('\n', ' ')
        minibox = mainbox.find("div", class_="show-detailsxss").find("ul").find_all("li")
        details['details'] = {}
        for item in minibox[:5]:
            details['details'][item.text.split(":")[0]] = item.text.split(":")[1]
        castbox = soup.find("div", class_="box clear").find("div", class_="p-a-sm").find_all("b")
        casts = []
        for item in castbox:
            casts.append(item.text)
        details['casts'] = casts
        sidebox = soup.find("div", class_="box-body light-b").find_all("li")
        details['sdetails'] = {}
        getkey = []
        for item in sidebox:
            details['sdetails'][item.text.split(":")[0]] = item.text.split(":")[1]
            getkey.append(item.text.split(':')[0])
        del details['sdetails'][getkey[0]]
        # Checkin if it is a Movie or Drama
        if details['sdetails'].keys() == 'Episodes':
            details['type'] = "Drama"
        else:
            details['type'] = "Movie"

        return InfoPage(details)


var = info("/40257-round-six")
print(var.details.keys())

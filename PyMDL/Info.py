import bs4
import requests


class InfoPage:
    def __init__(self):
        self.details = {}

    def Info(self, link=None):
        if link is None:
            return print("Nothing found")
        else:
            url = f"https://mydramalist.com{link}"
            base = requests.get(url)
            # noinspection PyUnboundLocalVariable
            soup = bs4.BeautifulSoup(base.text, 'lxml')
            mainbox = soup.find("div", class_="box")
            self.details['titlename'] = mainbox.find("h1", class_="film-title").text
            self.details['thumbnail'] = mainbox.find("img", class_="img-responsive")['src']
            self.details['ratings'] = mainbox.find("div", class_="row no-gutter").find("div", class_="hfs").text
            self.details['description'] = mainbox.find("p").text
            minibox = mainbox.find("div", class_="show-detailsxss").find("ul").find_all("li")
            self.details['details'] = {}
            for item in minibox[:5]:
                self.details['details'][item.text.split(":")[0]] = item.text.split(":")[1]
            castbox = soup.find("div", class_="box clear").find("div", class_="p-a-sm").find_all("b")
            casts = []
            for item in castbox:
                casts.append(item.text)
            self.details['casts'] = casts
            sidebox = soup.find("div", class_="box-body light-b").find_all("li")
            self.details['sdetails'] = {}
            getkey = []
            for item in sidebox:
                self.details['sdetails'][item.text.split(":")[0]] = item.text.split(":")[1]
                getkey.append(item.text.split(':')[0])
            del self.details['sdetails'][getkey[0]]
            # Checkin if it is a Movie or Drama
            if self.details['sdetails'].keys() == 'Episodes':
                self.details['type'] = "Drama"
            else:
                self.details['type'] = "Movie"
            # Printing
            # print("Titlename:", self.details['titlename'], "\nThumbnail:", self.details['thumbnail'], "\nType:", self.details['type'], "\nRatings:", self.details['ratings'], "\nDescription:", self.details['description'],
            #       "\nDetails: -")
            # for item in self.details['details']:
            #     print(f"{item} : {self.details['details'][item]}")
            # for item in self.details['sdetails']:
            #     print(f"{item} : {self.details['sdetails'][item]}")
            # print("Casts:-")
            # i = 1
            # for item in self.details['casts']:
            #     print(i, item)
            #     i += 1
            # print(self.details)


if __name__ == "__main__":
    info = InfoPage()
    info.Info("/35187-water-hole")
    print(info.details)

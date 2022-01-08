import requests
import bs4


class Cast:
    def __init__(self, details: dict):
        self.details = details
        keys = self.details.keys()
        self.desciption = self.details.pop('life')
        self.url = self.details.pop('url')
        if 'name' in keys:
            self.name = self.details.pop('name')
        else:
            self.name = None
        if 'thumbnail' in keys:
            self.thumbnail = self.details.pop('thumbnail')
        else:
            self.thumbnail = None
        if 'family name' in keys:
            self.family_name = self.details.pop('family name')
        else:
            self.family_name = None
        if 'native name' in keys:
            self.native_name = self.details.pop('native name')
        else:
            self.native_name = None
        if 'nationality' in keys:
            self.nationality = self.details.pop('nationality')
        else:
            self.nationality = None
        if 'gender' in keys:
            self.gender = self.details.pop('gender')
        else:
            self.gender = None
        if 'born' in keys:
            self.dob = self.details.pop('born')
        else:
            self.dob = None
        if 'age' in keys:
            self.age = self.details.pop('age')
        else:
            self.age = None
        if 'workfile' in keys:
            self.works = self.details.pop('workfile')
        else:
            self.works = None

    def __str__(self):
        return str(f'Info on <{self.name}>')


def casts(link: str) -> Cast:
    if not type(link) == str:
        raise TypeError
    else:
        details = {}
        if link.startswith("https"):
            url = link
        else:
            url = f"https://mydramalist.com{link}"
        base = requests.get(url)
        details['url'] = url
        # noinspection PyUnboundLocalVariable
        soup = bs4.BeautifulSoup(base.text, 'lxml')

        # Finding Name
        details['name'] = soup.find("div", class_="box-header p-b-0 text-center").find("h1").text.strip('\n')

        # Finding General Details
        details['thumbnail'] = soup.find("div", class_="col-lg-4 col-md-4").find("div", class_="box-body").find("img", class_='img-responsive')['src']
        mainbox = soup.find("div", class_="col-sm-8 col-lg-12 col-md-12")
        mainbox.find("div", class_='hidden-md-up m-b-1').decompose()
        details['life'] = mainbox.text.strip('\n')

        # Finding Info
        contents = soup.find("div", class_="box-body light-b").find_all("li")
        for item in contents:
            try:
                if item.text.split(":")[0].lower() == 'tags':
                    continue
                details[item.text.split(":")[0].lower()] = item.text.split(":")[1].strip()
            except IndexError:
                continue

        # Finding All the Works
        works = soup.find('div', class_='col-lg-8 col-md-8').find("div", class_="box")
        works = works.find_all("div", class_="box-body")[1]
        tables = works.find_all('table')
        workfile = {}  # For getting Titles of tables
        for item in works.find_all("h5"):
            workfile[item.text.lower()] = []
            curr_values = []
            curr_work = tables[0].tbody
            del tables[0]
            for tr in curr_work.find_all('tr'):
                for td in tr.find_all('td'):
                    try:
                        td.find('div', class_='text-muted').decompose()
                        td.find('button').decompose()
                    except AttributeError:
                        pass
                    curr_values.append(td.text.replace('\n', ''))
                workfile[item.text.lower()].append(curr_values)
                curr_values = []
        details['workfile'] = workfile
    return Cast(details)

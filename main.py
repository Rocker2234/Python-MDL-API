import bs4
import requests


try:
    url = f"https://mydramalist.com/search?q={'Move to Heaven'.replace(' ', '+')}"
    a = requests.get(url)
except requests.exceptions.ConnectionError:
    print("Problem connecting! Check your internet connection!")
    exit(1)

# noinspection PyUnboundLocalVariable
soup = bs4.BeautifulSoup(a.text, 'lxml')
soup.find()

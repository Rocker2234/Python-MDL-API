from bs4 import BeautifulSoup
import requests
import csv

try:
    a = requests.get('https://www.imdb.com/india/top-rated-indian-movies/')
except requests.exceptions.ConnectionError:
    print("Problem connecting! Check your internet connection!")
    exit(1)

# noinspection PyUnboundLocalVariable
soup = BeautifulSoup(a.text, 'lxml')
movies = soup.find('tbody').find_all('tr')
data = []

for movie in movies:
    poster = movie.find('td', class_='posterColumn').find('a').find('img')['src']
    title = movie.find('td', class_='titleColumn').find('a').text
    year = movie.find('td', class_='titleColumn').find('span').text.lstrip('(').rstrip(')')
    rating = movie.find('td', class_='ratingColumn imdbRating').find('strong').text
    data.append({'poster': poster, 'title': title, 'year': year, 'rating': rating})

f = open('list.csv', 'w', newline='', encoding='UTF-8')
if len(data) > 0:
    csv.writer(f).writerow(['title', 'year', 'rating', 'poster'])

for item in data:
    print(f"Title:{item['title']}\nYear:{item['year']}\nRating:{item['rating']}\nPoster Link:{item['poster']}",
          end='\n---------\n\n')
    csv.writer(f).writerow([item['title'], item['year'], item['rating'], item['poster']])

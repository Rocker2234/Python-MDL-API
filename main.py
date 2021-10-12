import bs4
import requests


movie = input("Name:")

try:
    url = f"https://mydramalist.com/search?q={movie.replace(' ', '+')}"
    a = requests.get(url)
except requests.exceptions.ConnectionError:
    print("Problem connecting! Check your internet connection!")
    exit(1)

# noinspection PyUnboundLocalVariable
soup = bs4.BeautifulSoup(a.text, 'lxml')
results_page = soup.find('div', class_='col-lg-8 col-md-8').find_all('div', class_='box')

results = {}

for item in results_page:
    # Titles
    curr_title = item.find("h6").find('a').text
    results[curr_title] = []
    # Category
    results[curr_title].append(item.find('span', class_='text-muted').text)
    # Score
    results[curr_title].append(item.find('span', class_='score').text)
    # Desc
    # print(item.find_all('p')[1].text)
    # print(curr_title, ":", results[curr_title])

print("Found", len(results), "Results!")
for key in results.keys():
    print(f"{key}: {results[key]}")
    print('\n ----------- \n')

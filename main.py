from bs4 import BeautifulSoup
import requests
import json

url = 'https://news.ycombinator.com/'
response = requests.get(url)
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, 'html.parser')
title_elements = soup.select('.titleline > a')
score_elements = soup.select('.subline .score')
author_elements = soup.select('.subline .hnuser')
age_elements = soup.select('.subline .age')
comments_elements = soup.select('.subline a')

titles = [title.getText() for title in title_elements]
links = [title['href'] for title in title_elements]
scores = [int(score.getText().split()[0]) for score in score_elements]
authors = [author.getText() for author in author_elements]
ages = [age.getText() for age in age_elements]
comments = [int(comment.getText().split('\xa0')[0])
            for comment in comments_elements if 'comment' in comment.getText()]

scraped_data = {}

for title, link, score, author, age, comment in zip(titles, links, scores, authors, ages, comments):
    scraped_data[title] = {
        'link': link,
        'score': score,
        'author': author,
        'age': age,
        'comments': comment
    }
top_5_articles = sorted(scraped_data.items(),
                        key=lambda x: x[1]['score'], reverse=True)[:5]


with open('scraped_data.json', 'w') as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

with open('top_5_articles.json', 'w') as json_file:
    json.dump(dict(top_5_articles), json_file, indent=4, ensure_ascii=False)

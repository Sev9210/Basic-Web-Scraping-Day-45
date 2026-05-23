from bs4 import BeautifulSoup
import requests
import json

url = 'https://news.ycombinator.com/'
response = requests.get(url)
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, 'html.parser')


scraped_data = {}
# This loop will check whatever it found inside a tag that has a class of .athing and .submission.
# I can choose either of the two class but i used both for precision
for row in soup.select('.athing.submission'):
    # this will select a tag with a class .titleline with a direct child <a>
    # then Check if it exist if not it'll create a default value for safety and to prevent misaligning the the data
    title_elements = row.select_one('.titleline > a')
    title = title_elements.getText()if title_elements else 'No title'
    link = title_elements.get('href') if title_elements else 'No link found'

    # this is to initialize the next sibling of the tag holding the .athing.submission
    # this also the one that is holding the tags for socre,comment,age and author
    subtext_row = row.find_next_sibling('tr')

    # initialize all the variables needed below.
    # these are the variables that will hold all the values found or scraped from the website
    # buy default it has no content yet.
    score = 0
    author = 'Unknown'
    age = 'Unknown'
    comment = 0

    # the block of code will find the value for the variables above this comment
    if subtext_row:
        # here it will select the tags that correspondes to the variable above
        # Note: i am selecting only the tag that has the possible content not the actual content or str.
        score_tag = subtext_row.select_one('.score')
        author_tag = subtext_row.select_one('.hnuser')
        age_tag = subtext_row.select_one('.age')
        comment_tag = subtext_row.select_one('.a')

        # this will check first if the tags are really exist if it doesnt the default value for score,author,age and comment will be the default initialized above

        if score_tag:
            score = int(score_tag.getText().split()[0])
        if author_tag:
            author = author_tag.getText()
        if age_tag:
            age = age_tag.getText()
        # this is for checking its precens as well but as you can see, it is a for loop
        # what's happening here is that the subtext_row has multiple <a> tags so to target the desired tag, i need to loop those <a>tags with the 'comment' string as content
        for a in subtext_row.select('a'):
            # here in each iteration from subtext_row.select(a), the value of a will be passed to text as text.
            text = a.get_text()
            # here it will read the text or the content of the tag if it has a 'comment' string, if it does, then it will split the string to get rid of the 'Points' ex: (56 Points to 56) then turn it to integer, if the comment doesnt exist then it will return a value of 0
            if 'comment' in text or 'discuss' in text:
                if text.split()[0].isdigit():
                    comment = int(text.split()[0])
                else:
                    comment = 0
                break

    # here is the structure of the dictionary
    # each title should have the data below
    scraped_data[title] = {

        'link': link,
        'score': score,
        'author': author,
        'age': age,
        'comments': comment
    }
# this will sort all the article found with its content and then only get the first 5 items based on score from highest to lowest
top_five_articles = sorted(
    scraped_data.items(), key=lambda x: x[1]['score'], reverse=True)[:5]

# the code below will only make a json file to save all the sraped data and the sorted data
with open('scraped_data.json', 'w') as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

with open('top_five_articles.json', 'w') as json_file:
    json.dump(dict(top_five_articles), json_file, indent=4, ensure_ascii=False)

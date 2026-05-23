# Hacker News (Y Combinator) Web Scraper - Day 45 (Modified Mastery)
IMPORTANT NOTE: THIS IS JUST A BASIC WEBSRAPING FOR STATIC WEBPAGE
A highly structured, production-ready Python web scraper that accurately parses the Hacker News homepage. While built as part of **Day 45 of the "100 Days of Code: The Complete Python Pro Bootcamp"**, this code skips the fragile, standard list-zipping tutorial architecture in favor of a robust **Row-by-Row Extraction Blueprint**.

## 🎯 The Challenge: Why the Original Goal Fails
The standard Day 45 curriculum relies on scraping global lists separately and then using `zip()` to stitch them together. However, Hacker News has a highly dynamic layout:
* Brand new stories **completely omit** the score span tag (`.score`).
* Stories with zero comments replace numbers with the static word `"discuss"`.
* Blank spacer rows stand between articles as layout artifacts.

Scraping these dynamically hidden values into global lists changes their total sizes (e.g., 30 titles but only 27 scores), causing `zip()` to mismatch your columns. This implementation completely resolves that by processing elements bound strictly to their respective rows.

## 🛠️ Complete Code Strategy & Logic Flow

### 1. Multi-Class Precision Anchor
```python
for row in soup.select('.athing.submission'):
```
The scraper anchors itself directly onto the core table rows. It selects the tags matching *both* `.athing` and `.submission` to precisely target the main article boxes while smoothly bypassing blank layout spacer rows.

### 2. Isolated Single-Element Drilling
```python
title_elements = row.select_one('.titleline > a')
```
Instead of matching deep global targets, `row.select_one()` searches exclusively *inside the current active row loop iteration*. Using the direct child combinator (`>`) ensures it matches only the main article title while bypassing sub-domain hyperlinks.

### 3. Sibling Leap Framework
```python
subtext_row = row.find_next_sibling('tr')
```
Because the metadata values (points, author, comment links) live on a separate row directly below the title container, the code jumps sideways using `.find_next_sibling('tr')` to isolate the target row without getting stuck on hidden text node newlines (`\n`).

### 4. Intentional Fallback Defaults
```python
score = 0
author = 'Unknown'
age = 'Unknown'
comment = 0
```
Variables are initialized with zero/neutral defaults *before* parsing the HTML values. If an article doesn't have an upvote score or comment link yet, the code gracefully retains these values instead of throwing a `NoneType` attribute crash or throwing the loop alignment out of whack.

### 5. Deep Keyword Text Identification
```python
for a in subtext_row.select('a'):
    text = a.get_text()
    if 'comment' in text or 'discuss' in text:
```
Because comments lack a unique custom class name, the scraper loops through all inside anchor links and checks the human-readable text contents for strings containing `'comment'` or `'discuss'`. It isolates the correct text, uses `.split()[0]` to parse out numbers, and casts strings like `"157 comments"` into pure structural integers (`157`).

### 6. Anonymous Lambda Data Slicing
```python
top_five_articles = sorted(scraped_data.items(), key=lambda x: x[1]['score'], reverse=True)[:5]
```
Utilizes a one-line lambda expression acting as a structural map path through dictionary elements (`x[1]['score']`) to sort the data list matrix purely by score integers from highest to lowest, immediately trimming it down to the top 5 elite entries.

## 📋 Project Output Format
The tool automatically compiles findings into two clean, localized storage files:

1. `scraped_data.json`: The complete collection of front-page articles.
2. `top_five_articles.json`: The top 5 highest-voted stories currently trending.

```json
{
    "Shipping a laptop to a refugee camp in Uganda": {
        "link": "https://notesbylex.com",
        "score": 436,
        "author": "lexandstuff",
        "age": "11 hours ago",
        "comments": 157
    }
}
```

## ⚙️ Installation & Usage

1. Open your terminal inside the project directory:
   ```bash
   cd bs4-start
   ```
2. Activate your workspace virtual environment:
   ```bash
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```
3. Install necessary web libraries:
   ```bash
   pip install beautifulsoup4 requests
   ```
4. Run the scraper:
   ```bash
   python main.py
   ```

